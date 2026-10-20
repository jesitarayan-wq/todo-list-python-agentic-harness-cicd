# Project Memory Index

Last updated: 2026-10-01 (decision-003 reconfirmed, review date extended)

## Active entries

- `decisions/decision-001.md` — Records the decision to store Task priority as an integer (1=high, 2=medium, 3=low, default 2) rather than a string, so MongoDB's native sort produces correct priority order. Recorded 2026-09-29.
 Review by 2026-12-28.

- `decisions/decision-002.md` — Records the decision to organize test files in a separate `/tests` directory rather than alongside their source files. Recorded 2026-09-29, implemented 2026-09-29 (test_todo.py moved into /tests).
 Review by 2026-12-28.

- `decisions/decision-003.md` — Records adding root-level `pytest.ini` with `pythonpath = .` so tests in `/tests` can import `task`/`todo` under plain `pytest` invocation, not just `python -m pytest`. Recorded 2026-09-29, reconfirmed 2026-10-01.
 Review by 2026-12-30.

- `decisions/decision-004.md` — Records that the priority feature (storage, defaulting, validation) is functionally complete across task.py/todo.py and both test files; backfill and update()/PUT remain deferred (not implemented, not formally scoped in decision-001). Recorded 2026-09-29.
 Review by 2026-12-28.

- `../knowledge/coding-standards.md` — Coding standards
 covering: validation belongs in the route layer not the
 DAO; new fields must be explicitly whitelisted in
 TaskDAO.create(); boolean values must be excluded when
 validating numeric-range fields; Flask routes must return
 status codes matching the actual outcome; no hardcoded
 MongoDB connection strings; new DAO methods need tests in
 tests/test_task.py using mongomock. Human-maintained,
 read-only. Last reviewed 2026-09-29.

- `decisions/decision-005.md` — Records the decision to connect to the data API using a service account, with the key referenced only via the ANTHROPIC_API_KEY environment variable (never hardcoded in memory, knowledge, or code). Recorded 2026-10-01.
 Review by 2026-12-30.

## Archived entries

(none yet)

## Pruning schedule

- Workflow-scoped entries: archived when the branch
 merges to main
- Project-scoped entries: reviewed every 90 days
