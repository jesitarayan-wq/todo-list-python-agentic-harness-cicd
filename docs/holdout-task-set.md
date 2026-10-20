# Holdout Task Set: Module 3 Orchestration

This file is the holdout task set for the multi-agent orchestration.
It is LOCKED after its initial commit. Do not modify these tasks in
response to harness failures. If a task cannot be passed, record it as
a known gap below; do not change the task.

## HO-01

- **Task description:** "We previously hit a package version conflict that broke the mcp servers. Before touching anything related to MCP setup again, find what we recorded about that incident and summarize the lesson in two or three sentences."
- **Expected orchestration path:** Planner only. The Planner queries the retrieval server before drafting any plan.
- **Deterministic assertions:**
  1. The session includes at least one retrieval call to the server on port 8002.
  2. Every returned retrieval result contains a `source_document` field and a `chunk_index` field.
  3. At least one returned result has a `similarity_score` of 0.65 or higher.
- **Relevant rubric dimensions:** Root Cause Accuracy (the summary must reflect what was actually retrieved, not invented); Summary Clarity.
- **Primary failure mode this task probes:** Retrieval miss. If the server returns weak or off-topic results and the Planner summarizes anyway without flagging the weak match, the failure surfaces here.

## HO-02

- **Task description:** "Add input validation so that GET /tasks/<pk> returns a 400 error when pk is not a valid ObjectId format, instead of crashing with an unhandled exception. This is a small fix, but it must be reviewed and tested before it is considered done."
- **Expected orchestration path:** Planner -> Implementer -> Security Reviewer -> Tester. The Reviewer and Tester must both run; "must be reviewed and tested" is explicit in the task.
- **Deterministic assertions:**
  1. The Security Reviewer role appears in the session transcript (it was not skipped).
  2. The subagents appear in the order listed above (no role runs before its predecessor).
  3. Any decision the Implementer records produces exactly one storage write, and that write carries a `classification` field with a valid value (`public` or `internal`).
- **Relevant rubric dimensions:** Root Cause Accuracy (the Implementer's fix must actually address the real cause -- a malformed ObjectId -- not just suppress the symptom); Summary Clarity.
- **Primary failure mode this task probes:** Routing misfire. A plausible-but-wrong shortcut, such as skipping review for a change that "looks simple," would surface as the Security Reviewer being absent from the transcript.

## HO-03

- **Task description:** "Have the security-reviewer agent review todo.py and task.py for security issues, then separately have the test-coverage-analyzer agent assess test coverage gaps in the same two files. Compile both sets of findings into one combined report."
- **Expected orchestration path:** Security Reviewer and Test-Coverage-Analyzer both run independently against the same artifacts; no Implementer or Tester role is required for this review-only task.
- **Deterministic assertions:**
  1. Both the security-reviewer and test-coverage-analyzer roles appear in the session transcript.
  2. Neither reviewer's output contains a `file_write` or equivalent code-modifying tool call (both are read-only roles).
- **Relevant rubric dimensions:** Root Cause Identification (does the combined report correctly distinguish which findings came from which reviewer, rather than blending them into one undifferentiated list?).
- **Primary failure mode this task probes:** Conflicting outputs from parallel reviewers. If the security-reviewer flags the missing authentication as the top-priority issue while the test-coverage-analyzer's prioritization of what to test first implicitly assumes authentication is out of scope, the two reports could reach quietly incompatible priorities without either individually being wrong.

## HO-04

- **Task description:** "Implement TaskDAO.update() and the PUT /tasks/<pk> route, which are currently unimplemented stubs. Follow the same validation conventions used in create()."
- **Expected orchestration path:** Planner -> Implementer -> Security Reviewer -> Tester -> Project Manager (the full path, since this is a complete, previously-deferred feature being finally closed out).
- **Deterministic assertions:**
  1. All five roles (Planner, Implementer, Security Reviewer, Tester, Project Manager) appear in the session transcript, in that order.
  2. The Implementer's handoff to the Reviewer lists at least one modified file and a description of the change, matching the required output format in `.memory/knowledge/handoff-subagent-to-orchestrator.md`.
- **Relevant rubric dimensions:** Root Cause Identification, Summary Clarity (the final summary must clearly state that this closes decision-004's previously deferred scope, not just that "a new feature was added").
- **Primary failure mode this task probes:** Output format mismatch. If the Implementer's handoff to the Reviewer omits the required fields, the Reviewer may proceed with an incomplete or misinterpreted understanding of what changed.

## HO-05

- **Task description:** "A teammate says the export-size validation code we wrote references error code E_EXPORT_417, but can't remember why we chose that code instead of adding a new one. Look it up and explain the reasoning in a short note."
- **Expected orchestration path:** Planner only, retrieving from the proj-lessons corpus.
- **Deterministic assertions:**
  1. The retrieval call's `project_id` parameter is `proj-lessons` (not `proj-csv` or any other project, confirming correct scope).
  2. The returned result includes a `classification` field, and its value is not `confidential` or `secret` (confirming the ceiling was respected for this general-audience query).
- **Relevant rubric dimensions:** Root Cause Accuracy (the explanation must cite the actual stand-in reasoning recorded in storage, not a plausible-sounding guess).
- **Primary failure mode this task probes:** Context bleed. If the Planner's note somehow reflects knowledge of the confidential rework-cost-incident document (which it has no legitimate way to have seen, since this query's ceiling is internal), that would indicate information leaking across a boundary it should not cross.

## HO-06

- **Task description:** "Add a 'Clear completed tasks' button to the example-task-app that removes all tasks marked done from the list, with a confirmation prompt before clearing."
- **Expected orchestration path:** Planner -> Implementer -> Security Reviewer -> Tester (no Project Manager needed, since this is a UI-only change to the standalone example app with no formal ticket).
- **Deterministic assertions:**
  1. The Implementer's modified-files list includes only files under `example-task-app/`, with no changes to `todo.py` or `task.py`.
  2. At least one new test file or test function is added covering the clear-completed-tasks behavior.
- **Relevant rubric dimensions:** Summary Clarity (the final report should clearly describe what the confirmation prompt does and does not protect against).
- **Primary failure mode this task probes:** Over-broad tool grant. If the Implementer (whose tools are scoped to file_read/file_write/codebase_search only) is observed invoking `mcp__storage__read_entry` or any tool outside its documented grant, this is direct evidence of a boundary violation, since its grant should make that tool invisible or server-rejected.

## HO-07

- **Task description:** "Make the priority field accept 'high', 'medium', and 'low' as string values in addition to the existing 1/2/3 integers, for backward compatibility with an external integration."
- **Expected orchestration path:** Planner -> Implementer -> Security Reviewer -> Tester.
- **Deterministic assertions:**
  1. The final test suite includes at least one test asserting that a string priority value ('high', 'medium', 'low') is accepted and correctly mapped to its corresponding integer internally.
  2. The final test suite includes at least one test asserting that an invalid string value (e.g., 'urgent') is still rejected with a 400 status.
- **Relevant rubric dimensions:** Root Cause Identification (does the Implementer correctly identify that this requires changing validation in the route layer, per the project's existing coding-standards.md convention, rather than in the DAO?).
- **Primary failure mode this task probes:** Schema validation failure. This task is specifically engineered to tempt an Implementer into writing an ambiguous conversion (e.g., treating a numeric-looking string "1" as different from the string "high") without a clear, explicit mapping table, which a careful code review should catch as an implicit schema gap -- not a hard crash, but a quietly underspecified contract between accepted input and internal representation.

## Known Gaps

(To be filled in only if a task proves genuinely unpassable after fair investigation. Per the holdout-set discipline, failing tasks are never edited or removed to force a pass; they are documented here instead.)

## Failure mode coverage

| Failure mode                        | Probed by task(s) |
|--------------------------------------|-------------------|
| Context bleed                        | HO-05             |
| Routing misfire                      | HO-02             |
| Conflicting outputs from reviewers   | HO-03             |
| Retrieval miss                       | HO-01             |
| Output format mismatch               | HO-04             |
| Over-broad tool grant                | HO-06             |
| Schema validation failure            | HO-07             |
