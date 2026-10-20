# Decision 003 - pytest.ini with pythonpath = . for /tests Imports

**Date:** 2026-09-29
**Review by:** 2026-12-30
**Status:** Active (reconfirmed 2026-10-01: pytest.ini still present at repo root with `pythonpath = .`, /tests still has no `__init__.py`; no changes since original decision)

**Decision:** Added a root-level `pytest.ini` with `pythonpath = .` so that test modules under `/tests` (which has no `__init__.py`) can `import task` / `from todo import app` regardless of how pytest is invoked.

**Rationale:** Per [[decision-002]], test files live in `/tests`, separate from the source files they cover. When pytest is invoked via the plain `pytest` console script (as `.travis.yml` does), pytest does not add the project root to `sys.path`, so `from task import TaskDAO` / `from todo import app` fail with `ModuleNotFoundError`. This only appeared to work when invoking `python -m pytest`, since `-m` adds the current working directory to `sys.path[0]` as a side effect unrelated to pytest itself. The `pythonpath` ini option (pytest >= 7) explicitly adds the project root to `sys.path` for every invocation style, fixing the root cause rather than relying on incidental behavior of one invocation form.

**Alternatives rejected:** Adding an `__init__.py` to `/tests` was considered -- this makes pytest walk up to find a directory without `__init__.py` (the project root) and insert *that* into `sys.path`, which also works. Rejected in favor of `pythonpath = .` because it does not change `/tests` into a package (avoiding import-mode subtleties) and is a single explicit, discoverable line in `pytest.ini`.
