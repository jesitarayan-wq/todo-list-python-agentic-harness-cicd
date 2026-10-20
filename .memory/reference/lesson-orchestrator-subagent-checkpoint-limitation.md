---
classification: internal
project: proj-lessons
doc_type: lesson
---

## Lesson: An Orchestrator Run as a Subagent Cannot Complete Its Own Human Checkpoints

**What happened:** The project's Orchestrator was initially invoked as a subagent (via the `Agent` tool) to run a multi-step feature workflow. When the human replied "approve" at the first human-in-the-loop checkpoint, the Orchestrator subagent correctly refused to treat this as valid approval, reasoning that messages from the human never reach a subagent directly; everything passes through the main session first, so the subagent cannot distinguish genuine human approval from the main session (or another agent) merely claiming approval occurred.

**What was learned:** This was not a malfunction; it was the checkpoint safeguard behaving exactly as designed, correctly recognizing that it had no legitimate, verifiable channel to the human. It revealed a genuine architectural tension: an Orchestrator implemented as a subagent structurally cannot complete its own human-in-the-loop checkpoints, because subagents have no direct channel to the human by design.

**How to apply this lesson:** When human-in-the-loop checkpoints are required mid-workflow, run the Orchestrator logic directly in the main Claude Code session (where human replies arrive directly) rather than invoking it as a subagent via the `Agent` tool. If an Orchestrator must run as a subagent for some other reason, its definition needs to explicitly hand each checkpoint back to the main session for approval, rather than attempting to collect approval itself, since it has no way to verify authenticity otherwise.
