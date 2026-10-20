# PRD: Lint Result Summary for todo-list-python

## Workflow Description

This workflow runs a linter against the project's code and summarizes the results.

## Trigger

A developer invokes `claude "run the linter and summarize the results..."` from the todo-list-python repo root, inside the sandboxed container.

## Decision Events

- If ruff is not available in the environment, the agent installs it.
- If ruff identifies issues that it could automatically fix, the agent does not apply automatic fixes; it only reports the issues found, unless explicitly instructed otherwise.

## Actions

1. Check whether ruff is installed; install it if missing.
2. Run ruff against the project directory.
3. Capture the full output, including all issues found.
4. Categorize or summarize the types of issues found (e.g., unused imports, style violations).
5. Produce a summary reporting the total number of issues and their categories.

## Acceptance Criteria

1. The summary states the exact total number of issues found.
2. The agent does not modify todo.py or task.py while linting (no automatic fixes applied).
3. If multiple issues share the same type, the summary groups them together rather than listing each individually.
