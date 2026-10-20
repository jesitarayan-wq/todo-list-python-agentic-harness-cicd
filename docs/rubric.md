# Quality Rubric

## Dimensions

### Root Cause Identification

Measures whether the agent correctly groups failures that share a common underlying cause, rather than treating each failing test as a separate, unrelated problem. A high score requires all failures stemming from the same cause to be explicitly connected in the summary.

### Root Cause Accuracy

Measures whether the identified cause of failures is actually correct and supported by evidence from the test output, rather than a vague or unsupported guess. A high score requires the agent to reference specific error messages or exact failure counts that confirm the stated cause.

### Summary Clarity

Measures whether the summary is written in plain, easy-to-follow language that clearly explains what happened and why, giving the reader enough understanding to know what action to take next. A high score requires the explanation to be understandable without needing to re-read the raw test output.

## Scoring Guide

### Root Cause Identification

1 - Does not meet: The summary lists each failing test individually with no attempt to identify shared causes, even when multiple failures clearly stem from the same underlying issue.

2 - Partially meets: The summary identifies a shared cause, but fails to account for one or more related failures, presenting them as separate or unexplained instead.

3 - Meets: The summary correctly groups all failures that share a common root cause, with no failures left ungrouped or misattributed.

4 - Exceeds: The summary groups all related failures accurately, and also explains why this particular root cause affects multiple tests (e.g., because they all depend on the same underlying resource).

### Root Cause Accuracy

1 - Does not meet: The summary states a cause without any supporting evidence from the actual test output, or the stated cause is factually incorrect (e.g., "some tests failed, possibly due to a path issue" -- vague and not tied to the actual error).

2 - Partially meets: The summary states a generally correct direction (e.g., "an environment or configuration issue"), but does not cite the specific error message or evidence confirming it.

3 - Meets: The summary correctly identifies the cause and cites specific evidence from the test output, such as the exact error message (e.g., "6 tests failed with pymongo.errors.ServerSelectionTimeoutError, indicating MongoDB is not running").

4 - Exceeds: The summary meets level 3, and also connects the cause to relevant project context, such as documented setup requirements, making it immediately clear how to resolve the issue.

### Summary Clarity

1 - Does not meet: The summary is difficult to understand, such as raw error output pasted without explanation, or technical jargon used without any plain-language interpretation for the reader.

2 - Partially meets: The summary explains the failure in plain language, but is disorganized or requires re-reading to fully understand what happened.

3 - Meets: The summary clearly explains what happened and why, in a way that can be understood in a single read-through without needing to consult the raw test output.

4 - Exceeds: The summary meets level 3, and is also organized in a way that makes the next action obvious (e.g., clearly separating "what failed" from "what to do about it").

## Pass Threshold

A run is passing if it scores 3 or higher on all three dimensions.

Reasoning: A summary with an inaccurate or ungrounded root cause is misleading even if it is clearly written, and a well-supported root cause that is poorly explained still fails to help the reader act on it. Since both correctness and communicability are essential for this workflow to be trustworthy, a dimension floor ensures no single weak area can be hidden by strong performance elsewhere.

## Notes on Threshold Design

Considered an aggregate minimum (e.g., 9 out of 12) instead of a dimension floor. Ruled out because it would allow a summary with a clearly written but factually wrong or unsupported root cause to pass, as long as clarity scored high enough to compensate. Since an inaccurate root cause could mislead a developer into fixing the wrong problem, this tradeoff was judged unacceptable.
