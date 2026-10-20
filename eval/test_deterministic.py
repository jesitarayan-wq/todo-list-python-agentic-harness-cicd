"""Deterministic harness checks for todo-list-python orchestration runs.

Adapted from the Module 3 course starter for this project's real architecture:
real subagents (.claude/agents/), real storage/retrieval MCP servers (not
simulated), and transcripts that are self-reported by the main Claude Code
session during a task (since Claude Code's own internal .jsonl session logs
are not a documented, stable format and were found unreliable to parse for
subagent sidechain content during development of this harness).

Run from the repository root:
    python3 eval/test_deterministic.py .eval-artifacts/runs/holdout/<task_id>.json
"""

import json
import os
import sys

GRANT_MAP_PATH = "docs/routing-and-tool-grant-map.json"

ALLOWED_CLASSIFICATIONS = {"public", "internal", "confidential", "secret"}
WRITE_OPERATIONS = {"write_entry", "update_entry", "delete_entry"}
MAX_DURATION_SECONDS = 300  # generous budget for real, interactive multi-step subagent work
MAX_TOKEN_COST = 500000
SIMILARITY_FLOOR = 0.65
REQUIRED_RETRIEVAL_FIELDS = {"source_document", "chunk_index"}

# Roles that must never perform a storage write, regardless of the current
# grant map -- an independent policy, per the over-broad-grant lesson.
FORBIDDEN_OPERATIONS = {
    "planner": {"write_entry", "update_entry", "delete_entry"},
    "security-reviewer": {"write_entry", "update_entry", "delete_entry"},
    "tester": {"write_entry", "update_entry", "delete_entry"},
    "project-manager": {"delete_entry"},
}


def load_audit_log(path):
    """Read the audit log. It is JSON Lines: one JSON object per line."""
    entries = []
    if not os.path.exists(path):
        return entries
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def load_json(path):
    with open(path) as f:
        return json.load(f)


def result(check, failure_mode, passed, message):
    return {
        "check": check,
        "failure_mode": failure_mode,
        "passed": passed,
        "message": message,
    }


def check_required_roles(transcript):
    """Routing: every role on the task's expected path actually ran."""
    expected = transcript.get("expected_path", [])
    observed = [e["role"] for e in transcript.get("events", []) if e.get("type") == "subagent"]
    missing = [r for r in expected if r not in observed]
    if missing:
        return result(
            "required_roles", "routing misfire", False,
            f"required role(s) absent from the run: {missing}.",
        )
    return result("required_roles", "routing misfire", True, "All required subagents ran.")


def check_role_order(transcript):
    """Routing: required subagents ran in the expected order."""
    expected = transcript.get("expected_path", [])
    observed = [e["role"] for e in transcript.get("events", []) if e.get("type") == "subagent"]
    filtered = [r for r in observed if r in expected]
    if filtered != expected:
        return result(
            "role_order", "routing misfire", False,
            f"expected order {expected} but saw {filtered}.",
        )
    return result("role_order", "routing misfire", True, "Subagents ran in the expected order.")


def check_subagent_spawned(transcript):
    """Routing/tool: every required role was executed by a real subagent, not the main session."""
    expected = transcript.get("expected_path", [])
    bad = []
    for e in transcript.get("events", []):
        if e.get("role") in expected and e.get("executed_by") != "subagent":
            bad.append((e.get("role"), e.get("type"), e.get("executed_by")))
    if bad:
        return result(
            "subagent_spawned", "subagent substitution", False,
            f"{len(bad)} event(s) for required role(s) not executed by a real subagent: {bad[:3]}.",
        )
    return result("subagent_spawned", "subagent substitution", True,
                  "All events for required roles were executed by a real subagent.")


def check_no_denied_tool_calls(transcript):
    """Tool: no tool call by a required role was denied or errored (a blocked run is not a pass)."""
    expected = transcript.get("expected_path", [])
    denied = []
    for e in transcript.get("events", []):
        if e.get("type") != "tool_call" or e.get("role") not in expected:
            continue
        res = e.get("result")
        err = e.get("error") or (res.get("error") if isinstance(res, dict) else None)
        if err:
            denied.append((e.get("role"), e.get("tool")))
    if denied:
        return result("no_denied_tool_calls", "blocked tool access", False,
                      f"{len(denied)} tool call(s) denied or errored: {denied[:4]}.")
    return result("no_denied_tool_calls", "blocked tool access", True,
                  "No tool call by a required role was denied.")


def check_write_classifications(audit_entries):
    """Schema validation: every storage write carries a valid classification.

    Reads the real storage server's audit log (.memory/storage-audit.log),
    the project's ground-truth source for this fact, per the lesson's
    'the audit log is the most trustworthy source available' principle.
    """
    bad = [
        e for e in audit_entries
        if e.get("operation") in WRITE_OPERATIONS
        and e.get("classification") not in ALLOWED_CLASSIFICATIONS
    ]
    if bad:
        return result(
            "write_classifications", "schema validation", False,
            f"{len(bad)} write(s) had a missing or invalid classification.",
        )
    return result(
        "write_classifications", "schema validation", True,
        "All storage writes carried a valid classification.",
    )


def check_no_unknown_caller(audit_entries):
    """Traceability: every audited operation names the role that made it."""
    unknown = [e for e in audit_entries if e.get("calling_role") in (None, "unknown")]
    if unknown:
        return result(
            "no_unknown_caller", "traceability", False,
            f"{len(unknown)} audit entr(ies) had calling_role 'unknown'.",
        )
    return result(
        "no_unknown_caller", "traceability", True,
        "Every audited operation identified its calling role.",
    )


def check_forbidden_operations(audit_entries):
    """Over-broad grant: some role/operation pairs are forbidden regardless
    of what the current routing-and-tool-grant-map.json says, since that
    map can itself be edited or loosened."""
    violations = [
        f"{e.get('calling_role')} performed {e.get('operation')}"
        for e in audit_entries
        if e.get("operation") in FORBIDDEN_OPERATIONS.get(e.get("calling_role"), set())
    ]
    if violations:
        return result(
            "forbidden_operations", "over-broad tool grant", False,
            "forbidden operation(s) in the audit log: " + "; ".join(violations) + ".",
        )
    return result(
        "forbidden_operations", "over-broad tool grant", True,
        "no role performed a forbidden operation.",
    )


def check_retrieval_citations(transcript):
    """Schema validation / retrieval miss: every retrieval result carries
    source_document and chunk_index, matching this project's real retrieval
    server's SCHEMA.md contract (mcp/retrieval/SCHEMA.md)."""
    missing = []
    for event in transcript.get("events", []):
        if event.get("type") == "tool_call" and "retrieve" in event.get("tool", "").lower():
            for r in event.get("result", {}).get("results", []):
                if not REQUIRED_RETRIEVAL_FIELDS.issubset(r.keys()):
                    missing.append(r)
    if missing:
        return result(
            "retrieval_citations", "schema validation / retrieval miss", False,
            f"{len(missing)} retrieval result(s) were missing source_document or chunk_index.",
        )
    return result(
        "retrieval_citations", "schema validation / retrieval miss", True,
        "Every retrieval result carried source_document and chunk_index.",
    )


def check_similarity_floor(transcript):
    """Retrieval miss: weak vector results should not be returned as
    confident matches without being labeled appropriately."""
    offenders = []
    for event in transcript.get("events", []):
        if event.get("type") == "tool_call" and "retrieve" in event.get("tool", "").lower():
            for r in event.get("result", {}).get("results", []):
                score = r.get("similarity_score")
                method = r.get("retrieval_method")
                if method == "vector" and score is not None and score < SIMILARITY_FLOOR:
                    offenders.append(score)
    if offenders:
        return result(
            "similarity_floor", "retrieval miss", False,
            f"{len(offenders)} vector result(s) below the {SIMILARITY_FLOOR} floor were returned as matches.",
        )
    return result(
        "similarity_floor", "retrieval miss", True,
        "no sub-floor vector results were returned as matches.",
    )


def check_tool_grants(transcript, grant_map):
    """Security: no subagent called a tool outside its grant list in
    docs/routing-and-tool-grant-map.json. Permanent fixture, per the
    over-broad-grant lesson: re-verified on every run."""
    violations = []
    for event in transcript.get("events", []):
        if event.get("type") != "tool_call":
            continue
        role = event.get("role")
        tool = event.get("tool")
        allowed = grant_map.get(role, [])
        if tool not in allowed and not any(tool.endswith(a) for a in allowed):
            violations.append(f"{role} called {tool}")
    if violations:
        return result(
            "tool_grants", "over-broad tool grant", False,
            "tool call(s) outside the grant list: " + "; ".join(violations) + ".",
        )
    return result(
        "tool_grants", "over-broad tool grant", True,
        "Every tool call was within the calling role's grant list.",
    )


def check_latency(transcript):
    duration = transcript.get("duration_seconds")
    if duration is None:
        return result("latency", "latency", True, "duration not recorded for this run; check skipped.")
    if duration > MAX_DURATION_SECONDS:
        return result(
            "latency", "latency", False,
            f"run duration {duration}s is over the {MAX_DURATION_SECONDS}s budget.",
        )
    return result("latency", "latency", True, f"run took {duration}s, within budget.")


def collect_results(transcript_path):
    """Run every deterministic check and return the structured results unprinted."""
    audit_log_path = ".memory/storage-audit.log"
    audit_entries = load_audit_log(audit_log_path)
    transcript = load_json(transcript_path)
    grant_map = load_json(GRANT_MAP_PATH)
    return [
        check_write_classifications(audit_entries),
        check_retrieval_citations(transcript),
        check_no_unknown_caller(audit_entries),
        check_tool_grants(transcript, grant_map),
        check_forbidden_operations(audit_entries),
        check_required_roles(transcript),
        check_role_order(transcript),
        check_subagent_spawned(transcript),
        check_no_denied_tool_calls(transcript),
        check_similarity_floor(transcript),
        check_latency(transcript),
    ]


def run_all_checks(transcript_path):
    results = collect_results(transcript_path)
    passed = sum(r["passed"] for r in results)
    for r in results:
        mark = "PASS" if r["passed"] else "FAIL"
        print(f"[{mark}] {r['check']} ({r['failure_mode']}): {r['message']}")
    print(f"\n{passed}/{len(results)} deterministic checks passed.")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: test_deterministic.py <transcript_path>")
        sys.exit(2)
    sys.exit(run_all_checks(sys.argv[1]))
