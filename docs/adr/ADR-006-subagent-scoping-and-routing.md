# ADR-006: Scope each subagent to the minimum tools and give one role per sensitive tool

## Status
Accepted

## Context
A single agent that plans, codes, tests and closes tickets can mark work done when tests failed, and the failing stage cannot be found. See docs/orchestration-diagram.md and docs/routing-and-tool-grant-map.md.

## Decision
Use an orchestrator with scoped subagents; each tool has the fewest roles possible, and the ticket tool belongs only to the project-manager.

## Alternatives considered
- Give the Security Reviewer the test runner. Rejected: the Tester owns test execution, and two roles could each claim or disclaim a failing test (docs/routing-and-tool-grant-map.md, Alternatives Considered).
- Give the Implementer the task tracker. Rejected: it would put the ticket tool in the Implementer's context and let it move tickets outside its job (same file).
- One agent for everything. Rejected: the motivating failure above.

## Consequences
More handoffs; clearer failure location. The tester's test_runner is a placeholder, so test results are unverified.

## Evidence
docs/routing-and-tool-grant-map.md; docs/calibration-log.md Cycle 1.

## Open risks
No live end-to-end run has exercised the full routing.
