# Step Classification

Updated 2026-10-22 for todo-list-python. Evidence is this project's own. Categories: strong candidate, weak candidate, not a candidate, already deterministic.

## Step: Handoff field check
- Stability: not measured. Only one calibration cycle exists (docs/calibration-log.md, Cycle 1), and holdout scores varied.
- Repeatability: the deterministic script gave identical output on three runs (0.193s, 0.170s, 0.175s). The agent version was never run three times.
- Specifiability: an implementer handoff needs task_id, role, summary and a non-empty modified_files list; each item needs a non-empty path and description.
- Run rate: every implementer handoff.
- Edge case the deterministic version must preserve: a description that is present but whitespace-only. It is rejected (tested in eval/test_deterministic_step.py).
- Recommendation: weak candidate. Already converted as ADR-003. To qualify as a strong candidate: a second calibration cycle with consistent harness scores, and three repeat runs of the agent version compared with diff.

## Step: Run-record writing
- Stability: not stable. The agent self-report was not written in 3 of 7 holdout runs.
- Repeatability: not repeatable.
- Specifiability: yes. The record format is fixed.
- Run rate: every run.
- Edge case: a session that exits before the record is written. Code must still produce a record from available facts.
- Recommendation: weak candidate. Needs a hook or script that writes the record, and a measured baseline.

## Step: Planner, implementer, security-reviewer
- Stability, repeatability: not measured.
- Specifiability: no. The correct output is not known in advance.
- Run rate: per task.
- Edge case: none identified, because these are kept as agents.
- Recommendation: not a candidate. They need judgment and synthesis.

## Step: Classification, role and ceiling checks in the MCP servers
- Recommendation: already deterministic. Allow-list lookups in mcp-servers/*/server.py.
- Edge case: none identified.

## Step: Closing a ticket when the tester result is unverified
- Recommendation: not a candidate. A human should confirm, because test_runner returns placeholder PASS output.
- Edge case: none identified.
