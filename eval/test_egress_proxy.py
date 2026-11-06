"""Tests for scripts/egress_proxy.py: the allow-list matcher and the proxy itself (local sockets only)."""
import asyncio
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("egress_under_test", ROOT / "scripts" / "egress_proxy.py")
PROXY = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PROXY)


def test_rules_ignore_comments_and_blank_lines():
    rules = PROXY.load_rules("# a comment\n\nAPI.Example.com  # trailing\n*.Foo.org\n")
    assert rules == ["api.example.com", "*.foo.org"]


def test_exact_and_wildcard_matching():
    rules = ["api.anthropic.com", "*.example.org"]
    assert PROXY.host_allowed("api.anthropic.com", rules)
    assert PROXY.host_allowed("API.ANTHROPIC.COM.", rules)
    assert PROXY.host_allowed("a.b.example.org", rules)
    assert not PROXY.host_allowed("example.org", rules)
    assert not PROXY.host_allowed("evilexample.org", rules)
    assert not PROXY.host_allowed("api.anthropic.com.evil.net", rules)
    assert not PROXY.host_allowed("", rules)


def test_connect_line_parsing():
    assert PROXY.parse_connect("CONNECT api.anthropic.com:443 HTTP/1.1") == ("api.anthropic.com", 443)
    assert PROXY.parse_connect("GET http://example.com/ HTTP/1.1") is None
    assert PROXY.parse_connect("CONNECT example.com HTTP/1.1") is None
    assert PROXY.parse_connect("CONNECT [::1]:443 HTTP/1.1") is None
    assert PROXY.parse_connect("CONNECT host:notaport HTTP/1.1") is None


def test_decisions():
    ports = PROXY.ALLOWED_PORTS_DEFAULT
    assert PROXY.decide("api.anthropic.com", 443, ["api.anthropic.com"], "enforce", ports)[0] == "allowed"
    assert PROXY.decide("example.com", 443, ["api.anthropic.com"], "enforce", ports)[0] == "denied"
    assert PROXY.decide("api.anthropic.com", 22, ["api.anthropic.com"], "enforce", ports)[0] == "denied"
    assert PROXY.decide("example.com", 443, [], "learn", ports)[0] == "allowed"
    assert PROXY.decide("example.com", 22, [], "learn", ports)[0] == "denied"


async def _read_head(reader):
    return (await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), 5)).decode("latin-1")


async def _echo_server():
    async def echo(reader, writer):
        data = await reader.read(100)
        writer.write(b"echo:" + data)
        await writer.drain()
        writer.close()
    server = await asyncio.start_server(echo, "127.0.0.1", 0)
    return server, server.sockets[0].getsockname()[1]


async def _scenario(tmp_path, rules, mode, request_lines, allowed_ports_from_upstream=True):
    upstream, upstream_port = await _echo_server()
    log_path = tmp_path / "proxy-log.jsonl"
    ports = frozenset({upstream_port}) if allowed_ports_from_upstream else frozenset({443})
    proxy = await PROXY.start(lambda: rules, mode=mode, allowed_ports=ports, log_path=str(log_path), host="127.0.0.1", port=0)
    proxy_port = proxy.sockets[0].getsockname()[1]
    results = []
    for line in request_lines(upstream_port):
        reader, writer = await asyncio.open_connection("127.0.0.1", proxy_port)
        writer.write(line.encode() + b"\r\nHost: x\r\n\r\n")
        await writer.drain()
        head = await _read_head(reader)
        extra = b""
        if head.startswith("HTTP/1.1 200"):
            writer.write(b"hello")
            await writer.drain()
            extra = await asyncio.wait_for(reader.read(100), 5)
        results.append((head, extra))
        writer.close()
    proxy.close()
    upstream.close()
    await proxy.wait_closed()
    entries = [json.loads(x) for x in log_path.read_text().splitlines()] if log_path.exists() else []
    return results, entries


def run_scenario(tmp_path, rules, mode, request_lines, **kwargs):
    return asyncio.run(_scenario(tmp_path, rules, mode, request_lines, **kwargs))


def test_an_allowed_host_is_tunnelled_and_logged(tmp_path):
    results, entries = run_scenario(tmp_path, ["127.0.0.1"], "enforce", lambda p: [f"CONNECT 127.0.0.1:{p} HTTP/1.1"])
    head, extra = results[0]
    assert head.startswith("HTTP/1.1 200")
    assert extra == b"echo:hello"
    assert entries[0]["decision"] == "allowed" and entries[0]["host"] == "127.0.0.1"


def test_a_host_not_on_the_list_is_refused_and_logged(tmp_path):
    results, entries = run_scenario(tmp_path, ["api.anthropic.com"], "enforce", lambda p: [f"CONNECT 127.0.0.1:{p} HTTP/1.1"])
    assert results[0][0].startswith("HTTP/1.1 403")
    assert entries[0]["decision"] == "denied" and entries[0]["reason"] == "not on the allow-list"


def test_a_port_that_is_not_allowed_is_refused(tmp_path):
    results, entries = run_scenario(tmp_path, ["127.0.0.1"], "enforce", lambda p: ["CONNECT 127.0.0.1:22 HTTP/1.1"])
    assert results[0][0].startswith("HTTP/1.1 403")
    assert entries[0]["reason"] == "port not allowed"


def test_plain_http_requests_are_refused(tmp_path):
    results, entries = run_scenario(tmp_path, ["127.0.0.1"], "enforce", lambda p: ["GET http://127.0.0.1/ HTTP/1.1"])
    assert results[0][0].startswith("HTTP/1.1 403")
    assert "only HTTPS tunnels" in entries[0]["reason"]


def test_learn_mode_allows_and_logs_any_host(tmp_path):
    results, entries = run_scenario(tmp_path, [], "learn", lambda p: [f"CONNECT 127.0.0.1:{p} HTTP/1.1"])
    assert results[0][0].startswith("HTTP/1.1 200")
    assert entries[0]["decision"] == "allowed" and entries[0]["mode"] == "learn"
