# A safer team of AI helpers for the to-do API

Sagaya Jesita Maria Sarath Raj · 2026-11-05

## The problem

AI helpers can make quiet mistakes that nobody notices until they cost real time to fix. In our own testing, one helper was blocked from reading files because of a name mismatch, yet every automated test still passed. Without extra checks, that mistake would have shipped unseen.

## What we built

A team of eight AI roles that work on a small to-do application, with safety checks built into how they work, not left to good intentions.

- **Each role gets only the access its job needs.** The reviewer can read code but cannot change it; only the ticket role can update tickets.
- **Every change is checked automatically.** 52 checks pass today, and a change cannot reach the main code unless three required checks pass.
- **A record is kept.** Refused actions are logged, so a manager can see what was tried and what was blocked.

## What it could save (a projection)

As a projection, for a team making 10 changes a week, catching half of the quiet mistakes early would save about 0.75 hours and $37.50 a week, or roughly $1,875 a year.

| Item | Value | Basis |
| --- | --- | --- |
| Engineer time | $50 per hour | Assumption |
| Changes made per week | 10 | Assumption |
| Changes hiding a quiet mistake | 1 in 20 | Assumption; one real miss is not a rate |
| Hours to fix a mistake caught late | 3 | Assumption |
| Share caught early by the checks | Half | Assumption; an early catch is assumed to cost almost nothing to fix |
| Defects avoided | 0.25 per week, about 12 per year | Projection |
| Hours saved | 0.75 per week, about 38 per year | Projection |
| Dollars saved | About $37.50 per week, about $1,875 per year | Projection |
| Running cost of one security review per change | About $2.90 to $3.20 per week | Measured cost of one review run, times 10; a full run was measured once, with one session uncosted |

These figures come from assumptions, not measurements. Replace the assumptions with your own team's numbers to get your own estimate.

## Proof it works

52 automated checks pass, and each safety layer has a recorded case of blocking something:

- The reviewer tried to create a file and the system refused it, because its workspace is read-only.
- A deliberately wrong permission change turned the checks red.
- A deliberately weakened safety check was caught by a second check.
- A direct change to the main code was rejected; every change must pass three required checks.

Separately, the lookup of past lessons passed 5 of 7 tests at first and 7 of 7 after a fix.

## Risks managed, and honest limits

The controls reduce three risks, and five limits remain.

Risks managed:

- An AI helper changing something outside its job.
- A bad change reaching the main code.
- Secrets or sensitive data ending up in shared files; none appear in anything submitted.

Limits:

- The full team has run live once, but one of its sessions was not costed, so its total cost is not known.
- The automated AI code review has never run, because no access key was set up.
- The tool that runs tests now runs the mock-based tests of the app for real; tests that need a live database are not run.
- One automatic check can report success even when what it runs fails. The fix is known and not yet applied.
- Everything ran on a sample project, not company data. A real rollout would need approvals and cleaned data.

## Next steps

The next step is a small trial that turns the assumptions above into measurements.

1. Repeat the full-team run, recording the cost of every session.
2. Fix the known check gap and limit the working environment's network access.
3. Try it on a team's real changes for a few weeks and count the real mistakes it catches.

To start, a decision-maker would need to approve the trial and provide access for the AI code review.
