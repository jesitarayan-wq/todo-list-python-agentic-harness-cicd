# Step Classification

Updated 2026-10-22 for todo-list-python. Evidence below is this project's own.

## Step: Handoff field check
- Status: converted to deterministic code (ADR-003).
- Stability: not measured. Only one calibration cycle exists (docs/calibration-log.md, Cycle 1), so the two-cycle signal is not met. Converted anyway because the rule is fully specifiable.
- Repeatability: the script gave identical output on three runs of the same input.
- Specifiability: an implementer handoff must have task_id, role, summary and a non-empty modified_files list; each item needs a non-empty path and description.
- Run rate: every implementer handoff.
- Preserved edge case: present-but-empty values are rejected (covered by eval/test_deterministic_step.py).
- Recommendation: converted.

## Step: Run-record writing
- Recommendation: candidate. The agent self-report failed to be written in 3 of 7 holdout runs. Not yet converted.

## Step: Planner, implementer, security-reviewer
- Recommendation: keep as agents. They need judgment and synthesis; the correct output is not specifiable in advance.

## Step: Closing a ticket when the tester result is unverified
- Recommendation: human. The tester's test_runner returns placeholder PASS output, so a person should confirm.
