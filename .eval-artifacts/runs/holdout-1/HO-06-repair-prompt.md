LOGGING REPAIR ONLY. Do NOT spawn any subagent. Do NOT edit or run anything in the repo. Do NOT redo any role's work.

A previous session ran HO-06 through four real subagents (planner, implementer, security-reviewer, tester, in that order) but exited before writing its run record. Write /workspace/.eval-artifacts/runs/holdout-1/HO-06.json in the same format as /workspace/.eval-artifacts/runs/holdout-1/HO-04.json, using ONLY these facts from the previous session's on-screen notices:

expected_path: ["planner","implementer","security-reviewer","tester"]
- planner: 29s, about 12700 tokens, 7 tool calls plus hand-back, no errors
- implementer: 24s, about 10600 tokens, 5 tool calls plus hand-back, no errors; created three files, all under example-task-app/ (index.html, tasks.js, tests/tasks.test.js); saved one lesson
- security-reviewer: 21s, about 13000 tokens, 6 tool calls plus hand-back, no errors; approved the change
- tester: 8s, tokens unknown (null); test_runner returned only a canned PASS, so the 9 new tests were not verified

One "subagent" event per role in that order, "executed_by": "subagent", "error": null. Write NO tool_call events, since individual calls were not captured. duration_seconds is 82. token_cost is 36300 (approximate, tester unknown).

Add a "provenance_note" stating plainly: RECONSTRUCTED AFTER THE SESSION EXITED from on-screen completion notices; the original session ended before writing the record; no tool_call events are logged; token counts are approximate; file evidence is in HO-06-files.md and HO-06-example-task-app/.
