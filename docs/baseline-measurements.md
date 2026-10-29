# Module 1 baseline measurements

Source: ~/LaunchCodeAgenticEngineer/docs/iteration-log.md (Sandbox repo), Run 001 and Run 002. Figures copied as recorded. Task: write unit tests for module_x.py without modifying it. This is a different task from the capstone workflow (to-do API ticket-to-implementation), so comparisons are by metric type, not like for like.

| Metric | Run 001 (2026-08-21, baseline) | Run 002 (repeat) |
|---|---|---|
| Rubric total | 12 / 12 | 11 / 12 |
| Pass threshold | 3 or higher on all dimensions | same |
| Cycle time | 18 min 8.375 s (real) | 2 min 47.143 s (real) |
| Review latency | about 10-15 min (estimated) | about 10 min (estimated) |
| Cost per run | not captured (display showed $0.00 / 0 tokens under a subscription) | $0.27 (355.2k input / 4.4k output tokens, status bar) |
| Pass/Fail | Pass | Pass |

## Variance notes (from the log)
- Test Coverage Depth and Test Code Readability scored 4 in both runs.
- Report Clarity and Completeness dropped from 4 to 3 in Run 002 because the summary did not state that module_x.py was unmodified, although git diff confirmed it was.
- Cycle time varied far beyond the 50 percent concern threshold; the log attributes this mainly to the number of approval-gated steps, not task complexity.
- Run 001's wall time (18m 8s) was mostly approval prompts, not agent processing (the agent reported 57 s).

## Limits
- Cost cannot be compared: Run 001 has no captured cost.
- Review latency values are estimates.
- Defect rate was not recorded in either run; the impact report must name a proxy.
