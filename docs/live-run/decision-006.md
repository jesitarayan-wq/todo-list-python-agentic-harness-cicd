# Decision 006 - TaskDAO.update() Accepted; Route Auth Required Before PUT

**Date:** 2026-11-05
**Review by:** 2027-02-03
**Status:** Active

**Decision:** Run LIVE-01 (`TaskDAO.update(object_id, data)` in `task.py`, 15 `test_update_*` tests in `tests/test_task.py`) is accepted. Security review found no high-severity issues in the changed code; tester reported 31 passed, 0 failed. Human-approved deviations: `update()` rejects non-boolean `done` in the DAO (not the route layer), and priority is not validated in `update()`.

**Follow-up (must be fixed before any `PUT /tasks/<pk>` route is added):** No route in `todo.py` (lines 11-40) has authentication or authorization. This is pre-existing and was out of scope for LIVE-01, so the human decided it does not block acceptance and is tracked separately. Wiring PUT to `update()` without auth would expose an unauthenticated write path.

**Also required when PUT is added (route layer, per coding standards):**
- Reject a null or non-dict `request.json`; check title/description are non-empty strings.
- Catch `bson.errors.InvalidId` and `ValueError` and return 400/404 with a fixed message (never `str(e)` or a traceback).
- Map a `None` return from `update()` (unknown id) to 404.

**Rationale:** The auth gap predates this change and `todo.py` was not modified, so blocking the DAO work on it would conflate two tasks. Recording it here makes sure the PUT work picks it up.

**Alternatives rejected:** Blocking LIVE-01 acceptance until auth is added. Rejected by the human because it is outside the task's scope.

Related: [[decision-004]] (update()/PUT previously deferred).
