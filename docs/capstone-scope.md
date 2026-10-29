# Capstone scope (Workstream 1)

## Workflow
Ticket-to-implementation with review and test support on the todo-list-python API (Flask + MongoDB). A feature request goes through planner, implementer, a deterministic handoff check, security-reviewer, tester and project-manager, orchestrated and governed. Test-coverage-analyzer and dependency-auditor run on demand.

## Delivery path
Job-seeker / no-deployment. Data: the to-do API and the 7 holdout tasks in docs/holdout-task-set.md, which are representative, not real internal data. In a real deployment: approvals for internal data, sanitized tickets, a real test runner, a registered API key, and a live end-to-end orchestration.

## Stakeholder
A small team maintaining the API, who want fewer review defects and a visible audit trail.

## Trigger
A feature request or a pull request.

## Inputs and outputs
- Input: feature request text and repo path.
- Output: reviewed change, handoff JSON (validated), test report, updated ticket, audit trail.

## Acceptance criteria
Reuse docs/prd.md and docs/rubric.md: pass threshold 3 or higher on every dimension. Governance: 37 policy checks pass; CI gates pass.

## Failure modes
NM-1 to NM-6 (docs/calibration-log.md) and the four delegation failures: routing misfire, output format mismatch, over-broad tool grant, context bleed.

## What the demo must show
1. Workflow, stakeholder, baseline problem (docs/baseline-measurements.md).
2. README path and repo map.
3. Containerized harness and the pipeline run.
4. Scoped grants, MCP storage and retrieval, one eval result.
5. Governance stopping an over-reaching agent (reviewer write refused, implementer delete denied).
6. Decision matrix and the deterministic conversion (ADR-003).
7. Baseline vs after metrics and the tool-evolution drill (still to do).

## Known gaps to close
Live end-to-end run, tool-evolution drill, reliability and cost controls, failure-mode playbook, audit log template, ADR package, one-pager, runbook, PDFs, video.
