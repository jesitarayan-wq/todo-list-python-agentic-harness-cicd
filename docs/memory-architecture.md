# Memory Architecture

## What this workflow needs to remember

This agent helps maintain the todo-list-python Flask/MongoDB API by implementing new features, analyzing test coverage, and reviewing code quality. Across sessions, it needs to remember which implementation approach was chosen for a feature and why, which work has been deliberately deferred versus genuinely incomplete, current known limitations (such as the missing route-level test coverage for the priority feature), and any architectural conventions this project follows (such as validation logic living in the route layer rather than the DAO layer). It does not need to store the actual contents of task.py, todo.py, or the test files, since those already exist as project artifacts that a fresh session can read directly. It must not store database credentials, MongoDB connection strings, or environment-specific details tied only to one session container (such as a one-time package conflict that was already resolved).
 
## Layer 1: Project memory directory
# Belongs here

- Current state: priority is stored as an integer (1-3), not a string, because MongoDB's native sort would give wrong results with string values
- Current state: priority defaults to medium (2) if not provided on POST
- Current state: route-level test coverage for priority validation in test_todo.py does not yet exist
- Current state: backfilling existing documents with a missing priority field, and implementing update()/PUT, remain out of scope for this feature by design, not by oversight
- Current state: the next recommended action is writing the missing test_todo.py route-level tests

# Does not belong here

- The actual contents of task.py or todo.py (too large, already exists as a project artifact, changes constantly as code evolves)
- MongoDB connection details or credentials (secrets must never be stored here)

- **Scope:** Project-scoped. This memory is for the todo-list-python repository only.
- **Write permissions:** The agent can write new entries and update existing ones as decisions are made.
- **Pruning policy:**
  - Entries tied to a specific feature are archived once that feature is fully complete and merged.
  - Entries about the project as a whole (decisions, known quirks, current phase) are reviewed every 90 days.

## Layer 2: Knowledge files

# Belongs here

- Validation logic in this project lives in the route layer (todo.py), not the DAO layer (task.py) -- new fields should follow this existing convention
- New fields added to a task must be explicitly whitelisted in TaskDAO.create(), following the existing pattern for title/description
- Boolean values must be explicitly guarded against when validating numeric-range fields, since True/False are valid ints in Python

# Does not belong here

- Specific feature decisions like "priority is an integer" (this is project memory, tied to one feature, not a universal rule)
- Test coverage status (this changes constantly, belongs in project memory, not a stable rule)

- **Scope:** Project-scoped. Applies to all future feature work in todo-list-python.
- **Write permissions:** Human-only. The agent may read this but must not edit it without explicit human review.
- **Pruning policy:** Reviewed whenever the project's architecture changes significantly, or at minimum every 6 months.

## Layer 3: Indexed reference documents
# Belongs here

- The full iteration-log-security.md (security-reviewer agent's detailed findings)
- The full iteration-log-context.md (context-management technique comparisons)
- The pre-session-plan-test-coverage.md and technique-plan-test-coverage.md documents

# Does not belong here

- Anything needed for routine, everyday feature work (too large to load every session)
- Anything that changes frequently (indexed references should be relatively stable, larger documents)

- **Scope:** Project-scoped.
- **Write permissions:** Human-authored; agent may read via the index but does not edit these documents directly.
- **Pruning policy:** Reviewed annually, or when a document becomes clearly superseded by newer work.

## Allocation decision table
| Information Type | Layer | Reason |
|---|---|---|
| Priority stored as integer, chosen for MongoDB sort behavior | Project memory | Feature-specific decision, not inferable from code |
| Deliberate deferral of backfill/update() | Project memory | Must prevent a recurring mistake, read every session |
| Validation lives in route layer, not DAO | Knowledge file | Stable, project-wide convention |
| Detailed iteration logs and pre-session plans | Indexed reference (planned, not yet implemented) | Large, infrequently needed documents -- in practice `.memory/reference/` is currently empty and these documents still live in `docs/`, not indexed into Layer 3 |
| Actual task.py/todo.py contents | Existing artifact (not memory) | Already captured in code |
| Memory scope declaration (SCOPE.md) | Project memory (read-only to agent) | Identifies which project owns the mounted memory directory |
| Credential location | Project memory | Records how the credential is accessed (e.g. environment variable name) without storing its value |

## Alternatives considered
Considered storing the "deliberate deferral of backfill and update()/PUT" decision as an Indexed Reference document instead of Project Memory. Ruled this out because Indexed References are consulted only occasionally, via an index, while this deferral decision needs to be seen every time a fresh session touches priority-related code, to avoid a future session mistakenly "fixing" something that was intentionally left alone. Project Memory is read at every session startup, making it the correct choice for a decision that must actively prevent a specific, recurring mistake, rather than sitting passively available only when searched for.

## Pre-Commit Credential Scan

A Git pre-commit hook exists at `.git/hooks/pre-commit` and scans the entire `.memory/` directory before any commit, blocking it (non-zero exit code) if it finds patterns matching common credential formats (`sk-`, `password=`, `secret=`, `token=`, `api_key=`, `apikey=`, case-insensitive). This was tested directly: a deliberate test file containing `password=test123` was correctly blocked, and a legitimate documentation commit was correctly allowed through.

**Important limitation:** `.git/hooks/` is not tracked by Git and does not travel with clones or pulls of this repository. Each developer working on this project would need to manually recreate this hook. For a team setting, this should be migrated to a managed, versioned hook system (e.g., the `pre-commit` Python package), but a manual hook is sufficient for this course's single-user context.

## Enforcement

This project relies on two different kinds of enforcement, and the distinction matters: a **soft guard** is a CLAUDE.md policy that the agent follows through judgment -- it can be misread, skipped, or reasoned around. A **hard stop** is mechanical -- it blocks the action regardless of what the agent decides. Everything below is a soft guard except the pre-commit hook.

### Soft guard: stale memory

Before acting on any entry in `.memory/project/`, the agent checks that entry's review date. If the review date has passed, the agent does not use the entry as-is. Instead it:

1. Flags the entry by name and states its review date in its response.
2. States explicitly that the date has passed and the entry needs human confirmation.
3. Waits for a human to confirm the entry is still accurate before relying on it.

This was tested and confirmed working in the Failure Mode 1 exercise: an entry with a past review date was correctly flagged and held rather than acted on.

This is a soft guard -- it depends on the agent reading CLAUDE.md's stale memory policy and applying it correctly. Nothing mechanically prevents the agent from using a stale entry if it fails to check the date.

**Why this exists:** This safeguard was added after testing a decision entry with a backdated review date and a fact that contradicted the actual codebase. Without this check, nothing would have prevented the agent from treating outdated information as current. During testing, the agent correctly flagged the review date, cross-verified the claim against actual code and git history, and refused to act until confirmed -- the safeguard worked on first test.

### Soft guard: scope verification

`SCOPE.md` at the root of `.memory/` names the project that directory's memory belongs to. Per the startup check in CLAUDE.md, the agent reads `SCOPE.md` before reading any other memory file and compares the project it names against the actual current repository. If they don't match, the agent halts and reports the mismatch instead of proceeding to read project memory, knowledge files, or indexed references.

This was tested and confirmed working in the Failure Mode 2 exercise: a `SCOPE.md` naming a different project than the current repository correctly halted the agent before it read further.

This is also a soft guard -- it relies on the agent performing the comparison and choosing to halt, not on anything that mechanically blocks file reads.

**Why this exists:** This safeguard was added after testing a container with memory mounted from a simulated second project (project-b), containing a decision that directly contradicted the real project's memory. Without this check, the agent could have treated the other project's contradictory decision as valid for this codebase. During testing, the agent independently verified the actual repo identity via git, compared it against SCOPE.md's claim, found the mismatch, and halted before reading any decision content -- the safeguard worked on first test.

### Soft guard: data classification and credential handling

See the Data Classification section above for the full Public/Internal/Confidential/Secret breakdown. The point most relevant to enforcement: credential **values** (the actual key, token, or password string) must never be written to any memory layer, under any classification. Only the **name** of the environment variable that holds the value may be referenced -- for example, `ANTHROPIC_API_KEY` is fine to write down; the string assigned to it is not. This rule is also a soft guard: it depends on the agent classifying content correctly before writing, not on a mechanism that inspects writes as they happen.

### Hard stop: pre-commit credential scan

The pre-commit hook at `.git/hooks/pre-commit` (described above) is the one true hard stop in this architecture. It scans `.memory/` for credential-shaped patterns and blocks the commit with a non-zero exit code if it finds one, regardless of whether the agent classified the content correctly, checked a review date, or verified scope first. It is the backstop for when a soft guard fails -- not a replacement for them, since it only catches pattern-matched secrets at commit time and does not catch Confidential data, stale reasoning, or scope mismatches.

**Why this exists:** This safeguard was added after testing what happens when a credential-shaped value is deliberately written into a memory file and committed. CLAUDE.md's write policy alone had already refused to write the value once, but needed to be explicitly overridden to reproduce the mistake -- showing that a judgment-based policy alone is not a sufficient backstop if an override or a different agent session chooses to bypass it. The pre-commit hook provides a mechanical check that does not depend on the agent's judgment at all: it was tested directly and correctly blocked a commit containing a fake secret, then correctly allowed a legitimate commit through afterward.

## Data Classification

Before writing anything to a memory file, classify it:

- **Public** — Safe to commit to the repo and share
 broadly. Most project decisions and coding standards
 fall here.

- **Internal** — Safe within the team but not for
 public repos. Store in a non-committed volume or
 .gitignore the containing folder.

- **Confidential** — Sensitive business data. Do not
 store in agent memory. Retrieve from secure systems
 on demand.

- **Secret** — Credentials, tokens, API keys, PII.
 Must never appear in any memory file. If the agent
 encounters a secret during a run, use it for the
 immediate task only and explicitly do not write it
 to any memory layer. Reference the environment
 variable name instead.

### Guardrails

A pre-commit hook at .git/hooks/pre-commit scans
.memory/ for common credential patterns before each
commit. If a pattern is found, the commit is blocked.

<!-- Reviewed: this document reflects the current system state after all three failure-mode exercises. -->
