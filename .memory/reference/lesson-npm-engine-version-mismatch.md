---
classification: internal
project: proj-lessons
doc_type: lesson
---

## Lesson: MCP Inspector's Latest Version May Require a Newer Node.js Than the Container Provides

**What happened:** Running `npx @modelcontextprotocol/inspector` installed the newest published version (2.10.1), which immediately failed with an `EBADENGINE` warning stating it requires Node.js `>=22.19.0`, while the container only provides Node v20.19.2. The process appeared to start (process IDs existed, a proxy health endpoint responded internally) but the web UI never became reachable from the browser.

**What was learned:** An npm package's "latest" version is not guaranteed to be compatible with an older but still actively-used Node.js runtime, and the resulting failure mode (silent non-binding, not a clean crash) can look like a networking or port-mapping problem rather than a Node version mismatch, costing significant debugging time in the wrong direction.

**How to apply this lesson:** When a globally-installed CLI tool behaves strangely (starts but is unreachable), check its stated Node.js engine requirement against the container's actual Node version before investigating networking or port configuration. If a mismatch exists, install an explicit older, compatible version (e.g., `npx @modelcontextprotocol/inspector@0.16.8`) rather than the unpinned "latest."
