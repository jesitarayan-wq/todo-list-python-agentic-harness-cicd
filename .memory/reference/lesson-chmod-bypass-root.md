---
classification: internal
project: proj-lessons
doc_type: lesson
---

## Lesson: chmod 444 Does Not Protect Files From Root in This Container

**What happened:** The project's `.memory/knowledge/` directory was set to `chmod 444` (read-only) to enforce that only humans, not the agent, could modify stable coding standards. During testing, a file inside that directory was still successfully created and modified by the agent, even though the permission bits said read-only.

**What was learned:** This container runs all processes as the `root` user, and standard Unix file permission bits (including read-only flags) do not restrict `root` the way they restrict a normal user account. A permission setting that looks like a real technical barrier can be silently bypassed by the exact environment the agent runs in, giving a false sense of security if no one checks that the restriction actually holds.

**How to apply this lesson:** Never rely solely on filesystem permissions (`chmod`) to enforce a read-only boundary in a root-run container. Instead, write the actual enforcement into the agent's standing instructions (e.g., a CLAUDE.md policy stating "never write to this directory"), and treat that written policy as the real, primary enforcement mechanism. If a harder guarantee is needed, use a mechanism the agent cannot bypass at all, such as a separate process or a hook that runs outside the agent's own control.
