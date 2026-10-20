# PRD: Test Result Summary for todo-list-python

## Workflow Description

This workflow runs the project's test command and summarizes any failures found.

## Trigger

A developer invokes `claude "[task prompt]"` from the todo-list-python repo root, inside the sandboxed container.

## Decision Events

- If pytest is not installed, the agent installs it, since the project's existing tests already use pytest conventions.
- If tests fail because MongoDB is not running or not reachable, the agent identifies this as the root cause and reports it clearly, rather than listing each failing test as a separate, unrelated problem.

## Actions

1. Check whether pytest is installed; install it if missing.
2. Run the test command: python -m pytest.
3. Capture the full output, including pass/fail counts and any error messages.
4. Analyze any failures to identify their likely root cause, grouping related failures together where they share a common cause.
5. Produce a summary stating the number of tests that passed and failed, along with the identified root cause(s) of any failures.

## Acceptance Criteria

1. The summary states the exact number of tests that passed and the exact number that failed.
2. The agent does not create new test files or modify any existing project files (test_todo.py, todo.py, task.py).
3. If failures share a common root cause, the summary identifies that shared cause rather than listing each failure as unrelated.
