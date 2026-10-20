# Quality Rubric: Lint Summary

## Dimensions

### Issue Grouping by Category

Measures whether the agent correctly groups issues that share the same type or rule, rather than listing each occurrence individually. A high score requires all instances of the same issue type to be counted and presented together.

### Summary Clarity and Completeness

Measures whether the report clearly explains what linting was performed and gives a complete overview of everything found, without omitting any category of issue. A high score requires the summary to be understandable at a glance, covering every type of issue detected.

### Explanation Usefulness

Measures whether the summary explains what each type of lint issue means and why it matters, rather than just listing raw rule codes. A high score requires the agent to translate technical rule codes into plain-language explanations of the actual problem and its importance.

## Scoring Guide

### Issue Grouping by Category

1 - Does not meet: The summary lists each issue occurrence individually without grouping by type, and may miss some issues entirely.

2 - Partially meets: The summary groups some issues by type, but the grouping is incomplete or some issue types are left ungrouped.

3 - Meets: The summary correctly groups all issues by type, with accurate counts, but without additional explanation.

4 - Exceeds: The summary correctly groups all issues by type with accurate counts, and adds useful context (e.g., noting where issues are concentrated or patterns across the codebase).

### Summary Clarity and Completeness

1 - Does not meet: The report omits entire categories of issues that ruff actually found, or fails to state the total number of issues.

2 - Partially meets: The report mentions the overall issue count, but omits details on one or more issue categories, or is disorganized enough to require re-reading.

3 - Meets: The report clearly states the total number of issues and covers every category of issue found, in an easy-to-follow format.

4 - Exceeds: The report meets level 3, and also briefly notes anything unusual worth the developer's attention (e.g., one file having significantly more issues than another).

### Explanation Usefulness

1 - Does not meet: The summary lists raw rule codes (e.g., F401, E501) without any plain-language explanation of what they mean.

2 - Partially meets: The summary attempts a plain-language explanation, but it is vague or doesn't clarify why the issue matters.

3 - Meets: The summary translates each issue type into a clear, plain-language explanation of the problem and why it's worth addressing.

4 - Exceeds: The summary meets level 3, and also indicates which issues are most important to fix first, or connects the issue to a concrete consequence for the project.

## Pass Threshold

A run is passing if it scores 3 or higher on all three dimensions.

Reasoning: A lint summary that omits or mis-groups an issue category is misleading even if it's clearly explained, and a well-grouped summary that never explains why issues matter provides little practical value to a developer deciding what to fix. Since accurate grouping, completeness, and useful explanation are all essential for this report to be genuinely actionable, a dimension floor ensures no single weak area is hidden by strong performance elsewhere.

## Notes on Threshold Design

Considered an aggregate minimum instead of a dimension floor. Ruled out for the same reason as the test-summary rubric: it would allow a report with strong explanations but incomplete or inaccurate grouping to pass, which risks a developer missing an entire category of issues simply because the report read well.
