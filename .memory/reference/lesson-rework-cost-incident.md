---
classification: confidential
project: proj-lessons
doc_type: finance
---

## Confidential: Cost Impact of the Stale-Memory Incident

**What happened:** During internal testing of the memory system, a stale decision entry was deliberately (and separately, once accidentally in an earlier draft of this exercise) left uncorrected for a period, leading to an estimated 6.5 hours of engineering time being spent re-diagnosing a decision that had already been made and documented, before the stale-memory detection safeguard was strengthened. At an internal blended engineering rate, this represented approximately $780 in avoidable rework cost for this single incident.

**What was learned:** Stale memory entries carry a real, quantifiable cost in engineering time, not just an abstract "confusion" risk. This specific incident is being used internally to justify continued investment in the stale-memory detection and review-date enforcement tooling.

**How to apply this lesson:** This cost figure is for internal budgeting and prioritization discussions only. It must not be included in any lesson, documentation, or report made available to coding or review roles, since it is an internal financial estimate rather than a technical or process lesson. Access to this document should remain restricted to roles with confidential-level clearance only.
