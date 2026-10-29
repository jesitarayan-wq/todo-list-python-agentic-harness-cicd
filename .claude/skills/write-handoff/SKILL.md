---
name: write-handoff
description: Write the implementer-to-orchestrator handoff as JSON matching schemas/handoff.json, then validate it with scripts/validate_handoff_deterministic.py. Use after the implementer finishes a change.
version: 0.1.0
---

# write-handoff

1. Collect: task_id, role, a one-sentence summary, and every modified file with a short description of the change.
2. Write handoff.json with fields task_id, role, summary, modified_files (list of objects with path and description), and lesson_entry_id if a lesson was recorded.
3. Validate: python3 scripts/validate_handoff_deterministic.py --input handoff.json --output result.json
4. If result.json says "valid": false, fix the listed problems and validate again. Never leave a description empty.
5. Report the validation result. Do not invent files or descriptions.

## Activation Scope
Permitted roles: implementer
Denied roles: orchestrator, planner, security-reviewer, tester, project-manager, test-coverage-analyzer, dependency-auditor
