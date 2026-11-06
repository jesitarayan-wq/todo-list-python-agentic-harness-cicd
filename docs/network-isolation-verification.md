# Network isolation: restricted mode and its verification (2026-11-06)

Agent containers can run in two network modes, chosen with the environment variable `AGENT_NETWORK` in `scripts/run-agent.sh`.

| Mode | How it works | Default |
| --- | --- | --- |
| `open` | Docker's default network, with the application ports published | Yes |
| `restricted` | The container joins the Docker network `agent-internal`, which has no route to the internet. All HTTPS goes through an allow-list proxy that logs every decision | No, opt-in |

## How to use it

```
./scripts/start-egress-proxy.sh enforce
AGENT_NETWORK=restricted ./scripts/run-agent.sh security-reviewer bash
./scripts/start-egress-proxy.sh stop
```

`./scripts/start-egress-proxy.sh learn` allows every HTTPS host and logs it, to discover what an agent needs. `config/egress-allow-list.txt` lists the allowed hosts, one per line. Restricted mode refuses to start if the proxy is not running.

## What was built

- `scripts/egress_proxy.py`: a proxy that tunnels HTTPS (CONNECT) on port 443 only, to hosts on the allow-list; it refuses other hosts, other ports and plain HTTP, and writes one JSON line per decision to `logs/egress-proxy-log.jsonl`.
- `scripts/start-egress-proxy.sh`: starts the proxy on the default network and on `agent-internal`. It is the only container attached to both.
- `scripts/run-agent.sh`: the `AGENT_NETWORK` setting. The role and workspace rules are unchanged.
- `eval/test_egress_proxy.py` and `eval/test_network_modes.py`: 17 tests (the matcher, the proxy over local sockets, and static checks of the script). With the existing checks, 84 tests pass.

## Evidence

Building block: a container on `agent-internal` cannot reach the internet. `curl https://example.com` gave `Could not resolve host`, exit 6. The same command on the default network gave `200`.

Learn mode: a security-reviewer session in restricted mode (the prompt "Reply with the single word ready", no tools, workspace read-only, 0 lines changed; cost $0.1307, 1 s API time, 1 m 54 s wall time) made 68 requests through the proxy, plus 1 from a curl test:

| Host | Requests | Probable purpose |
| --- | --- | --- |
| `api.anthropic.com` | 43 | The model API |
| `registry.npmjs.org` | 13 | Update check |
| `http-intake.logs.us5.datadoghq.com` | 6 | Telemetry |
| `downloads.claude.ai` | 2 | Update download |
| `platform.claude.com`, `mcp-proxy.anthropic.com`, `api.github.com`, `raw.githubusercontent.com` | 1 each | Login, hosted connectors, update and plugin lookups |

The purposes are read from the host names and were not verified.

Enforce mode, with only `api.anthropic.com` and `platform.claude.com` on the allow-list: the same session worked (cost $0.0771, 2 s API time, 32 s wall time, 0 lines changed). The proxy allowed 40 requests to `api.anthropic.com` and refused 10: 4 to the telemetry host, and 1 each to `api.github.com`, `github.com`, `raw.githubusercontent.com`, `registry.npmjs.org`, `downloads.claude.ai` and `mcp-proxy.anthropic.com`.

Refusal demonstration, from a throwaway container on `agent-internal`:

| Request | Result |
| --- | --- |
| `https://example.com` through the proxy | `curl: (56) CONNECT tunnel failed, response 403`, exit 56; the log records `denied`, reason `not on the allow-list` |
| `https://example.com` with no proxy | `curl: (6) Could not resolve host: example.com`, exit 6 |
| `https://api.anthropic.com` through the proxy | HTTP `404`, exit 0: the tunnel works; the log records `allowed` |

The learn-mode log is kept in `logs/` on the author's machine and was not committed.

## Limits

- Restricted mode is opt-in. The default stays `open`, so the documented commands and the published application ports work as before.
- It was tested with one role (security-reviewer) and a one-word prompt. A longer session that uses tools was not run in restricted mode, so a host that only a longer session needs would show up as a refusal in the log.
- `platform.claude.com` is on the allow-list because it appeared in the learn-mode session. The enforce-mode session did not use it, so whether it is needed was not tested.
- Only HTTPS is tunnelled. Plain HTTP and other ports are refused, and the local MCP servers use standard input and output, so they are not affected.
- The proxy log is a plain file in `logs/`; it is not tamper-proof.
