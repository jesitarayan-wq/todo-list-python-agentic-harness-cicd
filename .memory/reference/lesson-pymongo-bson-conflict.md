---
classification: internal
project: proj-lessons
doc_type: lesson
---

## Lesson: A Standalone bson Package Breaks pymongo's Bundled bson

**What happened:** While debugging a failing test environment, `pip uninstall bson` was run to try to resolve an import conflict, assuming `bson` was an independent package. This actually deleted pymongo's own bundled `bson` submodule, since `pymongo` ships its own internal `bson` implementation and a standalone `bson` package on PyPI can shadow or conflict with it. The result was `ModuleNotFoundError: No module named 'bson'` even after `pymongo` itself showed as correctly installed.

**What was learned:** Some Python packages bundle an internal module that shares a name with a completely separate, independently-installable package on PyPI. Uninstalling what looks like a redundant or conflicting package can actually remove functionality a different, unrelated-looking package depends on internally.

**How to apply this lesson:** Before uninstalling any package to resolve a conflict, check whether another installed package depends on a module of the same name internally (e.g., via `pip show` and reading the dependency tree), not just whether the package appears redundant. If this specific conflict recurs, the fix is `pip install --force-reinstall --no-deps pymongo==<version>` to restore pymongo's bundled bson, rather than reinstalling a standalone bson package.
