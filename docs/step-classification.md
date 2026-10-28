# Step Classification

This document is updated after every calibration cycle. Steps that cross the stability threshold are promoted to candidate status. A step that has been a candidate for more than two calibration cycles without meeting all four signals is reviewed for re-scoping.

Updated 2026-10-29 for todo-list-python. Evidence is this project's own. Categories: strong candidate, weak candidate, not a candidate, already deterministic.

## Step: Handoff field check
- Status: converted to deterministic code (ADR-003, 2026-10-22). ADR-003 is Proposed, not Accepted: the full end-to-end run was not possible.
- Stability: not measured. One calibration cycle exists (docs/calibration-log.md, Cycle 1).
- Repeatability: script output identical on three runs (0.193s, 0.170s, 0.175s).
- Specifiability: task_id, role, summary, and a non-empty modified_files list with a path and description per item.
- Run rate: every implementer handoff.
- Preserved edge case: present-but-whitespace values are rejected (eval/test_deterministic_step.py).
- Recommendation: weak candidate, converted. To qualify as strong: a second calibration cycle with consistent scores, and three repeat runs of an agent version.
- Next review: 2026-11-26.

## Step: Run-record writing
- Stability: not stable. The agent self-report was not written in 3 of 7 holdout runs.
- Specifiability: yes. Fixed record format.
- Edge case: a session that exits before the record is written.
- Recommendation: weak candidate. Needs a hook or script and a measured baseline.
- Candidate since: 2026-10-20. Next review: 2026-11-19.

## Step: Planner, implementer, security-reviewer
- Recommendation: not a candidate. Needs judgment and synthesis; output not specifiable in advance.
- Edge case: none identified.
- Next review: 2027-01-29.

## Step: Classification, role and ceiling checks in the MCP servers
- Recommendation: already deterministic (allow-list lookups in mcp-servers/*/server.py).
- Edge case: none identified.

## Step: Closing a ticket when the tester result is unverified
- Recommendation: not a candidate. A human confirms, because test_runner returns placeholder PASS output.
- Next review: 2027-01-29.
