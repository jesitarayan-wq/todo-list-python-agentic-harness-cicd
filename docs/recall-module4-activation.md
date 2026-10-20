# Recall: Module 4 activation exercise

Repo: todo-list-python-agentic-harness-cicd (user jesitarayan-wq), main, pushed commit 04f8d78 (origin/main was 2c0b27c). Image todo-agent-m4 built; container launched; claude reached a task prompt. Old repo ~/todo-list-python untouched (calibration-cycle-1, stash@{0}).

Merged: Dockerfile (their version + settings.json, statusline.sh, chmod lines); CLAUDE.md (your memory rules first, then their guide); requirements.txt (mcp<2, pymongo, sqlite-vec); .gitignore (secrets, jsonl, storage.db); eval/test_deterministic.py and test_rubric_suite.py (yours win); docs calibration-log, orchestration-diagram, routing-and-tool-grant-map (yours win).
Copied: todo.py, task.py, tests/, pytest.ini, requirements.pip, settings.json, statusline.sh, .mcp.json, .claude/agents (7), mcp/, .memory (no storage.db), docs, eval extras, .eval-artifacts/runs+archive.
Not copied: .git, slack_token.txt, google_cred.json, slack_channel_info.txt, *.jsonl, storage.db.

Open: reconcile mcp/ with mcp-servers/; choose agent source of truth (agents/ vs .claude/agents/); rename docs/lessons-learned-final-report.md. (trailing dot); remove inert does_not_exist line in security-reviewer.md; verify coursetools connects; Gmail/Slack need credentials; denied-vs-errored check, 300s latency budget, self-report fragility still open.

Start: docker run (todo-agent-m4, mount repo at /workspace), then start storage (8001) and retrieval (8002) servers at the container prompt.
