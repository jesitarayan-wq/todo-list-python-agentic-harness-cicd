# security-reviewer Run 2 Output (v0.3.0, Lab Track 2)

## Critical
1. No authentication/authorization on any route (todo.py:12-39)
   - Safe-fix requirement: an authentication/authorization check (e.g., verifying a session, token, or API key) performed before any DAO call in each route, rejecting unauthenticated requests with a 401/403.

## Warning
2. Unvalidated request.json (todo.py:26-29)
   - Safe-fix requirement: checking that request.json is a non-null dict before calling .get() on it, returning a 400 response otherwise.
3. Unvalidated pk passed to ObjectId() (todo.py:20, task.py:38)
   - Safe-fix requirement: validating that pk matches the expected ObjectId format (or catching the conversion error) before querying, and returning a 400/404 for invalid ids.
4. PUT /tasks/<pk> registered but unhandled, update()/delete() are no-ops (todo.py:17-20, task.py:41-45)
   - Safe-fix requirement: either implementing the PUT branch (with its own input validation) or removing PUT from methods until implemented.

## Suggestions
5. No pagination on list()
6. MongoDB connection has no auth configured
7. app.run() doesn't explicitly disable debug mode

## Important Observation
Step 6 (safe-fix descriptions) WAS correctly produced by the security-reviewer agent itself for all 4 Critical/Warning findings. The initial relay of results to the user omitted these descriptions during summarization -- this was a gap in how the orchestrating session condensed the sub-agent's output, not a failure of security-reviewer itself. Lesson: verify sub-agent compliance against raw output, not a summary of it.
