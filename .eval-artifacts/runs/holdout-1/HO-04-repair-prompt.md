LOGGING REPAIR ONLY. Do NOT spawn any subagent. Do NOT read, edit, or run anything in the repo. Do NOT redo any role's work.

A previous session ran HO-04 through five real subagents (planner, implementer, security-reviewer, tester, project-manager, in that order) but exited before writing its run record. Write /workspace/.eval-artifacts/runs/holdout-1/HO-04.json in the same format as /workspace/.eval-artifacts/runs/holdout-1/HO-03.json, using ONLY these facts, which come from the previous session's on-screen completion notices:

expected_path: ["planner","implementer","security-reviewer","tester","project-manager"]
- planner: 30s, 16371 tokens, 8 tool calls plus hand-back, no errors
- implementer: 75s, 27138 tokens, 16 tool calls plus hand-back, no errors
- security-reviewer: 41s, 20839 tokens, 6 tool calls plus hand-back, no errors; found no defects in the new update/PUT code; flagged missing authentication as pre-existing
- tester: 10s, 6314 tokens; test_runner returned only placeholder dummy PASS lines, so tests were not actually verified
- project-manager: 9s, tokens unknown (record as null), updated ticket status

Write one "subagent" event per role, in that order, with "executed_by": "subagent" and "error": null. Do NOT invent individual tool_call events: the individual calls were not captured, so write none. duration_seconds is the sum of the agent durations (165). token_cost is the sum of known tokens (70662) and note project-manager's is unknown.

Add a "provenance_note" that states plainly: this record was RECONSTRUCTED AFTER THE SESSION EXITED from on-screen completion notices; the original session ended before writing the record; no tool_call events are logged; the diff is saved separately in HO-04-diff.md.
