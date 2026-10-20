# Iteration Log: security-reviewer Agent

## Run 1 -- 2026-09-16 -- Baseline Run

### Run Metadata
- Agent: security-reviewer v0.1.0
- Skills active: none (agent invoked via natural-language delegation)
- Task: Review todo.py and task.py for security issues (hardcoded secrets, input validation, error handling).

### Rubric Scores
- Finding Accuracy: 4 -- All findings were specific, concrete, and verifiable (e.g., unvalidated pk passed to ObjectId(), unchecked request.json type, missing auth on all routes). Nothing appeared hallucinated or vague.
- Severity Classification Accuracy: 2 -- Most severities were reasonable, but "no authentication/authorization on any route" was labeled the same Warning severity as minor crash-causing bugs (e.g., malformed ID causing an uncaught exception). Missing auth entirely means zero access control on all data -- a more severe issue than an input-validation crash -- and should have been classified as Critical.
- Explanation Clarity: 4 -- Every finding explained the specific mechanism of the risk (e.g., "raises an uncaught InvalidId exception," "crashes with AttributeError"), not just a generic label.
- Scope Adherence: 4 -- Confirmed via `git status` after the run: zero files modified. The agent also explicitly asked before offering to implement any fixes, rather than assuming permission.
- Completeness: 4 -- All three defined categories were explicitly addressed: secrets (explicitly stated none found), input validation (multiple examples), and error handling (the missing try/except point).
- Total: 18/20 -- FAIL (Severity Classification Accuracy below the floor of 3, despite a strong overall review)

### Measurements
- Cycle time: ~48 seconds (per the agent's own reported tool-use duration; not independently timed with `date`)
- Review latency: ~10 minutes
- Cost: not captured this run
- Pass/Fail: FAIL

### Misfires
1. Severity under-classification: the agent's instructions ask it to classify findings as Critical, Warning, or Suggestion, but do not define what distinguishes a Critical issue from a Warning. Without explicit criteria (e.g., "missing authentication/authorization is Critical"), the agent applied Warning broadly to issues of clearly different real-world severity, treating "no access control on any route" the same as "a crash from malformed input."

### Proposed Fixes
1. File: `.claude/agents/security-reviewer.md` -- Add explicit severity criteria to the instructions, distinguishing Critical (e.g., missing authentication/authorization, exposed credentials, data exposure to any unauthenticated user) from Warning (e.g., crashes from invalid input, missing validation that does not expose data) and Suggestion (e.g., missing pagination, code style). Addresses the misfire directly by giving the agent a concrete rule to apply rather than relying on its own judgment alone.

### Changes Made
801aced -- agent: security-reviewer v0.2.0 (add explicit severity classification criteria)

## Run 2 -- 2026-09-16 -- Rerun after Fix 1

### Run Metadata
- Agent: security-reviewer v0.2.0
- Skills active: none (agent invoked via natural-language delegation)
- Task: Review todo.py and task.py for security issues (same task as Run 1, for direct comparison).

### Rubric Scores
- Finding Accuracy: 4 (was 4, no change) -- All findings remained specific and verifiable. The agent also surfaced a genuinely new, real issue not caught in Run 1: an IDOR vulnerability (any task readable by ID with no ownership check).
- Severity Classification Accuracy: 4 (was 2) -- FIXED. With explicit criteria now in the agent definition, "no authentication on any route" and the newly-found IDOR issue were both correctly classified as Critical, matching the intended severity. Warning and Suggestion items remained appropriately classified.
- Explanation Clarity: 4 (was 4, no change) -- Every finding continued to explain the specific mechanism of the risk (e.g., "falls through to None, causing an unhandled 500").
- Scope Adherence: 4 (was 4, no change) -- Confirmed via `git status`: zero files modified. The agent again asked before offering to implement fixes.
- Completeness: 4 (was 4, no change) -- All three categories explicitly addressed; secrets explicitly confirmed absent.
- Total: 20/20 -- PASS (all dimensions at or above the floor of 3; targeted dimension improved from 2 to 4 with no regressions elsewhere)

### Measurements
- Cycle time: ~55 seconds (per the agent's own reported tool-use duration; comparable to Run 1's ~48s)
- Review latency: ~8 minutes
- Cost: not captured this run
- Pass/Fail: PASS

### Comparison to Run 1
The targeted fix (explicit Critical/Warning/Suggestion criteria) directly resolved the Run 1 misfire: "no authentication on any route" is now correctly labeled Critical instead of Warning. No other dimension regressed, and the more precise criteria appear to have helped the agent identify an additional real issue (IDOR) that Run 1 did not surface, suggesting the clearer severity framework also sharpened what counted as worth flagging in the first place, not just how findings were labeled.

### Misfires
None identified this run.

### Proposed Fixes
None proposed this run -- all rubric dimensions passed.

### Changes Made
N/A (this run itself is the confirmation of the Run 1 fix; see Run 1's Changes Made field: 801aced -- agent: security-reviewer v0.2.0)
