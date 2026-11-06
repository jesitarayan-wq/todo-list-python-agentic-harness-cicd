# Reliability and cost controls

## Implemented (evidence in repo)
- Per-call output cap: scripts/run-reviewer.py sets max_tokens 1200 on the review call.
- Per-call timeout: scripts/run-reviewer.py uses a 90 s timeout; eval/test_rubric_suite.py uses a 180 s timeout on the judge call.
- Latency budget: eval/test_deterministic.py check "latency" fails a run over 300 s (MAX_DURATION_SECONDS). HO-02 failed it at 356 s.
- Escalation guard: .claude/agents/orchestrator.md halts and escalates to a human if the same phase fails its gate twice in a row.
- Fail-safe advisory step: the CI advisory-review job has continue-on-error: true, and run-reviewer.py exits 0 and writes "No review was performed" when no key is present.
- Gates that block: required checks in the protect-main ruleset (Policy Test Suite, Evaluation Harness, Pipeline Integrity Check).
- Retries with backoff: scripts/run-reviewer.py retries a failed model call up to 3 times (rate limits, server errors, timeouts and network errors; never a client error such as 401), doubles the wait each time, and records every attempt in the review output. Scope: the CI advisory review call only. Tested in eval/test_reviewer_retries.py with a fake sender.
- Per-run token budget and hard stop: the same script counts the largest answer each attempt could use against a budget of 3600 tokens (REVIEW_TOKEN_BUDGET) and makes no further attempt when the next one would exceed it. Scope: the CI advisory review call only; the budget guards in the live agent run were manual. Tested in eval/test_reviewer_retries.py.

## Planned, not built
- Rate limiting of agent calls.
- Max-iteration guard on loops other than the two-failure halt.
- Fallback to deterministic behavior when an agent step fails.

## Cost evidence
Only measured costs are in docs/baseline-measurements.md: Run 002 cost $0.27 (355.2k input, 4.4k output tokens). Run 001 cost was not captured. No cost has been measured for the 8-role pipeline, because no live end-to-end run or API key exists.

## Limits
The 300 s budget was set for scripted runs and was exceeded by a 4-role interactive run (HO-02), so it may need review.
