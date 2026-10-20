# Technique Plan: Test Coverage Analysis Session

## Explicit Context Boundary

**Location:** Immediately after Phase 1 (task.py/TaskDAO analysis) completes, before starting Phase 2 (todo.py/Flask routes analysis).

**What will be explicitly stated at this boundary:**
- That Phase 1 is complete: TaskDAO coverage analysis finished, recommendations produced.
- What Phase 2 focuses on: analyzing todo.py's Flask routes against test_todo.py.
- Requirements that remain active: still read-only analysis; still recommending specific tests, not writing them; still comparing actual code behavior against actual test coverage.
- Requirements that have changed: security/input-validation/access-control coverage gaps must now be prioritized higher than general gaps, due to planned upcoming authentication work.
- Information from Phase 1 that still matters: the Phase 1 recommendations list itself, which will be revisited later under the new priority rule.

**Why this technique here:** This is the exact point where a rule changes and the task shifts to a new file/scope -- precisely the kind of moment the lesson identified as most valuable for a boundary, since it prevents the agent from either forgetting the new priority rule or losing track of what Phase 1 already covers.

## Proactive Summarization

**Location:** Immediately before asking the agent to revisit and re-prioritize the Phase 1 recommendations list under the new security-focused priority rule (after Phase 2's analysis is complete).

**What the summary will capture:**
- Current goal: finalize a single, consistent, correctly-prioritized test coverage recommendation list across both files.
- Active requirements: security/input-validation gaps prioritized higher; read-only analysis; specific, actionable test recommendations.
- Decisions made so far: Phase 1's original recommendations (to be explicitly restated verbatim in the summary, not paraphrased) and Phase 2's recommendations.
- Current state of the artifact: the two separate recommendation lists as they currently stand.
- Unresolved questions: whether any Phase 1 items should change priority tier under the new rule.
- Next planned action: re-prioritize Phase 1's list under the new rule, then produce one final, combined, consistently-prioritized list.

**Why this technique here:** This is a natural breakpoint (analysis phase complete, about to move into revision/finalization) and is specifically designed to test whether the agent can accurately recall its own earlier output (Phase 1's list) rather than reconstructing or inventing it -- directly informed by the confabulation risk observed in the lesson's summarization run.

## Compaction

Compaction will be used only if the context window becomes crowded during the session, and only as a fallback -- it is not a planned, deliberate step in this session, consistent with the lesson's guidance that compaction is a last resort rather than a strategy.
