# Capstone reference
Project: todo-list-python (Flask + MongoDB) with a governed 8-role agent harness. Repo jesitarayan-wq/todo-list-python-agentic-harness-cicd, main b6f1862, image todo-agent-m4.
Roles: planner, implementer, security-reviewer, tester, project-manager, test-coverage-analyzer, orchestrator, dependency-auditor.
Layers: policy -> run-agent.sh containers -> MCP allow-lists -> eval/test_policy.py (35) -> red-team -> CI (6 jobs + audit trail) -> ruleset protect-main (3 required checks) -> deterministic handoff check (15 tests).
Evidence: name-mismatch calibration fix 280f176; gate proofs (policy red, integrity CI #13); handoff check ~0.18s identical x3, zero tokens.
Gaps: no API key; eval gate replays HO-01; skill scope prompt-only; tester placeholder PASS; orchestrator no shell tool; ADR-003 Proposed; .mcp.json points at old mcp/; image has stale allow-lists; integrity script editable in a PR; 7 bypass merges.
Rules: names must match everywhere; refusal without log is unverified; fix the lock not the test; deterministic is not correct; never invent numbers; commit/push from Git Bash.
