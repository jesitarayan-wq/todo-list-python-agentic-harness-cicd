#!/usr/bin/env python3
"""Allow-list egress proxy for agent containers in restricted-network mode.

Agent containers on the internal Docker network cannot reach the internet. Their only way
out is this proxy, which tunnels HTTPS (CONNECT) to hosts on the allow-list and refuses the
rest. Every decision is written to a JSON-lines log.

Settings (environment variables):
  EGRESS_MODE        enforce (default) or learn (allow every host on an allowed port, log them all)
  EGRESS_ALLOW_FILE  allow-list file, one host per line; *.example.com matches subdomains
  EGRESS_LOG         log file (JSON lines)
  EGRESS_PORT        listening port (default 3128)
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_PORTS_DEFAULT = frozenset({443})
CONNECT_TIMEOUT = 10
HEAD_TIMEOUT = 15
IDLE_TIMEOUT = 600


def load_rules(text: str) -> list[str]:
    """Read allow-list lines; blank lines and # comments are ignored."""
    rules = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip().lower()
        if line:
            rules.append(line)
    return rules


def host_allowed(host: str, rules: list[str]) -> bool:
    """Exact match, or *.domain.tld for any subdomain (not the bare domain)."""
    host = host.strip().lower().rstrip(".")
    if not host:
        return False
    for rule in rules:
        if rule.startswith("*."):
            if host.endswith(rule[1:]):
                return True
        elif host == rule:
            return True
    return False


def parse_connect(line: str):
    """Return (host, port) for 'CONNECT host:port HTTP/1.1', or None for anything else."""
    parts = line.strip().split()
    if len(parts) != 3 or parts[0].upper() != "CONNECT":
        return None
    host, sep, port = parts[1].rpartition(":")
    if not sep or not host or host.startswith("[") or not port.isdigit():
        return None
    return host, int(port)


def decide(host: str, port: int, rules: list[str], mode: str, allowed_ports) -> tuple[str, str]:
    if port not in allowed_ports:
        return "denied", "port not allowed"
    if mode == "learn":
        return "allowed", "learn mode: every host is allowed and logged"
    if host_allowed(host, rules):
        return "allowed", "on the allow-list"
    return "denied", "not on the allow-list"


def write_log(path, record: dict) -> None:
    record = {"time": datetime.now(timezone.utc).isoformat(), **record}
    line = json.dumps(record)
    print(line, flush=True)
    if path:
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")


async def pipe(reader, writer) -> None:
    try:
        while True:
            data = await asyncio.wait_for(reader.read(65536), IDLE_TIMEOUT)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except (asyncio.TimeoutError, ConnectionError, OSError):
        pass
    finally:
        try:
            writer.close()
        except Exception:
            pass


async def reply(writer, status: str, body: str = "") -> None:
    payload = body.encode("utf-8")
    head = f"HTTP/1.1 {status}\r\nContent-Type: text/plain\r\nContent-Length: {len(payload)}\r\nConnection: close\r\n\r\n"
    writer.write(head.encode("latin-1") + payload)
    try:
        await writer.drain()
    finally:
        writer.close()


def make_handler(rules_provider, mode: str, allowed_ports, log_path):
    async def handle(reader, writer):
        peer = writer.get_extra_info("peername")
        client = peer[0] if peer else "unknown"
        try:
            head = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), HEAD_TIMEOUT)
        except (asyncio.TimeoutError, asyncio.IncompleteReadError, asyncio.LimitOverrunError, ConnectionError):
            writer.close()
            return
        first = head.split(b"\r\n", 1)[0].decode("latin-1")
        target = parse_connect(first)
        if target is None:
            write_log(log_path, {"decision": "denied", "host": "", "port": 0, "mode": mode, "client": client,
                                 "reason": "only HTTPS tunnels (CONNECT) are supported", "request": first[:100]})
            await reply(writer, "403 Forbidden", "Blocked by the egress proxy: only HTTPS tunnels are supported.\n")
            return
        host, port = target
        decision, reason = decide(host, port, rules_provider(), mode, allowed_ports)
        write_log(log_path, {"decision": decision, "host": host, "port": port, "mode": mode, "client": client, "reason": reason})
        if decision == "denied":
            await reply(writer, "403 Forbidden", f"Blocked by the egress allow-list: {host}:{port} ({reason})\n")
            return
        try:
            up_reader, up_writer = await asyncio.wait_for(asyncio.open_connection(host, port), CONNECT_TIMEOUT)
        except (OSError, asyncio.TimeoutError) as exc:
            write_log(log_path, {"decision": "error", "host": host, "port": port, "mode": mode, "client": client,
                                 "reason": f"upstream connection failed: {exc}"})
            await reply(writer, "502 Bad Gateway", f"Could not reach {host}:{port}\n")
            return
        writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        await writer.drain()
        await asyncio.gather(pipe(reader, up_writer), pipe(up_reader, writer))

    return handle


async def start(rules_provider, mode="enforce", allowed_ports=ALLOWED_PORTS_DEFAULT, log_path=None, host="0.0.0.0", port=3128):
    handler = make_handler(rules_provider, mode, allowed_ports, log_path)
    return await asyncio.start_server(handler, host, port)


def main() -> int:
    mode = os.environ.get("EGRESS_MODE", "enforce")
    if mode not in ("enforce", "learn"):
        print(f"EGRESS_MODE must be enforce or learn, not {mode!r}", file=sys.stderr)
        return 2
    allow_file = Path(os.environ.get("EGRESS_ALLOW_FILE", "/workspace/config/egress-allow-list.txt"))
    log_path = os.environ.get("EGRESS_LOG", "/logs/egress-proxy-log.jsonl")
    port = int(os.environ.get("EGRESS_PORT", "3128"))

    def rules_provider() -> list[str]:
        return load_rules(allow_file.read_text(encoding="utf-8")) if allow_file.exists() else []

    async def run():
        server = await start(rules_provider, mode=mode, log_path=log_path, port=port)
        write_log(log_path, {"decision": "started", "host": "", "port": port, "mode": mode, "client": "",
                             "reason": f"allow-list file: {allow_file}"})
        async with server:
            await server.serve_forever()

    asyncio.run(run())
    return 0


if __name__ == "__main__":
    sys.exit(main())
