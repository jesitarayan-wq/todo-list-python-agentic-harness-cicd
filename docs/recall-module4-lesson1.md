# Recall: Module 4 Lesson 1 (governance)
Repo todo-list-python-agentic-harness-cicd, HEAD 7ba8cee. 8 roles incl. dependency-auditor.
Layers: policy -> Docker (run-agent.sh) -> MCP allow-lists -> red-team -> eval/test_policy.py (35 passed).
Commits: bb6c354, 2586ced, f109a07, 9bf42ef, a0fc533, 73a3a26, 0106e36, 879dfab, e73618f, 1d8a6d5, f2d0cb2, 66c8be4, 7ba8cee.
Open: skill scope prompt-only and unlogged; Prompts 1 and 5 refused by agent not Docker; image has stale reviewer lists; .mcp.json points at old mcp/; orchestrator file_write mismatch; jsonl needs git add -f.
Rules: commit/push in Git Bash; pytest/Inspector/claude in container; no exit in same paste.
