# todo-list-python: a governed multi-agent engineering harness

A Flask + MongoDB to-do API (`todo.py`, `task.py`) wrapped in an 8-role agent harness with least-privilege governance, enforced in code, and CI gates. Built across a 4-module agentic engineering course; evidence for each module is in `docs/`.

## Roles (`.claude/agents/`)
planner, implementer, security-reviewer, tester, project-manager, test-coverage-analyzer, orchestrator, dependency-auditor.
Own skills (`.claude/skills/`, v0.1.0): `write-handoff`, `run-policy-check`.

## Prerequisites
- Docker Desktop (running; `docker version` must show a Server section)
- Git Bash on Windows (or any bash)
- Optional: an Anthropic/OpenRouter key for live agent runs (not needed for the policy tests)

## Run it
1. Build the image (first build takes about 5 to 15 minutes): `docker build -t todo-agent-m4 .`
2. Start a role container: `./scripts/run-agent.sh orchestrator bash`
3. Inside the container run: `cd /workspace && python3 -m pytest eval/test_policy.py eval/test_deterministic_step.py -q` (expected: 52 passed, 37 policy + 15 handoff-validator tests)
4. Try a governance lock: `./scripts/run-agent.sh security-reviewer bash`, then `touch /workspace/x` gives "Read-only file system".

Run `git commit` and `git push` from the host shell, not inside a container.

## Repo map
- `docs/governance-policy.md`: per-role policy
- `scripts/run-agent.sh`: per-role container permissions
- `mcp-servers/*/allow-list.json`: per-operation role checks and classification ceilings
- `eval/`: policy tests, harness, red-team prompts and results
- `.github/workflows/ci.yml`: classifier, policy gate, governed-file check, eval gate, integrity check, advisory review, audit trail
- `schemas/handoff.json`, `scripts/validate_handoff_deterministic.py`: deterministic handoff check (ADR-003)
- `docs/adr/`: ADR-003 and ADR-004 (both Proposed)
- `docs/calibration-log.md`, `docs/baseline-measurements.md`, `docs/step-classification.md`

## Honest limits
- No live end-to-end orchestration run; the orchestrator has no shell tool and `eval/orchestrator.py` is a course simulation.
- No API key was registered, so the AI review and rubric have never run.
- The eval gate replays one saved transcript (HO-01).
- Skill scope is enforced by instruction plus a policy test, not by a runtime lock.
- The tester's `test_runner` returns placeholder PASS output.
- This is a fork: PRs on the GitHub UI can default to the parent repo, so check the base repository.
