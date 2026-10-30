# ADR-008: Per-role MCP allow-lists, classification ceilings, and a hard-stop memory hook

## Status
Accepted

## Context
Storage and retrieval hold data of different sensitivity. docs/memory-architecture.md separates soft guards from one hard stop.

## Decision
Check every MCP request by role and classification ceiling, log refusals, and block credential-shaped values in .memory/ with a pre-commit hook.

## Alternatives considered
- Rely on the CLAUDE.md write policy only. Rejected: docs/memory-architecture.md records that the policy refused once but had to be overridden to reproduce the mistake, so judgment alone is not a sufficient backstop.
- One shared allow-list for all roles. Rejected: per-role tests showed the planner denied write_entry and the implementer denied delete_entry (logs/storage-audit-log.jsonl).

## Consequences
A mechanical check that does not depend on agent judgment. Limit: .git/hooks is not version-controlled and does not travel with clones.

## Evidence
docs/memory-architecture.md (Enforcement, Why this exists notes); logs/storage-audit-log.jsonl.

## Open risks
The reference memory layer was never populated; stale-entry and scope checks are soft guards.
