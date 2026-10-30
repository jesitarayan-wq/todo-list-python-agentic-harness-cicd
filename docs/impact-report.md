# Impact report: baseline vs after, and tool-evolution drill

## Scope and honesty note
Delivery path: no-deployment. The Module 1 baseline measured a different task (unit tests for module_x.py), so comparisons are by metric type, not like for like. No live end-to-end run of the 8-role pipeline exists (no API key; the orchestrator has no shell tool), so there is no cost or cycle time for the full pipeline. Proxies are named below.

## Baseline (docs/baseline-measurements.md)
| Metric | Run 001 | Run 002 |
|---|---|---|
| Rubric total | 12/12 | 11/12 |
| Cycle time | 18 min 8.375 s | 2 min 47.143 s |
| Review latency | about 10-15 min (estimate) | about 10 min (estimate) |
| Cost per run | not captured | $0.27 (355.2k in / 4.4k out tokens) |

## After: what was measured
| Metric | Result | Source |
|---|---|---|
| Quality (holdout, 7 tasks) | HO-01 11/11 deterministic and rubric 4/4 (9/9), the only fully clean task; HO-03 11/11, rubric 3/4 (aggregate 9/9); HO-04, HO-06, HO-07 11/11 but weak (records reconstructed, rubric 1/4: 6/9, 6/9, 5/9) | docs/calibration-log.md lines 63-69 |
| Cycle time | HO-02 took 356 s, over the 300 s budget (4 sequential agents) | calibration-log.md line 64 |
| Review latency | Not re-measured; baseline estimates only | baseline file |
| Cost per run | Not measured for the pipeline; baseline $0.27 only | baseline file |
| Defect rate | Not measured directly. Proxy: defects caught by gates, namely the reviewer/security-reviewer name mismatch (Cycle 1), 1 policy test failure from a revoked grant, 2 policy failures from an over-grant, and an integrity-job failure (CI #13) | calibration-log.md, drill record, CI runs |
| Governance | 37 policy checks pass | eval/test_policy.py |
| Retrieval | 5/7 (71.4%) first run, below the 80% floor; 7/7 after fix | docs/lessons-learned-retrieval-validation.md |
| Deterministic conversion | Handoff check about 0.18 s (0.193, 0.170, 0.175), identical output on three runs, zero tokens, 15 unit tests; no agent baseline exists | calibration-log.md, ADR-003 |

## Tool-evolution drill (docs/tool-evolution-drill.md)
- Change: removed implementer from write_entry in the storage allow-list (throwaway branch).
- Broke: policy and allow-list disagreed.
- Detected: 1 failed, 36 passed (test_storage_allowlist_matches_policy[implementer]). I had predicted 2 failures; the over-grant test checks the opposite direction.
- Fix: restored the allow-list (policy authoritative). Final: 37 passed.
- Limit: tests policy-versus-config only, not a model swap or live tool-interface change.

## What improved, and what did not
Improved: failures that used to pass silently (name mismatch, policy drift, weakened gates) are now caught by tests and CI. Not improved or unproven: end-to-end quality, cost and cycle time of the full pipeline; the AI review and rubric in CI have never run.

## Next evidence to gather
A live end-to-end run with an API key, three repeat runs of the handoff check as an agent for a true before/after, and a second calibration cycle.
