# Live run record: governed team versus one plain agent (2026-11-06)

Task, given to both runs: implement `TaskDAO.update(object_id, data)` in `task.py` and add tests for it in `tests/test_task.py`, changing no other file. Both runs started from commit `feafb35` in separate throwaway worktrees, using the image `todo-agent-m4-new` (the main image plus `mongomock` 4.3.0). The system clock used below is the Windows clock (UTC+5:30). Time stamps printed inside the containers are UTC.

## Controls used (manual, not automatic)

- Time limit: stop the governed run at 45 minutes. Not reached.
- Cost limit: stop if the session cost passed $3.00. Not reached.
- Human approval: the plan was shown and approved before any code was written.
- Escalation: the orchestrator halts if one phase fails its gate twice. Not triggered, because no phase failed.
- Retries and fallbacks: not exercised in this run. They are still planned, not built.

## Governed run (orchestrator, planner, implementer, reviewer, tester)

| Step | What happened | Evidence |
| --- | --- | --- |
| Plan | The planner produced a plan limited to `task.py` and `tests/test_task.py`, and stopped for approval. The human approved it and added two decisions: include the malformed-id test, and check only `done` in the DAO | Screenshot of the plan; planner turn 2 m 14 s |
| Implementer | Changed `task.py` and `tests/test_task.py`; 1 m 43 s | `governed.diff`, `handoff.json` |
| Handoff check | Run by hand from the host at 02:18:04: `valid: true`, no problems, exit 0 | Terminal output |
| Security review | No high-severity issues in the new code. Findings: 1 high that already existed (no authentication on any route in `todo.py`), 2 medium (no type check on `data`, uncaught `InvalidId`), lows; retrieval tool unavailable | Screenshot of the summary |
| Tester | Called the real `test_runner`: `PASS (pytest exit code 0)`, `31 passed in 0.29s` | Screenshot |
| Independent cross-check | Tests run directly in a container with no agent: `31 passed in 0.33s` | Terminal output |
| Close-out | The human decided to track the authentication gap separately; the run was marked accepted. The orchestrator wrote `docs/run-summary.md` and `decision-006.md` and corrected `decision-004.md` | `run-summary.md`, `decision-006.md` |

Result: 148 lines added and 2 removed across `task.py` and `tests/test_task.py`; `todo.py` was not changed; 15 new test functions, 18 new test cases (one is parametrized over four values).

Measurements:

- Wall clock, system clock: from 2:08 to about 2:25 (the export was saved at 2:27), including permission prompts and the host-side handoff check.
- Session 1 (planner and implementer): cost not captured. The window was closed before the usage screen was read.
- Session 2 (reviewer and tester): $0.53 (Opus $0.4286, Sonnet $0.1043, Haiku $0.0002), 1 m 21 s API time, 3 m 29 s wall time.
- The security-reviewer used about 10% and the tester about 8% of that session's usage; the Opus model, which acts as the orchestrator, accounts for about 80% of its cost.

## Baseline (one plain agent, no plan checkpoint, no subagents)

Same task, started 2:33 and finished about 2:36 on the system clock. The agent worked as the implementer role and called `test_runner` itself.

| Item | Result |
| --- | --- |
| Cost | $0.3599 (Opus $0.3598, Haiku $0.0001) |
| Time | 43 s API time, 6 m 0 s wall time on the usage screen (includes start-up); about 3 minutes of work |
| Change | 102 lines added and 2 removed; 10 new test functions, 13 new test cases |
| Tests | `PASS (pytest exit code 0)`, `26 passed in 0.45s`; independent check `26 passed in 0.26s` |
| Boundary | Only `task.py` and `tests/test_task.py` changed; `todo.py` untouched |
| Review, handoff check, approval | None |

## Comparison

| | Governed team | Plain agent |
| --- | --- | --- |
| Time | about 17 minutes | about 3 minutes of work |
| Cost | $0.53 for session 2; session 1 not captured | $0.3599 |
| Tests passing in total | 31 | 26 |
| Plan approved by a human first | Yes | No |
| Handoff check | Valid | None |
| Independent security review | Yes | None |
| Test result from a separate tester role | Yes | The same agent ran the tests |
| Run record and memory update | Yes | No |

## Observations

- The governed run is slower and costs more in total. It adds a human approval point, a checked handoff, an independent review and an independent tester. Both runs produced working, tested code.
- The two costs are not a clean comparison, because session 1 of the governed run was not captured.
- The orchestrator's tool list has no shell tool, yet the main session asked to run Bash commands and to write files, and the permission prompts allowed it. The tool list in the agent file did not limit the main session.
- The plain agent, working as the implementer, was able to call `test_runner`, which the grant list allows only for the tester. The server checks the role name the caller supplies, and the role it supplied was not recorded. This looks like the "caller picks its own clearance" weakness. It has not been fixed.
- The implementer's own `git status` failed inside the container, because a worktree's `.git` file points to a host path. Git checks were done from the host.
- The retrieval tool was unavailable to the planner and the reviewer, so no past lessons were used.
- The planner and the plain agent both flagged that checking `done` in the DAO conflicts with the standard that validation belongs in the route layer. The task required it.
- Not captured: the cost of session 1. For the baseline, the author reports enabling only the coursetools MCP server (retrieval and storage unticked); this was not screenshotted.

## Limits

One task, one run of each kind. This is not a rate, and it does not show that either approach is better in general. Evidence files: `handoff.json`, `governed.diff`, `baseline.diff`, `run-summary.md`, `decision-006.md` and the session 2 export.

## What is and is not in this repository

The application code from both runs is not merged into `task.py` or `tests/test_task.py` here. The full diffs are kept as evidence in `docs/live-run/governed.diff` and `docs/live-run/baseline.diff`. The memory changes the orchestrator made during the run (`decision-006.md` and edits to `decision-004.md` and `MEMORY_INDEX.md`) are also not merged; `docs/live-run/decision-006.md` is a copy. Two clock details are approximate, because they come from the author's reading of the system clock and the time stamps on screenshots: the end of the governed run (about 2:25) and the end of the baseline (about 2:36). The MCP server setting for the baseline is the author's report and was not screenshotted.
