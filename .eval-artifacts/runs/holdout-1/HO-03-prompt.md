TASK: Have the security-reviewer agent review todo.py and task.py for security issues, then separately have the test-coverage-analyzer agent assess test coverage gaps in the same two files. Compile both sets of findings into one combined report.

Run this through real subagents via the Agent tool, in this order: security-reviewer, then test-coverage-analyzer (independently, both read-only). Do not do any role's work yourself. If a subagent cannot be spawned, stop and say why.

When done, write /workspace/.eval-artifacts/runs/holdout-1/HO-03.json in the same format as /workspace/.eval-artifacts/runs/calibration-1/after/DEV-04-fixed.json, with "expected_path": ["security-reviewer","test-coverage-analyzer"]. Every event has "role", "executed_by" ("subagent" or "main_session", be honest) and "error" (null unless a tool call failed). Record each tool_call's "tool" name exactly as it appears in that agent's declared tools list. Do not read any subagent's raw JSONL transcript.
