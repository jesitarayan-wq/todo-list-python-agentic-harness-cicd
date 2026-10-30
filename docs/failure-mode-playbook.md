# Failure-mode playbook

Each entry: recognize it, what detects it in this repo, first response, fix layer. Sources: docs/calibration-log.md (NM-1 to NM-6), Module 3 delegation failures, Module 2 memory failures.

## Governance and harness failures
| Failure | Recognize | Detected by | First response | Fix layer |
|---|---|---|---|---|
| NM-1 names drift between layers | A role is blocked or ungoverned; run still passes | eval/test_policy.py; check_no_denied_tool_calls | Compare role names in agent file, grant map, allow-lists | Tool (allow-list) |
| NM-2 declared tool nothing verifies | Agent file lists a tool no policy grants | Policy review; (not yet automated) | Remove the entry | Agent definition |
| NM-3 no limit on where roles write | New directories or memory edits by implementer | Docker read-only mounts; diff review | Reset the files, check run-agent.sh branch | Container |
| NM-4 gate that cannot fail | Placeholder PASS from test_runner; vacuous checks | Manual review of records | Treat result as unverified | Tool |
| NM-5 denial vs error look alike | no_denied_tool_calls flags an ordinary error | Harness output | Read the error text before concluding | Check logic |
| NM-6 self-reported evidence | Missing or reconstructed run records | Provenance notes | Mark record as reconstructed | Harness design |

## Delegation failures
| Failure | Recognize | First response |
|---|---|---|
| Routing misfire | Role skipped or out of order | Check orchestrator routing rule; rerun |
| Output format mismatch | Handoff cannot be parsed | Run scripts/validate_handoff_deterministic.py |
| Over-broad tool grant | Role calls a tool it did not need | Compare against docs/governance-policy.md |
| Context bleed | Subagent knows something not in its handoff | Check handoff contents |

## Memory failures (Module 2)
| Failure | Recognize | First response |
|---|---|---|
| Stale entry treated as current | Entry contradicts code or git history | Verify with git diff; correct the entry |
| Scope leak | SCOPE.md does not match the repo | Halt; fix the mount |
| Sensitive data in storage | Credential pattern in .memory/ | Remove value, keep only the variable name; pre-commit hook |

## Escalation
If the same phase fails its gate twice, stop and escalate to a human (orchestrator rule). If policy and config disagree, fix one side only and rerun eval/test_policy.py.
