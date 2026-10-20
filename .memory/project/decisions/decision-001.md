# Decision 001 - Integer Priority Field on Task

**Date:** 2026-09-29
**Review by:** 2026-12-28
**Status:** Active

**Decision:** Priority is stored as an integer (1=high, 2=medium, 3=low) on Task, defaulting to 2 (medium) if not provided on POST.

**Rationale:** MongoDB's native sort would give incorrect results with string values like "high"/"medium"/"low" since alphabetical order does not match priority order, and an integer sorts correctly with no translation layer needed. This solves the problem of needing correct priority-based ordering directly via the database's sort, keeping query logic simple.

**Alternatives rejected:** A string enum was considered but rejected because it would require either a Python-side sort after materializing the cursor, or a second stored numeric rank field alongside the string -- both add complexity the integer approach avoids.
