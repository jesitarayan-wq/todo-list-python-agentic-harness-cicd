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

## Step: Pipeline integrity check
- Does: Reads .github/workflows/ci.yml and fails if the pipeline has been weakened.
- Checks: (1) policy-gate, eval-gate and pipeline-integrity exist and have no continue-on-error: true, because that would silently disable a gate. (2) audit-trail exists and keeps if: always(), so evidence is kept even when other jobs fail. (3) change-type-check exists, because later jobs depend on its outputs.
- Input: the workflow file only (no Docker build, no secrets).
- Produces: integrity-report.json artifact with fields check, result (passed or failed) and sha. The audit trail records it as results.pipeline_integrity and reports_present.integrity_report.
- Classification: gating, permanent. It protects an invariant the team agreed must always hold, so it is never demoted to advisory.
- Runs: needs change-type-check only, with if: always(), so a failing policy gate cannot hide a weakened pipeline.
- Required status check: "Pipeline Integrity Check" added to the protect-main ruleset.
- Audit trail wiring: pipeline-integrity is in audit-trail's needs list; build-audit-trail.py takes --integrity-result.
- Time limit: 2 minutes. Credentials: none.
- Verified: On a throwaway branch, continue-on-error: true was added to policy-gate. Pipeline Integrity Check failed with exit code 1 (the script's response to a weakened gate), and the branch was deleted without merging. Not recorded: the exact log line, and whether the merge button was blocked.
