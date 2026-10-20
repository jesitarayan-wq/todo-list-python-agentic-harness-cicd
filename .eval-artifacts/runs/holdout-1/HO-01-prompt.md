TASK: We previously hit a package version conflict that broke the mcp servers. Before touching anything related to MCP setup again, find what we recorded about that incident and summarize the lesson in two or three sentences.

Run this through real subagents via the Agent tool, in this order: planner. Do not do any role's work yourself. If a subagent cannot be spawned, stop and say why.

When done, write /workspace/.eval-artifacts/runs/holdout-1/HO-01.json in the same format as /workspace/.eval-artifacts/runs/calibration-1/after/DEV-04-fixed.json, with "expected_path": ["planner"]. Every event has "role", "executed_by" ("subagent" or "main_session", be honest) and "error" (null unless a tool call failed). Record each tool_call's "tool" name exactly as it appears in that agent's declared tools list. Do not read any subagent's raw JSONL transcript.
