TASK: Add a 'Clear completed tasks' button to the example-task-app that removes all tasks marked done from the list, with a confirmation prompt before clearing.

Run this through real subagents via the Agent tool, in this order: planner, implementer, security-reviewer, tester. Do not do any role's work yourself. If a subagent cannot be spawned, stop and say why.

When done, write /workspace/.eval-artifacts/runs/holdout-1/HO-06.json in the same format as /workspace/.eval-artifacts/runs/calibration-1/after/DEV-04-fixed.json, with "expected_path": ["planner","implementer","security-reviewer","tester"]. Every event has "role", "executed_by" ("subagent" or "main_session", be honest) and "error" (null unless a tool call failed). Record each tool_call's "tool" name exactly as it appears in that agent's declared tools list. Do not read any subagent's raw JSONL transcript.
