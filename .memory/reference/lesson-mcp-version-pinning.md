---
classification: internal
project: proj-lessons
doc_type: lesson
---

## Lesson: Pin the mcp Package Below Version 2

This project pins the mcp Python package strictly below major version 2 in requirements.txt and dev-requirements.pip. This pin exists specifically to avoid a breaking import rename introduced in mcp version 2.x, where FastMCP was renamed to MCPServer and its module path was restructured, which would otherwise break this project's server code without warning.

**What happened:** When first running the storage and retrieval MCP servers, `python3 mcp/storage/server.py` crashed with `ModuleNotFoundError: No module named 'mcp'`. Installing it with a bare `pip install mcp` appeared to fix the import, but the server then crashed differently, with `ImportError: cannot import name 'FastMCP' from 'mcp.server.fastmcp'`. The bare install pulled in `mcp` version 2.3.0, which renamed `FastMCP` to `MCPServer` and restructured the module path, breaking the exact import this project's server code expects.

**What was learned:** A library crossing a major version boundary can silently break an import path that worked fine for months, and the resulting error (`ImportError`, not `ModuleNotFoundError`) looks like a different, unrelated problem unless you specifically check the installed version against what the code expects.

**How to apply this lesson:** Always install `mcp<2` explicitly (e.g., `pip install "mcp<2"`) rather than a bare `pip install mcp`, and keep this pin recorded in `requirements.txt` or `dev-requirements.pip`. Before upgrading any MCP-related dependency, check the project's actual `import` statements against that version's changelog, not just whether `pip install` succeeds.
