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
3. Inside the container run: `cd /workspace && python3 -m pytest eval/test_policy.py eval/test_deterministic_step.py eval/test_runner_tool.py -q` (expected: 59 passed, including 7 test-runner tool tests; 37 policy + 15 handoff-validator tests)
4. Try a governance lock: `./scripts/run-agent.sh security-reviewer bash`, then `touch /workspace/x` gives "Read-only file system".

Run `git commit` and `git push` from the host shell, not inside a container.

## Repo map
- `docs/governance-policy.md`: per-role policy
- `scripts/run-agent.sh`: per-role container permissions
- `mcp-servers/*/allow-list.json`: per-operation role checks and classification ceilings
- `eval/`: policy tests, harness, red-team prompts and results
- `.github/workflows/ci.yml`: classifier, policy gate, governed-file check, eval gate, integrity check, advisory review, audit trail
- `schemas/handoff.json`, `scripts/validate_handoff_deterministic.py`: deterministic handoff check (ADR-003)
- `docs/adr/`: ADR-003 to ADR-008 (ADR-003 and ADR-004 Proposed; ADR-005 to ADR-008 Accepted)
- `docs/calibration-log.md`, `docs/baseline-measurements.md`, `docs/step-classification.md`

## Sandbox boundaries and how they were tested

Checked on 2026-11-05 with the image `todo-agent-m4` and `scripts/run-agent.sh`.

### Boundaries

| Boundary | What is set | Limit |
| --- | --- | --- |
| Filesystem | Only the current folder is mounted, at `/workspace`. It is read-only for security-reviewer, planner, test-coverage-analyzer, tester, project-manager and dependency-auditor, and read-write for implementer and orchestrator. No home folder, `/c` or `/Users` is visible | `logs/` is mounted read-write for every role so refusals can be logged. Container-local paths such as `/tmp` stay writable |
| Memory | `.memory/` is mounted only for implementer and orchestrator | |
| Network | The default Docker network. Outbound access is open in the working container, because an agent session must reach Claude. Ports 8501 and 8502 are published | A misbehaving agent could send project files out. An allow-list proxy is the planned fix and is not built yet |
| Credentials | The Claude login lives in a named volume (`claude-auth`), not in the image. `OPENROUTER_API_KEY` is passed through only if set on the host. Slack values default to placeholders | |

### Test 1: parallel sessions are isolated

Two worktrees were created, each with its own marker file, and each was started with its own role through the real run script:

```
git worktree add --detach ~/wt-cap-a
git worktree add --detach ~/wt-cap-b
echo "marker A" > ~/wt-cap-a/MARKER-A.txt
echo "marker B" > ~/wt-cap-b/MARKER-B.txt
cd ~/wt-cap-a && ./scripts/run-agent.sh implementer bash -c 'ls /workspace | grep MARKER; ls /workspace/MARKER-B.txt; ls /wt-cap-b; ls /c /Users'
cd ~/wt-cap-b && ./scripts/run-agent.sh security-reviewer bash -c 'ls /workspace | grep MARKER; ls /workspace/MARKER-A.txt; ls /wt-cap-a; ls /c /Users; touch /workspace/x'
```

| Check | Container A (implementer, `workspace=rw`) | Container B (security-reviewer, `workspace=ro`) |
| --- | --- | --- |
| Own marker | `MARKER-A.txt` listed, content "marker A" | `MARKER-B.txt` listed, content "marker B" |
| Other worktree's marker | No such file or directory | No such file or directory |
| Other worktree's path | `/wt-cap-b` not found | `/wt-cap-a` not found |
| Host drives | `/c` and `/Users` not found | `/c` and `/Users` not found |
| Write attempt | Not tested | `touch: cannot touch '/workspace/x': Read-only file system`, exit 1 |

Each session sees only its own worktree, and the reviewer's write is refused by the container, not by the agent. Not tested: writes from container A to its own worktree, and what two sessions do if mounted on the same folder.

### Test 2: the network

```
docker run --rm --network none --entrypoint python3 todo-agent-m4 -c "import urllib.request; print(urllib.request.urlopen('https://example.com', timeout=8).status)"
docker run --rm --entrypoint python3 todo-agent-m4 -c "import urllib.request; print(urllib.request.urlopen('https://example.com', timeout=8).status)"
```

- With `--network none`: `urllib.error.URLError: <urlopen error [Errno -3] Temporary failure in name resolution>`, exit 1.
- With the default network (the control): `200`, exit 0.

This shows the network can be switched off for checks that do not need it. It does not restrict the working agent container, which still has open outbound access.

### Prerequisite check

- Docker Desktop is running: `docker version` prints both Client and Server.
- The image exists: `docker image ls todo-agent-m4`. If it is missing, build it with `docker build -t todo-agent-m4 .` (about 5 to 15 minutes the first time).

### Troubleshooting

- A path such as `/workspace/...` turns into `C:/Program Files/Git/...` in Git Bash: Git Bash rewrote it. Wrap the command in `bash -c '...'`.
- `git` fails inside a worktree container: the worktree's `.git` file points to a host path. Run git on the host.
- `Temporary failure in name resolution` with `--network none` is expected.

## Honest limits
- One live orchestration run exists (docs/live-run-record.md), but the orchestrator has no shell tool, so the handoff check was run by hand, and `eval/orchestrator.py` is a course simulation.
- No API key was registered, so the AI review and rubric have never run.
- The eval gate replays one saved transcript (HO-01).
- Skill scope is enforced by instruction plus a policy test, not by a runtime lock.
- The tester's `test_runner` now runs the mock-based tests of the app (needs mongomock in the image) and returns the real pytest output.
- This is a fork: PRs on the GitHub UI can default to the parent repo, so check the base repository.
