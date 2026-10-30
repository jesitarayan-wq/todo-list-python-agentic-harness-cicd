# Tool-evolution drill: revoke a permission

## Change attempted
On a throwaway branch (drill-revoke-write), removed "implementer" from write_entry in mcp-servers/storage/allow-list.json, simulating a revoked permission.

## What broke
The governance policy still granted write_entry to the implementer, but the allow-list no longer did, so policy and enforcement disagreed.

## What the harness detected
python3 -m pytest eval/test_policy.py: 1 failed, 36 passed. Failing test: test_storage_allowlist_matches_policy[implementer]; the assertion showed 'write_entry' as an extra item on the policy side.
Note: I predicted 2 failures. The over-grant test checks the opposite direction (list grants more than policy), so a revocation cannot trigger it.

## Fix
Restored the allow-list from git (policy treated as authoritative). Only one side was changed. If the revocation had been intentional, the policy row would change to NO with a justification instead.

## Final result
37 passed after the restore.

## Limits
This drill exercises the policy-versus-config check only. It did not swap a model or change a live tool interface, because there has been no live agent run (no API key; the orchestrator has no shell tool). The broken state was never committed to main.
