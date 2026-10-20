# Decision 002 - Test Files Organized in Separate /tests Directory

**Date:** 2026-09-29
**Review by:** 2026-12-28
**Status:** Active

**Decision:** Test files are organized in a separate `/tests` directory rather than alongside their corresponding source files.

**Rationale:** Keeping tests in a dedicated directory separates test code from application code, making the source tree easier to navigate and keeping the top-level project layout uncluttered as more test files are added.

**Alternatives rejected:** Co-locating test files next to the source files they cover (e.g. `task.py` and `test_task.py` in the same directory) was considered but rejected in favor of the dedicated `/tests` directory.

**Implemented:** 2026-09-29 -- `test_todo.py` was moved from the project root into `/tests` (alongside `test_task.py`), completing this decision. See [[decision-003]] for a sys.path issue this move exposed and how it was fixed.
