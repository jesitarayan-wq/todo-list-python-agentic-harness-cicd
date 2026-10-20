# Routing-and-Tool-Grant Map: todo-list-python Orchestrated Workflow

| Role | Receives from Orchestrator | Produces | Tools granted | Tools denied (reason) | Context isolation reason | Autonomy |
|---|---|---|---|---|---|---|
| Planner | Feature request and repo path | Numbered plan and file list | file-read, codebase-search | file-write (writes no code), shell (runs nothing), test-runner (does not test), task-tracker (PM owns it), web-search (not needed) | Planning reads code but never changes it; withholding write and execute tools keeps context lean and blast radius at zero | High (plans are cheap to correct) |
| Implementer | Plan and file list | Modified files | file-read, file-write, codebase-search | shell (no need to run arbitrary commands), test-runner (Tester owns it), task-tracker (PM owns it), web-search (not needed) | Needs read and write to make changes; keeping the test runner out means it cannot grade its own work, and keeping the ticket tool out means it cannot move tickets on its own | Medium (writes files; should pause before anything irreversible) |
| Security Reviewer | Modified files | Security review report (Critical/Warning/Suggestion, with safe-fix descriptions) | file-read, codebase-search | file-write (proposes, never edits), shell (runs nothing), test-runner (Tester owns it), task-tracker (PM owns it), web-search (not a review tool) | Read-only by design; with no write or execute tools it can only propose changes, never make them, so its blast radius is zero even at high autonomy | High (read-only; proposes, never changes) |
| Tester | Modified files | Pass or fail report (pytest results) | file-read, test-runner | file-write (must not "fix" code and mask failures), codebase-search (not needed to run tests), shell (test runner covers the real need), task-tracker (PM owns it), web-search (not needed) | Owns test execution and nothing else; lacking file-write means it cannot quietly edit code to make a failing test pass | Medium (executes code, but bounded to the test runner) |
| Project Manager | Orchestrator's run summary | Ticket-update confirmation | task-tracker | file-read, file-write, codebase-search, shell, test-runner, web-search (none are needed to update a ticket) | Sole owner of the ticket tool; because no coding role carries it, the ticket tool's description never enters the Planner's, Implementer's, Security Reviewer's, or Tester's context | Medium (changes a shared record; only after the Orchestrator confirms the work is done) |

## Design Observations

- The two roles that can change things (Implementer writes files, Tester runs tests) have the narrowest, most specific grants.
- The read-only roles (Planner, Security Reviewer) carry only reading tools.
- The one externally consequential tool, task-tracker, sits alone on its own role (Project Manager), so it never enters any coding role's context.
- `shell`, the most powerful and generic tool (it can run any command), is granted to no one in this workflow. The only real command-running need -- executing tests -- is served by the narrower `test-runner` tool. Denying a broad tool to everyone until a specific need justifies it is a deliberate design choice, not an oversight.

## Alternatives Considered

- Giving the Security Reviewer the test-runner so it could verify its own findings. Ruled out: the Tester role owns test execution. A Reviewer that can also run tests blurs the role boundary and creates ambiguous ownership when a test fails, since two roles could each claim or disclaim responsibility.
- Giving the Implementer the task-tracker so it could update ticket status as it works. Ruled out: task tracking belongs to the Project Manager. Granting it here would put the ticket tool's description into the Implementer's context for no benefit and would let the Implementer move tickets on its own, outside its actual job.
