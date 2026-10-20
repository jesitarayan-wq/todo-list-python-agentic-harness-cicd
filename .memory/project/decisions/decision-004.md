# Decision 004 - Priority Feature Functionally Complete

**Date:** 2026-09-29
**Review by:** 2026-12-28
**Status:** Active

**Decision:** The priority feature is functionally complete. `task.py` (integer priority field, defaulting per [[decision-001]]) and `todo.py` (route-level validation rejecting missing-range, non-numeric, and boolean priority values) fully implement priority storage, defaulting, and validation. `tests/test_task.py` and `tests/test_todo.py` fully cover this behavior at both the DAO and route layers, per [[decision-002]] and [[decision-003]] for test file location and import setup.

**Rationale:** Storage, defaulting, and validation were the scope needed to make priority usable end-to-end through the existing API surface (`POST /tasks`, `GET /tasks`). That scope is now implemented and tested, so the feature is complete for its current surface area.

**Alternatives rejected:** N/A -- this is a status record, not a choice between alternatives.

**Deferred (intentionally out of scope):**
- Backfilling `priority` onto existing documents created before this field existed.
- Implementing `TaskDAO.update()` and the `PUT /tasks/<pk>` route (both currently `pass`/unimplemented), which would allow changing priority after creation.

Note: [[decision-001]] itself only records the integer-vs-string storage rationale and does not explicitly discuss backfilling or `update()`/PUT -- these two items are deferred by omission (they were never implemented, and `TaskDAO.update()`/`PUT /tasks/<pk>` remain `pass`/no-op stubs in the current code), not by an explicit statement in decision-001. Neither is required for priority to function on creation, listing, and validation.
