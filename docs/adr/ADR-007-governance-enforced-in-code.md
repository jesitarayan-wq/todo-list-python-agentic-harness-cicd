# ADR-007: Enforce governance in code, not only in a policy document

## Status
Accepted

## Context
docs/governance-policy.md defines per-role grants. In Cycle 1 (docs/calibration-log.md) the allow-list named "reviewer" while the agent was "security-reviewer", so the reviewer was blocked from reading files while the old harness still passed.

## Decision
Enforce policy through run-agent.sh container permissions, MCP allow-lists with audit logs, eval/test_policy.py (37 checks), and CI required checks.

## Alternatives considered
- Policy document alone. Rejected: the name mismatch above went undetected by a passing suite.
- Prompt instructions alone. Rejected: red-team Prompts 1 and 5 were refused by the agent itself, not by a lock (eval/red-team-results.md), and skill scope has no runtime lock.
- Enforce only in CI. Rejected: it would not stop a local run.

## Consequences
Policy, files and tests must stay in agreement; the tool-evolution drill (docs/tool-evolution-drill.md) shows a revoked permission caught by test_storage_allowlist_matches_policy[implementer].

## Evidence
docs/calibration-log.md; eval/red-team-results.md; docs/tool-evolution-drill.md; CI gate runs on gate-test and integrity-test branches.

## Open risks
Skill scope is not a runtime lock; the AI review has never run.
