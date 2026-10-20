# Coding Standards

Last reviewed: 2026-09-29
Maintained by: the team

These standards apply to all code in this project. The
agent should consult this file before writing or reviewing
any code. These rules are set by humans and the agent
should never modify this file.

## Validation lives in the route layer, not the DAO
todo.py validates incoming request data; task.py's TaskDAO trusts that data is already valid and does not re-validate it.

## New fields must be explicitly whitelisted in TaskDAO.create()
Following the existing pattern for title, description, and priority, any new field must be deliberately added to the dict construction, not passed through automatically.

## Boolean values must be explicitly guarded when validating numeric-range fields
Since True and False are valid integers in Python, range checks like "value in (1, 2, 3)" must explicitly exclude booleans.

## Flask routes must return a status code matching the actual outcome
Do not default to 200 for responses that represent an error or a partial failure.

## No hardcoded MongoDB connection strings
Connection details should come from configuration, not be embedded directly in task.py.

## New DAO methods must have corresponding tests in tests/test_task.py using mongomock
Tests should not require a live MongoDB instance to run.
