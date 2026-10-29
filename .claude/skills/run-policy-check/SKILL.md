---
name: run-policy-check
description: Run the governance policy test suite and report which role or artifact disagrees with docs/governance-policy.md. Use after any change to the policy, allow-lists, skills or scripts/run-agent.sh.
version: 0.1.0
---

# run-policy-check

1. Run: python3 -m pytest eval/test_policy.py -q
2. If all tests pass, report the pass count.
3. If any fail, name the failing role or skill and show both sides (policy vs file) from the assertion message.
4. Do not edit the policy and the artifact together to hide a mismatch. Report which side looks authoritative and ask a human.

## Activation Scope
Permitted roles: orchestrator
Denied roles: implementer, planner, security-reviewer, tester, project-manager, test-coverage-analyzer, dependency-auditor
