---
classification: internal
project: proj-lessons
doc_type: lesson
---

## Lesson: Route-Level Tests Hang Indefinitely Without a Live MongoDB Instance

Route-level tests in this project hang indefinitely instead of failing quickly whenever they are run inside the sandboxed container, because they require an actual live MongoDB connection that simply does not exist in that environment, and the default connection behavior retries silently rather than raising a fast, visible error.

**What happened:** When a Tester subagent attempted to run `tests/test_todo.py` inside the sandboxed container, `pytest` did not fail quickly with a clear connection error; it hung indefinitely, eventually requiring the process to be manually stopped after several minutes with no result. This is because `todo.py`'s routes connect directly to a real MongoDB instance (`mongodb://localhost`), which does not exist in this container, and the default pymongo connection behavior retries silently rather than failing fast.

**What was learned:** `tests/test_task.py`, which tests the DAO layer using `mongomock` (an in-memory MongoDB simulator), runs successfully in this environment with no live database needed. `tests/test_todo.py`, which tests the Flask routes directly, requires an actual live MongoDB connection and cannot be verified in this container as currently configured. A silently-hanging test looks identical, from the outside, to a slow-but-working test, which makes this failure mode easy to miss until a timeout forces the issue.

**How to apply this lesson:** When writing or assigning route-level tests, confirm whether a live database dependency exists before assuming a Tester agent can verify them in a sandboxed environment with no such service running. Either provision a real, lightweight MongoDB instance (e.g., via docker-compose) for route-level test verification, or restructure route tests to use mongomock the same way the DAO tests do, and flag any remaining live-dependency tests explicitly as requiring a different verification environment.
