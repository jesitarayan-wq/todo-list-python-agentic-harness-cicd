# Impact report: baseline versus after, and the tool-evolution drill

Sagaya Jesita Maria Sarath Raj · 2026-11-05

## At a glance

Failures that used to pass silently are now caught by tests and CI, and one live run of the full team now exists (docs/live-run-record.md), but it is a single run, one session cost was not captured, and review time and defect rate are still not measured.

- **Measured:** 52 automated checks pass; retrieval went from 5/7 to 7/7 after a fix; a revoked permission was caught by exactly one failing policy test (36 passed, then 37 after the fix); the handoff check as code runs in about 0.18 s with zero tokens.
- **Two improvement cycles, each confirmed by a rerun:** the reviewer authorization fix, and the retrieval fix (details below).
- **Not measured:** review latency and defect rate; full-pipeline cost and cycle time are only partly measured (one governed run). The table below marks each one as measured, a proxy, or not yet measured.

Scope: delivery path is no-deployment on a representative to-do API. The Module 1 baseline measured a different task (unit tests for `module_x.py`), so comparisons are by metric type, not like for like.

## Baseline versus after

Of the five measures, quality is measured, defect rate and cost have proxies, review latency is not measured, and full-pipeline cycle time is partly measured (one governed run).

| Measure | Baseline (Module 1, different task) | After | Status |
| --- | --- | --- | --- |
| Quality | Run 001: rubric 12/12. Run 002: rubric 11/12 | Holdout, 7 tasks: HO-01 passes 11/11 checks and rubric 4/4 (9/9); HO-03 11/11, rubric 3/4 (9/9); HO-04, HO-06, HO-07 pass 11/11 checks but are weak (records reconstructed, rubric 6/9, 6/9, 5/9) | Measured. Only HO-01 is fully clean |
| Review latency | About 10 to 15 min (Run 001), about 10 min (Run 002), both estimates | Not re-measured | Not measured |
| Defect rate | Not available | Not a rate. Defects the gates caught: the reviewer name mismatch, 1 policy failure from a revoked grant, 2 from an over-grant, 1 integrity-job failure (CI #13) | Proxy |
| Cycle time | Run 001: 18 min 8.375 s. Run 002: 2 min 47.143 s | HO-02 took 356 s, over the 300 s budget (4 sequential agents). Handoff check as code: about 0.18 s; the same check by an agent: 40 to 65 s wall, three runs. One governed run on 2026-11-06: about 17 minutes wall time including approvals, against about 3 minutes for a plain agent on the same task (one run each) | Partly measured |
| Cost per run | Run 001: not captured. Run 002: $0.27 (355.2k in, 4.4k out tokens) | One governed run: $0.53 for the second session; the first session (planner and implementer) was not captured, so there is no total. A plain agent on the same task: $0.3599. Single review runs this month: $0.32 and $0.29 (security review, two versions), $0.25 (lint review). Handoff check as code: zero tokens; the same check by an agent: about $0.10 to $0.16 per session, three runs | Proxy |

The single-run costs are session totals read from the Claude Code usage screen on 2026-11-05. They include the main session's own turns and a warm prompt cache, so they show the order of magnitude of one agent step, not the cost of the pipeline.

## Cycle time across the seven holdout tasks

Run time in seconds, from the saved holdout run records. HO-04, HO-06 and HO-07 are reconstructed records.

| Task | Seconds | Within the 300 s budget |
| --- | --- | --- |
| HO-01 | 12 | Yes |
| HO-02 | 356 | No, over by 56 s (4 sequential agents) |
| HO-03 | 110 | Yes |
| HO-04 | 165 | Yes |
| HO-05 | 36 | Yes |
| HO-06 | 82 | Yes |
| HO-07 | 102 | Yes |

## Two improvement cycles, each confirmed by a rerun

Both changes were made because a check failed, and both were confirmed by running the same checks again.

| Cycle | Evidence that triggered it | Change | Rerun result |
| --- | --- | --- | --- |
| 1. Reviewer authorization | A development run passed the original 10 checks, but a new denied-tool-call check failed on 3 calls: the security-reviewer was blocked from reading files because the server's lists named the role differently from the agent | Added security-reviewer to the file_read and codebase_search allow-lists (commit `280f176`); no write, shell, test or ticket access was granted | Next development run passed 11/11 checks with rubric aggregate 9 (one dimension still below threshold); HO-01 then passed 11/11 and rubric 4/4 |
| 2. Retrieval quality | Ground-truth set passed 5 of 7 (71.4%), below the 80% floor; one lesson was found only through keyword fallback | Restructured paragraphs in two corpus documents; the expected answers were not changed | 7 of 7 (100%) on the same queries and threshold |

Limit: the reruns used the same development tasks and ground-truth set, not a fresh locked holdout. Sources: `docs/calibration-log.md` and `docs/lessons-learned-retrieval-validation.md`.

## Tool-evolution drill

Revoking one storage permission on a throwaway branch was caught by exactly one failing policy test, and restoring it brought the suite back to 37 passing.

| Stage | What happened |
| --- | --- |
| Change attempted | Removed the implementer from write_entry in the storage allow-list |
| What broke | The allow-list and the written policy disagreed |
| What the harness detected | 1 failed, 36 passed: `test_storage_allowlist_matches_policy[implementer]`. I had predicted 2 failures; the over-grant test checks the opposite direction |
| What improved | The disagreement was caught by a check before any agent used the wrong grant |
| Fix | Restored the allow-list; the policy is authoritative |
| Final result | 37 passed |

Limit: the drill tests policy against configuration only. It is not a model swap or a live tool-interface change. Full record: `docs/tool-evolution-drill.md`.

## Measured gains versus projected gains

Everything above is measured. The figures below are projections from stated assumptions, and a reader should replace the assumptions with their own team's numbers.

| Item | Value | Basis |
| --- | --- | --- |
| Engineer time | $50 per hour | Assumption |
| Changes made per week | 10 | Assumption |
| Share of changes hiding a quiet mistake like the reviewer name mismatch | 1 in 20 | Assumption; one real miss is not a rate |
| Time to find and fix such a mistake when caught late | 3 hours | Assumption |
| Hidden mistakes per week | 0.5 (10 ÷ 20) | Derived |
| Cost of those mistakes if caught late | 1.5 hours, about $75 per week | Derived |
| Saving if the checks catch half of them early | 0.75 hours, about $37.50 per week, about $1,875 per year (50 weeks) | Projection; assumes an early catch costs almost nothing to fix |
| Cost of one security review per change | 10 × $0.29 to $0.32, about $2.90 to $3.20 per week | Measured run cost, assumed one review per change; excludes the rest of the pipeline |

The projection is only as good as its assumptions. What would make it a measurement is more live runs that record the full-pipeline cost, now that one exists with one session uncaptured, plus a count of defects over a period of real changes.

## What is not measured yet, and how each gap closes

Five gaps remain; one of them, the handoff check comparison, is now measured on one input.

| Gap | How it closes |
| --- | --- |
| Full-pipeline cost and cycle time | Partly measured on 2026-11-06 (one governed run and one plain-agent baseline; see docs/live-run-record.md). Still open: the first session cost was not captured, and one run is not a rate. Repeat with the cost of every session recorded |
| Review latency | Time a human reviewer on the same runs |
| Defect rate | Count defects found over a period of real changes, with the checks on |
| Handoff check, agent versus script | Measured on 2026-11-05: three agent runs on one input, given only the schema, each judged the bad document valid while the script rejects it (agent 40 to 65 s and about $0.10 to $0.16 per session; script about 0.18 s and zero tokens). Still open: more inputs, and an end-to-end run. ADR-003 stays Proposed until the script is wired into a running workflow |
| Holdout evidence for HO-04, HO-06 and HO-07 | Those records were reconstructed after early exits. A fresh run that saves every tool call as it happens replaces them |

Also still open: the AI review and the rubric scoring in CI have never run, because no API key was registered.
