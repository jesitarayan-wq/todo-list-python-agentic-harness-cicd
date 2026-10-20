# Iteration Log: security-reviewer Calibration (Module 2 Lab, Track 2)

## Run 1 -- v0.2.0 -- Baseline

Task: Review todo.py and task.py for security issues.
Result: 1 Critical (no auth), 5 Warnings (hardcoded connection string, unhandled PUT, unvalidated ObjectId, unvalidated request.json, no error handlers/debug=False), 3 Suggestions.
Observation: Findings correctly classified and explained, but the agent only flagged problems without stating what a safe fix would need to include.
Commit: 229ef9d (output saved to docs/security-reviewer-run1-output.md)

## Fix 1: v0.3.0

Change: Added step 6 requiring a one-sentence description of what a safe fix would need for each Critical/Warning finding, without implementing it.
Rationale: Run 1 showed the agent correctly identifies and classifies issues, but a developer reading the report still has to independently figure out what remediation would look like -- adding this makes the report immediately actionable.
Commit: f000615

## Run 2 -- v0.3.0

Task: Same as Run 1.
Result: Same 4 Critical/Warning findings (slightly consolidated), each with a safe-fix description, e.g., "an authentication/authorization check (e.g., verifying a session, token, or API key) performed before any DAO call in each route, rejecting unauthenticated requests with a 401/403."
Important finding: The orchestrating Claude Code session's FIRST relayed summary to the user omitted these safe-fix descriptions entirely, appearing as a regression. On inspection of the sub-agent's raw output directly, all 4 descriptions were genuinely present -- the gap was in how the summary was condensed, not in security-reviewer's own compliance. Lesson: verify sub-agent compliance against raw output, not a summary of it.
Commit: 8fe4315 (output saved to docs/security-reviewer-run2-output.md)

## Fix 2: v0.4.0

Change: Added step 7, a self-verification step: before finalizing, re-read the draft report and confirm every Critical/Warning finding includes its safe-fix description, adding any that are missing.
Rationale: Directly addresses the Run 2 finding -- rather than relying on the orchestrating session to faithfully relay compliance, the agent now explicitly states its own verification result as part of its visible output, making compliance evidence harder to lose in summarization.
Commit: 1057d29

## Run 3 -- v0.4.0

Task: Same as Runs 1-2, explicitly requesting complete raw output this time (applying the Run 2 lesson).
Result: Same 4 Critical/Warning findings, each with a safe-fix description, PLUS an explicit new line: "Self-verification: all 4 Critical/Warning findings include safe-fix descriptions (confirmed above)."
Commit: feb6f9d (output saved to docs/security-reviewer-run3-output.md)

## Comparison Across Versions

| Version | Findings quality | Safe-fix descriptions | Self-verification visible |
|---|---|---|---|
| v0.2.0 (Run 1) | Strong | No | N/A |
| v0.3.0 (Run 2) | Strong | Yes (confirmed via raw output) | No |
| v0.4.0 (Run 3) | Strong | Yes | Yes, explicitly stated |

## Conclusion

Across three runs, security-reviewer's core finding-and-classification quality remained consistently strong throughout. The calibration work specifically targeted REPORT ACTIONABILITY and COMPLIANCE VISIBILITY, not finding accuracy, which was never the weak point. The most valuable discovery of this calibration cycle was not a flaw in the agent itself, but a flaw in how an orchestrating session can silently misrepresent a sub-agent's genuine compliance through summarization -- this led directly to the v0.4.0 self-verification step, which makes the agent's own compliance explicitly visible rather than dependent on faithful relay by whatever session invokes it.
