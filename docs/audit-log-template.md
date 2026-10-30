# Audit log template

Format: JSON Lines, one object per event. Real files: logs/storage-audit-log.jsonl, logs/retrieval-audit-log.jsonl.

Fields (as written by the MCP servers):
- timestamp: ISO 8601 UTC
- event: storage_write, authorization_denied, classification_withheld
- operation: write_entry, delete_entry, retrieve, ...
- role: the calling role
- outcome: success, authorization_denied, classification_withheld
- detail: extra text or null
- policy_reference: docs/governance-policy.md

Example: {"timestamp": "2026-10-21T16:02:13+00:00", "event": "authorization_denied", "operation": "delete_entry", "role": "implementer", "outcome": "authorization_denied", "detail": null, "policy_reference": "docs/governance-policy.md"}

Not yet logged: human approvals, retries, rollbacks. The CI audit trail (ci-audit-trail-<sha>.json) holds job results but not MCP denials.
