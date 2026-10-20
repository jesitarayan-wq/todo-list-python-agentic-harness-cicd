# Risk statements (scratch file for Module 4 governance)

NM-1: The Security Reviewer subagent was blocked from reading files because the server allow-list named "reviewer" but not "security-reviewer", and the grant map separately spelled project-manager as project_manager.
Risk: when the agent file, grant map and server allow-list disagree on a role name, a role is silently blocked or left with an undefined grant, and the run can still appear to pass.

NM-2: A nonexistent tool, mcp__retrieval__does_not_exist, was added to the Security Reviewer's tool list and nothing flagged it.
Risk: an agent file that declares tools no policy confirms lets declared access drift away from granted access without anyone noticing.

NM-3: The Implementer created a new example-task-app/ directory and modified two .memory/ files during holdout tasks, with no path limit stopping it.
Risk: a role with unrestricted write paths can change files outside its feature scope, including the memory that governs later sessions.

NM-4: The Tester's test_runner returned only placeholder PASS output, and checks passed on records that contained no tool calls.
Risk: a gate that cannot fail gives false assurance, so a broken change can be treated as verified.

NM-5: The no_denied_tool_calls check flagged an oversized-output error as a denial in HO-05, although the role had been accepted.
Risk: if the audit cannot tell a policy denial from an ordinary failure, real denials hide among false alarms.

NM-6: Tool calls were recorded from each subagent's own account, some were missing, and three run records were reconstructed after early exits.
Risk: governance that depends on self-reported evidence can be incomplete or wrong, so a boundary breach could go unrecorded.

Outside the log: slack_token.txt and google_cred.json sat in the old repo root, within reach of agent file reads.
Risk: an agent that can read credential files can pull secrets into its context and any output it writes.
