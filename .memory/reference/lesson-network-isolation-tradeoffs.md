---
classification: internal
project: proj-lessons
doc_type: lesson
---

## Lesson: Full Network Isolation Blocks Legitimate First-Time Setup Needs

**What happened:** The project's container network was switched from `--network none` (blocks all networking, including loopback) to an internal bridge network (`agent-internal`, blocks only external egress while allowing loopback), specifically so the agent could reach its own MCP servers on `localhost`. However, several genuinely necessary first-time setup steps still failed under `agent-internal`, each producing the same underlying error: `EAI_AGAIN` (DNS resolution failure, since external DNS lookups are blocked). This occurred when the embedding model (`all-MiniLM-L6-v2`) needed its one-time download from huggingface.co, when MCP Inspector's `npx` install needed to fetch a package from the npm registry, and when Claude Code itself needed to reach `api.anthropic.com`.

**What was learned:** A network configuration correctly scoped for an agent's *ongoing* operation (reach its own tools, never reach the internet) can still be too restrictive for *initial setup* operations that genuinely need one-time external access (downloading a model, installing a tool, authenticating a service). The same `EAI_AGAIN` error recurred three separate times in this project for three unrelated root causes, all stemming from the same network boundary.

**How to apply this lesson:** When a command fails with `EAI_AGAIN` or "Temporary failure in name resolution" inside this environment, first check whether the current network mode is `agent-internal` before investigating the specific tool or package involved. For one-time setup steps that genuinely require internet access (model downloads, package installs, initial authentication), temporarily run the container on the default network, complete the setup step, and switch back to `agent-internal` for all subsequent, steady-state agent operation. Downloaded models and packages that land in a mounted volume (e.g., `/workspace/.cache/`) persist across container restarts, so this is typically a one-time cost per environment, not a recurring one.
