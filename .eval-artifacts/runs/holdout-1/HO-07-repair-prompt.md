LOGGING REPAIR ONLY. Do NOT spawn any subagent. Do NOT edit or run anything in the repo. Do NOT redo any role's work.

A previous session ran HO-07 through four real subagents (planner, implementer, security-reviewer, tester, in that order) but exited before writing its run record. Write /workspace/.eval-artifacts/runs/holdout-1/HO-07.json in the same format as /workspace/.eval-artifacts/runs/holdout-1/HO-06.json, using ONLY these facts from the previous session's on-screen notices:

expected_path: ["planner","implementer","security-reviewer","tester"]
- planner: 18.5s, 9847 tokens, 4 logged tool calls plus hand-back, no errors
- implementer: 40.8s, 18410 tokens, 7 logged tool calls plus hand-back, no errors; also changed one existing test that used 'high' as its invalid value to 'urgent', because 'high' is now valid
- security-reviewer: 28.7s, 11598 tokens, 3 logged tool calls plus hand-back, no errors; approved the change; Critical and Warning findings were pre-existing and out of scope
- tester: 14s, tokens unknown (null); the tester's test_runner is believed to return only placeholder PASS output, so tests are unverified

One "subagent" event per role in that order, "executed_by": "subagent", "error": null. Write NO tool_call events. duration_seconds is 102. token_cost is 39855 (tester unknown).

Add a "provenance_note" stating plainly: RECONSTRUCTED AFTER THE SESSION EXITED from on-screen completion notices; the original session ended before writing the record; no tool_call events are logged; the diff is in HO-07-diff.md.
