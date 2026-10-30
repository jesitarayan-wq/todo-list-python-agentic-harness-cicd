# Stakeholder one-pager: a safer team of AI helpers for the to-do API

## The problem
AI helpers can make quiet mistakes. In our own testing, one helper was blocked from reading files because of a name mismatch, yet every automated test still passed. Nobody would have noticed.

## What we built
A team of 8 AI roles (planner, implementer, reviewer, tester and others) working on a small to-do API. Each role gets only the access it needs. Automatic checks run on every change, and a record is kept of what happened.

## Proof it works
- 52 automated checks pass.
- A deliberately bad permission change was caught by the checks.
- A deliberately weakened safety check was caught by a second check.
- Direct changes to the main code are blocked; every change must pass three required checks.

## Cost and savings
Only an early baseline exists: $0.27 for one run of a different task. The cost of the full 8-role pipeline has not been measured yet, and we do not claim savings.

## Risks and honest limits
- The full pipeline has not been run live from start to finish, and no API key was registered, so the AI code review has never run.
- The test tool used by the tester returns a placeholder result, so test outcomes are unverified.
- This ran on a representative sample project, not real company data. A real rollout would need approvals, sanitized data and a real test runner.

## Next steps
1. A live end-to-end run with an API key.
2. A second evaluation cycle to confirm results are stable.
3. A true before/after measurement for the automated handoff check.
