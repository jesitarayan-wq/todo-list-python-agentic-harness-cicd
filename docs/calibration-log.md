# Calibration Log

## Cycle 1 (2026-10-20): required role blocked by a tool allow-list, run still passes

**Branch:** calibration-cycle-1 (base 8a1a3c8)

### Failure mode and development task
- Planned failure mode: a required role is executed by the main session instead of a real subagent (substitution).
- Failure actually found: security-reviewer was rejected by the coursetools allow-list for file_read and codebase_search, so it reviewed no code, and the deterministic suite still passed 10/10.
- Development task: security-reviewer reviews todo.py and task.py (not a holdout task).
- Runs: DEV-02 (healthy baseline), DEV-03 (faulted), DEV-04 (after fix), DEV-05 (regression, planner).
- DEV-01 is not a trustworthy baseline: its own summary says the security-reviewer was never spawned, so its 9/9 measured the main session.

### Induced fault (deviation, recorded honestly)
- Commit 7db91df added the nonexistent tool mcp__retrieval__does_not_exist to security-reviewer.md.
- Hypothesis: the spawn would fail and the main session would take over. This was falsified: the subagent spawned normally and never called the tool. The fault was inert.
- The real failure was already in the repo: DEFAULT_ALLOWLIST in mcp/coursetools_server.py lists "reviewer" but not "security-reviewer" for file_read and codebase_search. The 8a1a3c8 fix changed only the grant-map JSON, not this server list.

### Detection
- Before the fix, no check caught it: DEV-03 passed 10/10 (before/DEV-03-deterministic.md). tool_grants only compares roles with the JSON map, and required_roles only checks that a role appeared.
- Added check_subagent_spawned (commit 8f53140). It fails when an event for a required role lacks executed_by "subagent". Proven on DEV-01 (9/10 fail) and passing on DEV-02 (10/10). Note: on DEV-01 it failed because the field was missing (None), not because it said main_session.
- Added check_no_denied_tool_calls (commit c22f0a3). It fails when a required role's tool call carries an error. On DEV-03 it gives 10/11 FAIL (3 denied calls: 2 file_read, 1 codebase_search). On DEV-02 it gives 11/11 PASS.
- The failure is structural, so no rubric change was made.

### Before-fix result
- DEV-03: 10/10 on the original suite, 10/11 with no_denied_tool_calls. Rubric not run (gate failed on the new check).
- The reviewer returned "not assessed" for all findings and honestly refused to retry as role "reviewer".

### Root-cause hypothesis and fix layer
- Hypothesis: the server-side allow-list does not include the role name security-reviewer, so file reads and searches are rejected.
- Fix layer: Tool (server allow-list), not Prompt.
- Open point: DEV-02 read both files successfully before the fix. The role is a caller-supplied argument in file_read(role, path), so DEV-02's subagent probably passed "reviewer", but this was not verified because raw transcripts were not read.

### Change applied
- Commit 280f176: added "security-reviewer" to the file_read and codebase_search lists in mcp/coursetools_server.py (2 lines changed).
- The inert bogus-tool line was left in place during the after-fix run, so a passing run also shows it was inert. It is still in security-reviewer.md and should be removed in a follow-up commit.

### After-fix result
- DEV-04: 11/11 deterministic. Rubric aggregate 9/9 (needs 9), 3/4 checks: root_cause_identification 2/4 FAIL (same as the DEV-01 baseline), root_cause_accuracy 3/4, summary_clarity 4/4.
- The reviewer read todo.py and task.py (no errors) and produced real findings (Critical: no auth).
- Remaining rubric concern: root_cause_identification fits review tasks poorly. The rubric was not changed.

### Evidence paths
- Before: .eval-artifacts/runs/calibration-1/before/ (DEV-02-healthy.json, DEV-02-deterministic.md, DEV-03-faulted.json, DEV-03-deterministic.md, DEV-03-deterministic-v2.md)
- After: .eval-artifacts/runs/calibration-1/after/ (DEV-04-fixed.json, DEV-04-deterministic.md, DEV-04-rubric.md)
- Regression: .eval-artifacts/runs/calibration-1/regression/ (DEV-05-regression.json, DEV-05-deterministic.md)

### Regression check
- DEV-05: planner plans GET /health. 11/11 deterministic. The planner's file_read and retrieve calls were accepted after the fix.
- Limitation: DEV-05 was never run before the fix, so this is a "still works after" check, not a before/after comparison. The diff shows no other role's allow-list entry changed.

### Other deviations
- Pre-holdout harness-data fix (commit f928cef): grant map project_manager renamed to project-manager, and test-coverage-analyzer added with Read, Grep, Glob. Made before holdout task 1, so all 7 tasks ran on one system version.
- Evidence is self-reported: the main session was told not to read subagents' raw JSONL, so tool_call details come from each subagent's own account, and some calls are not captured (e.g. planner 6 of about 9 in HO-02).
- Leftover HO-03 files and an old pagination edit (stash@{0}) from earlier work were archived or stashed before the cycle began.

## Holdout measurement 1 (2026-10-20)

Tasks evaluated: 7 (HO-01 to HO-07), each in a fresh claude session, one system version (f928cef), no changes between tasks. Source files were reset between tasks, and each task's diff was saved. Artifacts: .eval-artifacts/runs/holdout-1/ (commit 15c6062).

| Task | Deterministic | Rubric | Notes |
|---|---|---|---|
| HO-01 | 11/11 | 4/4 (9/9) | only fully clean task |
| HO-02 | 10/11 | skipped | latency 356s over the 300s budget (4 sequential agents) |
| HO-03 | 11/11 | 3/4 (aggregate 9/9) | root_cause_accuracy 2/4: findings inferred from reading code |
| HO-04 | 11/11 (weak) | 1/4 (6/9) | record reconstructed, no tool_call events |
| HO-05 | 10/11 | skipped | no_denied_tool_calls flagged an oversized-output error, not an authorization denial |
| HO-06 | 11/11 (weak) | 1/4 (6/9) | record reconstructed, no tool_call events |
| HO-07 | 11/11 (weak) | 1/4 (5/9) | record reconstructed, no tool_call events |

### Did the targeted fix hold?
- Where tool calls were recorded (HO-01, HO-02, HO-03, HO-05), no security-reviewer or planner file access was denied. The reviewer completed reviews in HO-02 and HO-03.
- HO-04, HO-06 and HO-07 have no tool_call events, so the denial check passed vacuously and cannot confirm it. The completion notices reported no errors.

### Records reconstructed after early exits (HO-04, HO-06, HO-07)
The original sessions were exited before the run record was written. Each task ran once. A separate logging-only session wrote the record from on-screen completion notices, and each record says so in its provenance note. The judge then scored records with no failure analysis, which explains the low root-cause scores. This is a fragility of the self-reporting design.

### Remaining gaps and near misses
- no_denied_tool_calls cannot tell an authorization denial from an ordinary tool error (HO-05 false positive). A future cycle should split it.
- The latency budget (300s) was set for the scripted Sandbox orchestrator and may be too tight for 4 or 5 roles (HO-02).
- HO-01's 0.65 similarity assertion and HO-05's classification assertion could not be verified: the self-reported records contain no score or classification fields. HO-05's project_id was proj-lessons on both calls.
- The tester's test_runner returns only placeholder PASS output, so no run in this harness verified tests.
- Three failure-mode checks dropped in Exercise 3.3 (context bleed, conflicting reviewers, schema validation) are still not automated, so HO-03, HO-05 and HO-07 coverage of those modes is judged by rubric only.
- HO-03: the combined report's suggested order puts a mongomock fixture and bug fixes ahead of designing authentication, though security rated missing auth Critical (a quiet priority difference).
- HO-05: nothing about E_EXPORT_417 exists in proj-lessons, so the honest answer was "not found". No context bleed was observed.
- HO-06: example-task-app did not exist in the repo. The implementer created three files under it (copy saved in HO-06-example-task-app/), and todo.py and task.py were untouched.
- HO-04: the implementer also modified two .memory files (MEMORY_INDEX.md, decision-004.md).
- HO-07: the implementer changed an existing test from 'high' to 'urgent' because 'high' is now valid. The change was in todo.py (route layer), not task.py.
- Follow-up: remove the inert does_not_exist tool line from security-reviewer.md in a new cycle, then rerun the full holdout set.
