# Runbook: todo-list-python governed harness

## Start and stop
- Build: docker build -t todo-agent-m4 . (about 5 to 15 minutes the first time)
- Start a role container: ./scripts/run-agent.sh <role> bash (read-only or read-write per docs/governance-policy.md)
- Stop: type exit on its own line.
- Rule: run git commit and git push on the host shell (Git Bash), never inside a container; the container has no saved GitHub login.

## Health check
In a container: cd /workspace && python3 -m pytest eval/test_policy.py eval/test_deterministic_step.py -q
Expected: 52 passed (37 policy + 15 handoff-validator tests).

## Incident handling (details: docs/failure-mode-playbook.md)
- A role is blocked or ungoverned: compare role names across the agent file, grant map and allow-lists (NM-1); run eval/test_policy.py.
- Policy and config disagree: change one side only, then rerun the policy tests (see docs/tool-evolution-drill.md).
- A gate looks weakened (for example continue-on-error on policy-gate): the Pipeline Integrity Check job fails; revert the workflow change.
- Memory problems (stale entry, scope leak, credential pattern): follow the memory entries in the playbook; the pre-commit hook blocks credential patterns in .memory/.

## Escalation and rollback
- Escalate: the orchestrator halts and escalates to a human if the same phase fails its gate twice in a row.
- Restore a config file: git checkout <file>.
- Undo the handoff-check wiring: git revert 97aaa2e (single integration commit, ADR-003).
- Direct pushes to main are rejected by ruleset protect-main (3 required checks); changes go through a branch.

## Audit and logs
- MCP audit logs: logs/storage-audit-log.jsonl and logs/retrieval-audit-log.jsonl (format: docs/audit-log-template.md).
- CI audit trail: ci-audit-trail-<sha>.json artifact on each CI run (job results, harness and integrity results).
- Not yet logged: human approvals, retries, rollbacks, MCP denials in the CI trail.

## Cost and reliability controls
See docs/reliability-and-cost-controls.md (implemented versus planned).

## Known limits
No live end-to-end run and no API key, so the AI review and rubric have never run. Skill scope is not a runtime lock. The tester's test_runner returns placeholder PASS output.
