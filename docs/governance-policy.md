# Agent Governance Policy

Version: v1.0.0
Last updated: 2026-10-20
Reviewed by: Jessie

## Policy basis

This policy is derived from:

- The routing-and-tool-grant map (docs/routing-and-tool-grant-map.md)
- Near-miss patterns observed in calibration (docs/calibration-log.md, section: Near-miss patterns)
- Least-privilege defaults applied to all roles

## Least-privilege default

Every role starts with no access. All grants below are explicit and justified.
Any access not explicitly granted to a role is denied by default.

To widen access, open a pull request with: the proposed grant, a concrete justification, and confirmation that the grant does not conflict with any near-miss pattern in the calibration log.

## Role: implementer

**Version:** v1.0.0
**Defined in:** .claude/agents/implementer.md

### MCP server and operation access

| Operation | Server | Granted | Justification / Denial reason |
|---|---|---|---|
| write_entry | storage | YES | Implementer records one lesson learned per task (agent file). |
| read_entry | storage | YES | Implementer reads prior decisions (course allow-list). |
| list_entries | storage | YES | Implementer checks existing state (course allow-list). |
| update_entry | storage | YES | Implementer updates state after changes (course allow-list). |
| delete_entry | storage | NO | Implementer must not remove project state (NM-3). |
| audit_read | storage | NO | Audit inspection is owned by the orchestrator (NM-6). |
| retrieve | retrieval | YES | Implementer retrieves reference docs, ceiling internal (course allow-list). |

### Tool and path access

| Tool | Granted | Justification / Denial reason |
|---|---|---|
| file_read | YES | Implementer reads the plan and the files to change. |
| file_write | YES | Core responsibility. Limited to files named in the plan (NM-3). |
| codebase_search | YES | Needed to follow project conventions. |
| shell | NO | Test execution belongs to the tester. |
| test_runner | NO | Owned by the tester role. |
| task_tracker | NO | Owned by the project-manager role. |
| web_search | NO | Not required; denied by default. |

### Skill activation scope

| Skill | Activation permitted | Reason if denied |
|---|---|---|
| check-gmail | NO | Not part of implementation; denied by default. |
| send-email | NO | Not part of implementation; denied by default. |
| send-slack-message | NO | Not part of implementation; denied by default. |
| rebuild-and-deploy | NO | Deployment is outside the role; denied by default. |
| summarize-session | NO | Not required; denied by default. |

### Data classification ceiling

**Maximum level:** internal
**Reason:** Implementer does not need confidential data and has no retrieval access.

### Autonomy level

**Level:** medium
**Conditions for human checkpoint:** Before writing any file not named in the plan; before creating a new top-level directory; before changing anything under .memory/ (NM-3).
**Reason:** Implementation is reversible in the container, but unrestricted write paths let the role change memory and project structure (NM-3).
**Container permissions:** workspace read-write, memory mounted

## Role: planner

**Version:** v1.0.0
**Defined in:** .claude/agents/planner.md

### MCP server and operation access

| Operation | Server | Granted | Justification / Denial reason |
|---|---|---|---|
| retrieve | retrieval | YES | Planner retrieves prior lessons from proj-lessons before finalizing a plan (agent file). |
| write_entry | storage | NO | Planner must not change project state (NM-3). |
| update_entry | storage | NO | Planner must not change project state (NM-3). |
| delete_entry | storage | NO | Planner must not remove project state (NM-3). |
| read_entry | storage | NO | Not required; denied by default. |
| list_entries | storage | NO | Not required; denied by default. |
| audit_read | storage | NO | Audit inspection is owned by the orchestrator (NM-6). |

### Tool and path access

| Tool | Granted | Justification / Denial reason |
|---|---|---|
| file_read | YES | Planner reads code to plan changes. |
| codebase_search | YES | Planner locates files to change. |
| file_write | NO | Planner does not write code (NM-3). |
| shell | NO | Planner does not run commands. |
| test_runner | NO | Owned by the tester role. |
| task_tracker | NO | Owned by the project-manager role. |
| web_search | NO | Not required; denied by default. |

### Skill activation scope

| Skill | Activation permitted | Reason if denied |
|---|---|---|
| check-gmail, send-email, send-slack-message, rebuild-and-deploy, summarize-session | NO | Not part of planning; denied by default. |

### Data classification ceiling

**Maximum level:** internal
**Reason:** Retrieval calls use an internal ceiling; planning needs no confidential data.

### Autonomy level

**Level:** high
**Conditions for human checkpoint:** None required, because the role is read-only. Any request to write a file or state escalates to the orchestrator.
**Reason:** All planner tools are read-only (agent file).

**Container permissions:** workspace read-only, memory omitted

## Role: security-reviewer

**Version:** v1.0.0
**Defined in:** .claude/agents/security-reviewer.md

### MCP server and operation access

| Operation | Server | Granted | Justification / Denial reason |
|---|---|---|---|
| retrieve | retrieval | YES | Reviewer retrieves standards and prior lessons from proj-lessons (agent file). |
| write_entry | storage | NO | Reviewer must not change project state (NM-3). |
| update_entry | storage | NO | Reviewer must not change project state (NM-3). |
| delete_entry | storage | NO | Reviewer must not remove project state (NM-3). |
| read_entry | storage | YES | Reviewer reads decisions to review them (course allow-list). |
| list_entries | storage | YES | Reviewer checks what exists before reviewing (course allow-list). |
| audit_read | storage | NO | Audit inspection is owned by the orchestrator (NM-6). |
| does_not_exist | retrieval | NO | Not a real operation; declared in the agent file with no policy backing (NM-2). To be removed from the file. |

### Tool and path access

| Tool | Granted | Justification / Denial reason |
|---|---|---|
| file_read | YES | Reviewer reads files under review. Credential files are out of scope (see credentials note in the calibration log). |
| codebase_search | YES | Reviewer searches the code under review. |
| file_write | NO | Reviewer is read-only. |
| shell | NO | Reviewer does not run commands. |
| test_runner | NO | Owned by the tester role. |
| task_tracker | NO | Owned by the project-manager role. |
| web_search | NO | Not required; denied by default. |

### Skill activation scope

| Skill | Activation permitted | Reason if denied |
|---|---|---|
| check-gmail, send-email, send-slack-message, rebuild-and-deploy, summarize-session | NO | Not part of review; denied by default. |

### Data classification ceiling

**Maximum level:** internal
**Reason:** Review of internal work needs no confidential data.

### Autonomy level

**Level:** high
**Conditions for human checkpoint:** Output is advisory only; any action beyond producing findings escalates to the orchestrator. The role name must match across the agent file, grant map and server allow-lists (NM-1).
**Reason:** All reviewer tools are read-only (agent file).

**Container permissions:** workspace read-only, memory omitted

## Role: tester

**Version:** v1.0.0
**Defined in:** .claude/agents/tester.md

### MCP server and operation access

| Operation | Server | Granted | Justification / Denial reason |
|---|---|---|---|
| write_entry | storage | NO | Tester reports results but does not change stored state (NM-3). |
| update_entry | storage | NO | Tester reports results but does not change stored state (NM-3). |
| delete_entry | storage | NO | Tester must not remove project state (NM-3). |
| read_entry | storage | YES | Tester reads decisions and test context. |
| list_entries | storage | YES | Tester lists available state before reporting. |
| audit_read | storage | NO | Audit inspection is owned by the orchestrator (NM-6). |
| retrieve | retrieval | YES | Tester retrieves internal references for test context (ceiling internal). |

### Tool and path access

| Tool | Granted | Justification / Denial reason |
|---|---|---|
| file_read | YES | Tester reads the modified-file list from its handoff. |
| test_runner | YES | Core responsibility. The current tool returns placeholder PASS output and must be replaced with a real runner (NM-4). |
| file_write | NO | Tester does not write code. |
| codebase_search | NO | Not required (agent file). |
| shell | NO | Test execution goes through test_runner only. |
| task_tracker | NO | Owned by the project-manager role. |
| web_search | NO | Not required; denied by default. |

### Skill activation scope

| Skill | Activation permitted | Reason if denied |
|---|---|---|
| check-gmail, send-email, send-slack-message, rebuild-and-deploy, summarize-session | NO | Not part of testing; denied by default. |

### Data classification ceiling

**Maximum level:** internal
**Reason:** Tester has no retrieval access and needs no confidential data.

### Autonomy level

**Level:** medium
**Conditions for human checkpoint:** A result must not be reported as a pass unless test_runner returned real test output (NM-4); any write to tracked files escalates.
**Reason:** A gate that cannot fail gives false assurance (NM-4).

**Container permissions:** workspace read-only, memory omitted

## Role: project-manager

**Version:** v1.0.0
**Defined in:** .claude/agents/project-manager.md

### MCP server and operation access

| Operation | Server | Granted | Justification / Denial reason |
|---|---|---|---|
| write_entry | storage | NO | Project-manager updates the ticket, not project state (NM-3). |
| update_entry | storage | NO | Project-manager updates the ticket, not project state (NM-3). |
| delete_entry | storage | NO | Must not remove project state (NM-3). |
| read_entry | storage | YES | Project-manager reads state to report ticket status. |
| list_entries | storage | YES | Project-manager lists state to report ticket status. |
| audit_read | storage | NO | Audit inspection is owned by the orchestrator (NM-6). |
| retrieve | retrieval | NO | Does not perform retrieval. |

### Tool and path access

| Tool | Granted | Justification / Denial reason |
|---|---|---|
| task_tracker | YES | Owns the ticket status exclusively (agent file). |
| file_read | NO | Not required (agent file). |
| file_write | NO | Not required (agent file). |
| codebase_search | NO | Not required (agent file). |
| shell | NO | Not required (agent file). |
| test_runner | NO | Owned by the tester role. |
| web_search | NO | Not required (agent file). |

### Skill activation scope

| Skill | Activation permitted | Reason if denied |
|---|---|---|
| check-gmail, send-email, send-slack-message, rebuild-and-deploy, summarize-session | NO | Not part of ticket updates; denied by default. |

### Data classification ceiling

**Maximum level:** internal
**Reason:** Project-manager needs only ticket status and has no retrieval access.

### Autonomy level

**Level:** medium
**Conditions for human checkpoint:** Setting a ticket to done when the tester's result was unverified (NM-4).
**Reason:** Ticket status is the only state this role changes.

**Container permissions:** workspace read-only, memory omitted

## Role: test-coverage-analyzer

**Version:** v1.0.0
**Defined in:** .claude/agents/test-coverage-analyzer.md

### MCP server and operation access

| Operation | Server | Granted | Justification / Denial reason |
|---|---|---|---|
| write_entry | storage | NO | Analyzer only recommends; it must not change state (NM-3). |
| update_entry | storage | NO | Analyzer only recommends; it must not change state (NM-3). |
| delete_entry | storage | NO | Must not remove project state (NM-3). |
| read_entry | storage | NO | Not required; denied by default. |
| list_entries | storage | NO | Not required; denied by default. |
| audit_read | storage | NO | Audit inspection is owned by the orchestrator (NM-6). |
| retrieve | retrieval | NO | Not required; denied by default. |

### Tool and path access

| Tool | Granted | Justification / Denial reason |
|---|---|---|
| Read | YES | Reads application code and tests (agent file). |
| Grep | YES | Searches code and tests (agent file). |
| Glob | YES | Locates files to analyze (agent file). |
| file_write / Write / Edit | NO | Analyzer never modifies files (agent file; NM-3). |
| shell / test_runner | NO | Analyzer never runs the app or tests (agent file). |
| task_tracker, web_search | NO | Not required; denied by default. |

### Skill activation scope

| Skill | Activation permitted | Reason if denied |
|---|---|---|
| check-gmail, send-email, send-slack-message, rebuild-and-deploy, summarize-session | NO | Not part of coverage analysis; denied by default. |

### Data classification ceiling

**Maximum level:** internal
**Reason:** Analysis of internal code and tests needs no confidential data.

### Autonomy level

**Level:** low
**Conditions for human checkpoint:** Output is advisory only; any action beyond producing recommendations escalates to the orchestrator.
**Reason:** Read-only role. The agent file declares no autonomy field, so this level is set by the policy, not copied from the file.

**Container permissions:** workspace read-only, memory omitted

## Role: orchestrator

**Version:** v1.0.0
**Defined in:** .claude/agents/orchestrator.md

### MCP server and operation access

| Operation | Server | Granted | Justification / Denial reason |
|---|---|---|---|
| audit_read | storage | YES | Audit inspection is owned by the orchestrator (NM-6). Not yet enforced by the current servers. |
| read_entry | storage | YES | Orchestrator reads state to coordinate subagents. |
| list_entries | storage | YES | Orchestrator lists state to coordinate subagents. |
| write_entry | storage | YES | Orchestrator records run state it coordinates (course allow-list). |
| update_entry | storage | YES | Orchestrator updates run state it coordinates (course allow-list). |
| delete_entry | storage | YES | Orchestrator manages entry lifecycle; no other role may delete (closes NM-3). |
| retrieve | retrieval | YES | Orchestrator retrieves for coordination, ceiling confidential (course allow-list). |

### Tool and path access

| Tool | Granted | Justification / Denial reason |
|---|---|---|
| Agent | YES | Core responsibility: invokes subagents in order. |
| file_read | YES | Reads handoffs and results. |
| file_write | NO | The agent file declares it, but the role's own instructions say it does not modify files. Declared and granted access disagree (NM-2); the declaration should be removed. |
| codebase_search | NO | Not required (agent file). |
| shell / test_runner | NO | Owned by other roles. |
| task_tracker | NO | Owned by the project-manager role. |
| web_search | NO | Not required (agent file). |

### Skill activation scope

| Skill | Activation permitted | Reason if denied |
|---|---|---|
| check-gmail, send-email, send-slack-message, rebuild-and-deploy, summarize-session | NO | Not part of orchestration; denied by default. |

### Data classification ceiling

**Maximum level:** confidential
**Reason:** Course allow-list gives the orchestrator a confidential retrieval ceiling.

### Autonomy level

**Level:** medium
**Conditions for human checkpoint:** Before replacing a human escalation with an automatic fallback; any attempt to do a subagent's work itself (agent file); any write outside the run record.
**Reason:** The orchestrator coordinates but must not substitute for a subagent (NM-1, NM-6).
**Container permissions:** workspace read-write, memory mounted
