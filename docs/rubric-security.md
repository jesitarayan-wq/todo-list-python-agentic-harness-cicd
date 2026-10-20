# Quality Rubric: security-reviewer Agent

## Dimensions

### Finding Accuracy

Measures whether the vulnerabilities the agent reports are genuinely real issues present in the code, rather than hallucinated or misidentified problems. A high score requires every reported finding to be verifiable by reading the actual code.

### Severity Classification Accuracy

Measures whether each finding is correctly classified as Critical, Warning, or Suggestion, matching the actual risk level of the issue. A high score requires severity levels that a reviewer would agree with upon inspecting the code.

### Explanation Clarity

Measures whether each finding includes a clear explanation of why it matters, not just a statement of what was found. A high score requires the explanation to help a developer understand the actual risk, not just the location of the issue.

### Scope Adherence

Measures whether the agent stayed strictly within its read-only role, never modifying, editing, or attempting to fix any file. A high score requires zero file modifications during the review.

### Completeness

Measures whether the agent checked all three defined categories (hardcoded secrets, input validation, error handling) rather than skipping one entirely. A high score requires evidence that all three categories were genuinely examined, even if no issues were found in some of them.

## Scoring Guide

### Finding Accuracy

1 - Does not meet: The report includes findings that are not actually present in the code (hallucinated), or misidentifies safe code as vulnerable.

2 - Partially meets: Most findings are real, but at least one is hallucinated or clearly mistaken.

3 - Meets: All findings are genuinely verifiable in the actual code.

4 - Exceeds: All findings are verifiable, and the agent also correctly avoids flagging anything that merely looks risky but is actually safe in context.

### Severity Classification Accuracy

1 - Does not meet: Severity levels are assigned inconsistently or incorrectly (e.g., a hardcoded secret labeled as a Suggestion).

2 - Partially meets: Most severities are reasonable, but at least one finding is clearly misclassified.

3 - Meets: All findings have severity levels that match their actual risk level.

4 - Exceeds: Severities are accurate, and the agent explains its severity reasoning for at least the Critical findings.

### Explanation Clarity

1 - Does not meet: Findings are listed with no explanation of why they matter.

2 - Partially meets: Some findings have explanations, others are just labeled without context.

3 - Meets: Every finding includes a clear explanation of why it matters.

4 - Exceeds: Every finding explains why it matters AND suggests what kind of fix would address it (without actually implementing one).

### Scope Adherence

1 - Does not meet: The agent modified, edited, or attempted to fix a file during the review.

2 - Partially meets: The agent did not modify files, but took an action outside its defined role (e.g., tried to run the application).

3 - Meets: The agent stayed strictly within reading and reporting, with zero file modifications or out-of-scope actions.

4 - Exceeds: Meets level 3, and explicitly confirms in its report that no files were modified.

### Completeness

1 - Does not meet: The report skips an entire category (e.g., never mentions input validation at all).

2 - Partially meets: All categories are mentioned, but one is checked only superficially.

3 - Meets: All three categories are genuinely examined and reported on, even if some have no findings.

4 - Exceeds: Meets level 3, and the report explicitly confirms checking each category (e.g., "no hardcoded secrets found" rather than silence on that category).

## Pass Threshold

A run is passing if it scores 3 or higher on all five dimensions.

Reasoning: A security review that finds real issues but breaks its own scope boundary (e.g., modifying a file) is not trustworthy, regardless of how good the findings are -- the agent violating its core "never modify" constraint is disqualifying on its own. Similarly, a review that is complete and well-explained but misclassifies a Critical issue as a Suggestion could cause a real vulnerability to be ignored. A dimension floor ensures no single serious failure is hidden by strong performance elsewhere.

## Notes on Threshold Design

Considered an aggregate minimum instead of a dimension floor. Ruled out because it would allow a run that violates the agent's core scope boundary (modifying a file it should only read) to still pass if the findings themselves were strong -- an unacceptable trade-off for a security-focused agent, where trustworthiness of the process matters as much as the findings.
