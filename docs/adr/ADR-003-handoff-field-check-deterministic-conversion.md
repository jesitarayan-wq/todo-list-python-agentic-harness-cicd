# ADR-003: Convert the handoff field check from agent convention to deterministic code

## Status
Accepted

## Context
Agent handoffs (implementer to orchestrator) were a convention in the agent prompts: a list of modified files, a description of each change, and any lesson entry_id. Nothing checked them. HO-04 probed this "output format mismatch" risk, and its referenced handoff spec file never existed. The rule can be written exactly.

## Decision
Check each handoff with scripts/validate_handoff_deterministic.py against schemas/handoff.json. Required: task_id, role, summary, and modified_files (a non-empty list whose items each have a non-empty path and description). Invalid handoffs exit 1 with a list of problems.

## Alternatives considered
- Keep it as an agent convention. Rejected: no check, variance, and governance overhead for a fixed rule.
- Ask an agent to validate. Not measured here, so no figures are claimed. Qualitatively it adds token cost and inference latency to a step with no ambiguity.
- Convert to code. Accepted.

## Consequences
Measured: the script took 0.193s, 0.170s and 0.175s over three runs on the same input, with identical output each time, no token cost, and the 7 existing step tests still pass. Trade-off: the result is a terse problem list, not prose. Limits: stability was not measured (one calibration cycle), and no agent baseline was measured.

## Evidence
- docs/step-classification.md
- examples/handoff_good.json (valid, exit 0) and examples/handoff_bad.json (empty description, exit 1)
- eval/test_deterministic_step.py: 7 passed
