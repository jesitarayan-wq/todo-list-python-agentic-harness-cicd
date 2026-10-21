# Enforcement Verification

Role: dependency-auditor (read-only, no storage, retrieval at internal). Run on 2026-10-21.

## Layer 1: Container Permissions
**Role:** dependency-auditor
**Launch line:** `Launching 'dependency-auditor': image=todo-agent-m4, workspace=ro, memory=omitted`

**Workspace check**
**Command:** touch /workspace/should-fail.txt
**Output:** touch: cannot touch '/workspace/should-fail.txt': Read-only file system

**Memory volume check**
**Command:** grep ' /memory ' /proc/mounts || echo "OK: /memory is not mounted"
**Output:** OK: /memory is not mounted

**Host check:** `ls should-fail.txt` -> No such file or directory
**Result:** blocked as expected

## Layer 2: MCP Server Allow-Lists

**Denied operation check**
**Command:** npx --yes @modelcontextprotocol/inspector --cli -e AGENT_ROLE=dependency-auditor python3 mcp-servers/storage/server.py --method tools/call --tool-name write_entry --tool-arg key=probe --tool-arg value=denied
**Output:** authorization_denied: role 'dependency-auditor' may not call 'write_entry'. See docs/governance-policy.md. (isError: true)

**Granted operation check**
**Command:** npx --yes @modelcontextprotocol/inspector --cli -e AGENT_ROLE=dependency-auditor python3 mcp-servers/retrieval/server.py --method tools/call --tool-name retrieve --tool-arg query="architecture notes"
**Output:** isError false; returned "Internal architecture notes" (internal) and "Public README" (public). No confidential document.

**Classification ceiling check**
**Command:** same retrieve call with --tool-arg query="design specification"
**Output:** "result": [] (isError false)

**Audit log tail:**
- logs/storage-audit-log.jsonl: {"timestamp": "2026-10-21T17:08:34.333065+00:00", "event": "authorization_denied", "operation": "write_entry", "role": "dependency-auditor", ...}
- logs/retrieval-audit-log.jsonl: {"timestamp": "2026-10-21T17:08:36.589564+00:00", "event": "classification_withheld", "operation": "retrieve", "role": "dependency-auditor", "detail": "1 result(s) above the 'internal' ceiling were withheld", ...}
- A successful retrieval writes no log line (the server logs denials and withholdings only).

## Policy test suite
**Command:** python3 -m pytest eval/test_policy.py -q
**Output:** 35 passed in 0.20s (8 roles; the dependency-auditor is included in every per-role check)
