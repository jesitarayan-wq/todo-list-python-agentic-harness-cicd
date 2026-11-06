# Rubric self-check

Sagaya Jesita Maria Sarath Raj · 2026-11-06

## Against the capstone brief

Seven of the 14 required items are met and seven are partly met; none is a gap now that one live run exists.

| Requirement | Evidence | Status |
| --- | --- | --- |
| README and run path | `README.md`. The build takes 5 to 15 minutes, so the 15-minute target holds only if the image is already built | Partly met |
| Containerized harness | `Dockerfile`, `scripts/run-agent.sh` (per-role mounts) | Met |
| Module 1: PRD, rubric, baseline, iteration log | `docs/prd.md`, `docs/rubric.md`, `docs/baseline-measurements.md`, `docs/iteration-log*.md`. The baseline is a different task | Met |
| Module 2: agent, two or more skills, memory, reflection | `.claude/agents/`, `.claude/skills/` (write-handoff and run-policy-check, v0.1.0), `docs/memory-architecture.md`, `.memory/` | Met |
| Module 3: diagram, routing map, MCP, retrieval report, harness, holdout, calibration log | `docs/orchestration-diagram.md`, `docs/routing-and-tool-grant-map.md`, `mcp-servers/`, `docs/lessons-learned-retrieval-validation.md` (5/7, then 7/7), `eval/`, `docs/holdout-task-set.md`, `docs/calibration-log.md` | Met |
| Module 4: policy, access matrix, CI guardrails, audit template, playbook, decision matrix, conversion, ADR | `docs/governance-policy.md`, `ci.yml` with 3 required checks, `docs/audit-log-template.md`, `docs/failure-mode-playbook.md`, `docs/step-classification.md`, ADR-003 to ADR-008. ADR-003 and ADR-004 are Proposed; the decision matrix lives in `docs/step-classification.md` | Partly met |
| Production-like end-to-end integration | One governed run and one plain-agent baseline on 2026-11-06 (docs/live-run-record.md), with a real test runner. One session's cost was not captured, the handoff check was run by hand, and retries and fallbacks are not built | Partly met |
| Reliability and cost controls | `docs/reliability-and-cost-controls.md` (implemented versus planned) | Partly met |
| Tool-evolution drill | `docs/tool-evolution-drill.md` (policy versus configuration only) | Partly met |
| Impact report with the required metrics | Impact report (the live run and baseline measured once; review latency and defect rate not measured; proxies named) | Partly met |
| Governance stopping an over-reaching agent | `eval/red-team-results.md`, `enforcement-verification.md`, storage audit-log denials | Met |
| Architecture write-up, one-pager, runbook | Architecture write-up, stakeholder one-pager, runbook | Met |
| Walkthrough video and PDFs | Video recorded 2026-10-31. The first PDFs were browser printouts; formatted PDFs and a slide deck have been built, and the video is to be re-recorded with the slides | Partly met |
| Sanitization | `docs/sanitization-note.md` (scan results and what it does not cover) | Met |

## Against the grader's feedback

Six categories scored below 3 at first grading; all six are in progress, and a first live run now exists, with its limits stated.

| Category | First score | Revision status |
| --- | --- | --- |
| Design | 1 | In progress: documents rebuilt with real tables and a drawn diagram, a slide deck built and PDFs exported; the video is to be re-recorded |
| Stakeholder Communication | 2 | In progress: the one-pager and impact report now give hours, defects and dollars as labelled projections; the video is to be re-recorded |
| Sandboxed Environment | 2 | In progress: the README now documents the boundaries, a parallel-isolation test and a network test, with evidence (merged to main in pull request 8); the working container still has open network access |
| Right-Tool Decisions and ADRs | 2 | In progress: three agent runs of the handoff check on one input are compared with the script, and the ADR package is rebuilt; the handoff check also ran on a real implementer result in the live run, and more inputs are open |
| Production Integration and Tool-Evolution Drill | 2 | In progress: one governed run and a plain-agent baseline are recorded with cost and time (docs/live-run-record.md); one session's cost was not captured, and retries and fallbacks are not built |
| Iteration Narrative and Impact | 2 | In progress: the five-measure table, two improvement cycles and a measured baseline run are written; review latency and defect rate are still not measured |
| Workflow Scoping | 3 | Optional, open: quantify the before-state pain and argue why a custom pipeline beats a prebuilt agent or a script |
| Quality Spec and Baseline | 3 | Optional, open: tie the thresholds to business outcomes |
| Orchestration and MCP Tools | 3 | Optional, open: point the agents at the governed servers; `.mcp.json` still lists the older ones |
| Governance, Security and CI/CD | 3 | Optional, in progress: an agent's overreach attempt was tested and refused twice (the allow-list, then the read-only mount), and is to be shown in the video; approvals, failures, retries and rollbacks are logged for the live run (docs/live-run-record.md); one CI step gap is known |
| Clarity and Flow | 3 | In progress: the slide deck follows the required sequence |
| Agent, Skills and Memory | 4 | No change needed |
| Evaluation and Calibration | 4 | No change needed |

## Honest summary

The strongest part is governance enforced in code, with tests, CI gates shown to block, and candid evidence; the weakest is that the live run exists only once and one of its sessions was not costed, so impact claims rest on one run, the baseline, the policy tests, the handoff check and the drill.

Still open:

- Repeat the live run with the cost of every session recorded.
- More inputs for the agent-versus-script handoff comparison (three runs are done on one input).
- Restricting network access in the working container; the README documents the test and the open access.
- Fixing the CI evaluation step (`tee` without `pipefail`) and pointing the agents at the governed servers.
- Re-recording the walkthrough video with the slide deck.
