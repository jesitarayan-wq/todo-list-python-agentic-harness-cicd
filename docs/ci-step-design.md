# CI Agentic Step Design

Rule: new agentic steps start advisory. A step can gate only if it gives clear, repeatable pass/fail results and has shown a low false-alarm rate. Deterministic checks can gate immediately.

## Step: Policy test suite
- Does: Confirms docs/governance-policy.md, the MCP allow-lists, skill scopes and container permissions agree.
- Input: whole repository.
- Produces: policy-report.json artifact.
- Classification: gating, permanent (deterministic; green in CI run #1).
- Time limit: 5 minutes.
- Credentials: none.

## Step: Automated code review
- Does: Reviewer script scores changed files and writes an advisory review.
- Input: changed files from the change classifier.
- Produces: review-output.md and a review audit log as artifacts.
- Classification: advisory (new, uses judgment; promote to gating only after a low false-alarm rate over many runs). continue-on-error is true.
- Time limit: 15 minutes.
- Credentials: ANTHROPIC_API_KEY, scoped to this step only. Without it the script writes "No review was performed" and does not fail.

## Step: Evaluation harness, rubric run
- Does: Scores agent output against the project rubric (root cause identification, root cause accuracy, summary clarity) with an AI judge.
- Input: a run transcript.
- Produces: a rubric report.
- Classification: advisory. The harness reads local transcripts and audit logs that do not exist on a clean CI runner, so it cannot run in CI yet, and the rubric uses an AI judge.
- Time limit: 10 minutes.
- Credentials: ANTHROPIC_API_KEY, scoped to this step only.

## Step: Audit trail
- Does: Combines policy, governed-file and review results into one JSON record.
- Input: artifacts from earlier jobs.
- Produces: ci-audit-trail-<sha>.json artifact (confirmed in CI run #1).
- Classification: observational; always runs.
- Credentials: none.
