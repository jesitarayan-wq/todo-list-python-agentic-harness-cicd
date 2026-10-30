# ADR-005: Score rubrics with a per-dimension floor

## Status
Accepted

## Context
Agent output is scored on several dimensions (docs/rubric.md, rubric-security.md, rubric-linter.md). A total score can hide one serious weakness.

## Decision
Require every dimension to score 3 or higher, in addition to any total.

## Alternatives considered
- Aggregate minimum only. Rejected: docs/rubric-linter.md says it would let a report with strong explanations but incomplete grouping pass. Evidence: docs/iteration-log-security.md line 16 records a run totalling 18/20 that FAILED because Severity Classification Accuracy was below the floor, despite a strong overall review; the fixed run scored 20/20 (line 46).
- No numeric rubric. Rejected: scores could not be compared across runs (docs/baseline-measurements.md).

## Consequences
A single weak dimension fails a run. Cost: stricter, so more iterations are needed.

## Evidence
docs/iteration-log-security.md lines 16 and 46; docs/rubric-security.md line 81; docs/rubric-linter.md lines 53 and 57.

## Open risks
Rubric scores are agent-judged and the AI rubric has not run in CI (no API key).
