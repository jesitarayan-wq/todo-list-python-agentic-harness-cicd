# Agent Instructions

## Memory Configuration

At the start of every session, read .memory/project/MEMORY_INDEX.md
to orient yourself. Then read any active entries listed there that
are relevant to the current task.

Before making any significant decision or observing something worth
remembering across sessions, check the index for an existing entry
on the same topic. Update existing entries rather than creating
duplicates.

### Memory layers

- .memory/project/ -- Read on startup via MEMORY_INDEX.md. You may
  write new entries here when a significant decision is made or
  project state changes.

- .memory/knowledge/ -- Read-only. Consult before making any decision
  that touches coding standards or architectural constraints. Never
  attempt to write to this directory.

- .memory/reference/ -- Read-only. Query by keyword for relevant
  excerpts when you need background context. Do not read the entire
  directory.

### Write policy

Before writing any content to a memory file, classify it:
- If it is Public or Internal: proceed with writing
- If it is Confidential: do not write it to memory. Note in your
  response that the information was not stored and explain where
  it should be retrieved from instead.
- If it is Secret (credential, token, API key, PII): do not write
  it anywhere. Use it for the immediate task only. If you find a
  secret already written in a memory file, flag it immediately and
  do not proceed until a human removes it.

Before writing a new memory entry, check MEMORY_INDEX.md for an
existing entry on the same topic. Update existing entries rather
than creating new ones. Never write anything classified as
Confidential or Secret to any memory layer.

### Stale memory policy

Before acting on any memory entry, check its review date.
If the review date has passed:
1. Do not act on that entry until a human confirms it
  is still accurate
2. State clearly in your response: "Memory entry
  [filename] has a review date of [date], which has
  passed. Please confirm this is still current before
  I proceed."
3. Wait for confirmation before using the entry

This applies to all entries in .memory/project/.
Knowledge files do not have review dates and are
maintained by humans directly.

### Scope verification

Read SCOPE.md at the root of .memory/ on startup. If it does not
match this project, halt and report the mismatch before doing
anything else.

### Pre-commit credential scan

A pre-commit hook at .git/hooks/pre-commit scans .memory/ for common
credential patterns (sk-, password=, secret=, token=, api_key=,
apikey=) and blocks the commit if any are found.


<!-- Scope verification confirmed working correctly via Failure Mode 2 testing on 2026-10-01; no strengthening was required, as the existing check caught the deliberate mismatch on first attempt. See docs/iteration-log-memory.md for full test record. -->


---

# Project and environment (Module 4 infrastructure)

## This project

Target codebase: todo-list-python (Flask + MongoDB to-do API: todo.py, task.py, tests/).
Agents live in .claude/agents/ (orchestrator, planner, implementer, security-reviewer, tester, project-manager, test-coverage-analyzer).
MCP servers: mcp/ (project servers, registered in .mcp.json) and mcp-servers/ (Module 4 governed servers, to be reconciled in Lesson 1).
Eval harness: eval/ (test_deterministic.py has 11 checks; rubric in eval/rubric.json). Calibration history: docs/calibration-log.md.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Docker-based development environment for LaunchCode's **Agentic Programming** course, Module 4.

## Docker Commands

Build the image:
```bash
docker build -t agentic_engineer_4 .
```

Force a clean rebuild:
```bash
docker build --no-cache -t agentic_engineer_4 .
```

Run with a local workspace mounted (recommended):
```bash
docker run -it --rm -p 8501:8501 -p 8502:8502 \
  -e SLACK_BOT_TOKEN=your-token \
  -e SLACK_TEAM_ID=your-team-id \
  -v "$PWD":/workspace \
  agentic_engineer_4
```

Pull and run the pre-built image from DockerHub:
```bash
docker run -it --rm -p 8501:8501 -v "$PWD":/workspace heatonresearch/agentic_engineer_4:latest
```

## MCP Servers

Two MCP servers are pre-installed and configured in `/root/.claude/settings.json`:

### Slack
- Package: `@modelcontextprotocol/server-slack`
- Requires env vars: `SLACK_BOT_TOKEN`, `SLACK_TEAM_ID`
- Allows Claude Code prompts to read channels, post messages, and interact with Slack workspaces.

### Gmail
- Package: `@gongrzhe/server-gmail-autoauth-mcp`
- OAuth credentials stored in `/root/.gmail-mcp/` (persist this directory across container runs if needed)
- Allows Claude Code prompts to read, search, and send Gmail messages.

## Skills

Pre-configured skills (invoked with `/skill-name` in Claude Code):

| Skill | Description |
|---|---|
| `/send-slack-message` | Send a message to a Slack channel |
| `/check-gmail` | Summarize recent unread Gmail messages |
| `/send-email` | Draft and send an email via Gmail |
| `/summarize-session` | Bullet-point summary of the current session |
| `/rebuild-and-deploy` | Rebuild the Docker image and push it to DockerHub |

Skills are defined in `settings.json` which is copied to `/root/.claude/settings.json` during image build.

## Agents

Pre-configured sub-agents available inside Claude Code sessions. Agents are autonomous specialists that Claude Code can invoke automatically or that you can request explicitly.

| Agent | Description |
|---|---|
| `code-reviewer` | Reviews recent git changes for quality, security, and maintainability |
| `email-summarize` | Checks new Gmail messages and posts sender + 2-line summary to #test Slack channel |

Agents are defined as Markdown files with YAML frontmatter in `/root/.claude/agents/` inside the container. Source files live in the `agents/` directory of this repo and are copied in at build time.

**Running an agent:**

Ask Claude Code to use the agent explicitly:
```
Review my recent changes using the code-reviewer agent.
```

Or Claude Code may invoke it automatically when the task matches the agent's description.

## Running Streamlit Apps

From inside the container:
```bash
streamlit run app.py
```

Access at `http://localhost:8501`.

## Key Dependencies (requirements.txt)

- `anthropic` — Claude API client
- `streamlit` — web UI framework
- `python-dotenv` — environment variable management
- `slack_sdk` — Slack integration (Python)
- `google-api-python-client`, `google-auth-oauthlib` — Gmail/Google API access (Python)
- `fastapi`, `flask`, `uvicorn` — web frameworks
- `pydantic`, `httpx` — HTTP and data validation

## Environment & Tools in the Container

- Python 3.12 (aliased as `python` and `pip`)
- Claude Code CLI (`claude`) installed globally via npm
- OpenCode (`opencode-ai`) installed globally via npm
- MCP server: `@modelcontextprotocol/server-slack`
- MCP server: `@gongrzhe/server-gmail-autoauth-mcp`
- ngrok for tunneling
- Workspace mounted at `/workspace`

## Gmail API Setup

Place `credentials.json` (from Google Cloud Console) in your workspace directory. On first run it triggers OAuth and saves `token.json`. Both files should be in `.gitignore`.
