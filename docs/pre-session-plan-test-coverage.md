# Pre-Session Plan: Test Coverage Analysis Agent

## Real Project Task

Analyze test coverage for todo-list-python and recommend additional tests that should be written. The agent will compare the actual behavior of the application code (todo.py, task.py) against what is currently tested (test_todo.py, tests/test_task.py), and identify gaps.

## Agent

A new agent, `test-coverage-analyzer`, will be created for this exercise. It will be scoped to read-only tools (Read, Grep, Glob) so it can analyze and recommend, but never write or modify test files itself.

## Phases of Work

### Phase 1: Analyze task.py / TaskDAO coverage
Scope: Compare task.py's TaskDAO class methods against tests/test_task.py. Identify which methods are tested, which are untested or only partially tested (e.g., happy path only, no edge cases), and recommend specific additional tests.

Rules for this phase: Treat all types of coverage gaps (missing edge cases, missing error handling tests, missing happy-path tests) as equally important. Produce a prioritized list of recommended tests, but with no single category weighted above another.

### Phase 2: Analyze todo.py / Flask routes coverage
Scope: Compare todo.py's Flask routes against test_todo.py. Identify which routes and behaviors are tested, which are not, and recommend specific additional tests.

Rules for this phase: A mid-session requirement change (see below) applies starting in this phase -- security/input-validation-related gaps must now be prioritized higher than general coverage gaps.

## Mid-Session Requirement Change

After Phase 1 completes, the following change will be introduced:

"We're planning to add user authentication to this API soon. Going forward, prioritize any coverage gaps related to security, input validation, or access control more highly than general coverage gaps."

This changes the PRIORITIZATION rule (not the analysis method itself) partway through the session, testing whether the agent can correctly apply a new priority rule going forward while also being asked to revisit and re-prioritize earlier findings under the new rule.

## Artifact to Revisit Later

The Phase 1 recommendations list (the prioritized list of additional tests for TaskDAO) will be revisited in a later phase. After the mid-session requirement change, the agent will be asked to re-review the Phase 1 list and re-prioritize it using the new security-focused priority rule, without being given the original list again -- testing whether it accurately recalls its own earlier output rather than reconstructing or guessing at it.

## Evidence for Evaluation

- Whether the agent's Phase 1 recommendations are genuinely accurate (verifiable by reading the actual TaskDAO and test_task.py code).
- Whether the agent correctly acknowledges and applies the mid-session priority change when analyzing Phase 2.
- Whether the agent, when asked to revisit Phase 1's list under the new priority rule, accurately recalls its own earlier recommendations rather than inventing new ones or misremembering what it originally found.
- Whether the final combined recommendation list (both phases) is internally consistent and correctly reflects the updated priority rule throughout.
- Rubric scores (Rule/Scope Accuracy, Task Adherence, Coherence) recorded in the iteration log, using the same 3-dimension structure from the module's lesson exercises.
