TASK: Add input validation so that GET /tasks/<pk> returns a 400 error when pk is not a valid ObjectId format, instead of crashing with an unhandled exception. This is a small fix, but it must be reviewed and tested before it is considered done.

Run this through real subagents via the Agent tool, in this order: planner, implementer, security-reviewer, tester. Do not do any role's work yourself. If a subagent cannot be spawned, stop and say why.

When done, write /workspace/.eval-artifacts/runs/holdout-1/HO-02.json in the same format as /workspace/.eval-artifacts/runs/calibration-1/after/DEV-04-fixed.json, with "expected_path": ["planner","implementer","security-reviewer","tester"]. Every event has "role", "executed_by" ("subagent" or "main_session", be honest) and "error" (null unless a tool call failed). Record each tool_call's "tool" name exactly as it appears in that agent's declared tools list. Do not read any subagent's raw JSONL transcript.
