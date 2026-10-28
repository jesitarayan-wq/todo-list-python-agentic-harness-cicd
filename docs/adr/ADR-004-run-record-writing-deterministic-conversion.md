# ADR-004: Convert run-record writing from agent self-report to deterministic code

## Status
Proposed

## Context
The orchestrator session writes the run record that the harness reads. In 3 of 7 holdout runs (HO-04, HO-06, HO-07) the session ended before the record was written and it had to be rebuilt from on-screen notices. The format is fixed, but the facts come from subagent output the session cannot always see.

## Decision
Replace agent-written run records with a script that builds the record from captured facts and marks missing values as null.

## Alternatives considered
- Keep the agent self-report. Rejected: it failed in 3 of 7 runs and tool-call details were only self-reported.
- Ask the agent to write the record sooner, with a stricter prompt. Rejected: this does not fix the cause, which is a session ending before the write.
- Convert to code. Preferred, but only if the facts can be captured outside the agent, for example from server audit logs.

## Consequences
Expected: records are always written, and are repeatable and cheap. Trade-off: a script can only record what it is given, so it may produce thinner records. Nothing is measured yet.

## Evidence
To gather: a second calibration cycle, three repeat runs, and the measurements in step-classification.md. Existing: the 3 of 7 failures in docs/calibration-log.md (Holdout measurement 1).
