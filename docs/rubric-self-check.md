# Rubric self-check

Mapped to the capstone brief's required repository contents. Status: Met, Partly met, or Gap.

| Requirement | Evidence | Status |
|---|---|---|
| README and run path | README.md (build takes 5 to 15 min, so the 15-minute target holds only if the image is already built) | Partly met |
| Containerized harness | Dockerfile, scripts/run-agent.sh (per-role mounts) | Met |
| Module 1: PRD, rubric, baseline, iteration log | docs/prd.md, docs/rubric.md, docs/baseline-measurements.md, docs/iteration-log*.md (baseline is a different task) | Met |
| Module 2: agent, 2+ skills, memory, reflection | .claude/agents/, .claude/skills/ (write-handoff, run-policy-check, v0.1.0), docs/memory-architecture.md, .memory/ | Met |
| Module 3: diagram, routing map, MCP, retrieval report, harness, holdout, calibration log | docs/orchestration-diagram.md, routing-and-tool-grant-map.md, mcp-servers/, lessons-learned-retrieval-validation.md (5/7 then 7/7), eval/, holdout-task-set.md, calibration-log.md | Met |
| Module 4: policy, access matrix, CI guardrails, audit template, playbook, decision matrix, conversion, ADR | governance-policy.md, ci.yml with 3 required checks, audit-log-template.md, failure-mode-playbook.md, step-classification.md, ADR-003 to ADR-008 | Partly met (ADR-003 and ADR-004 Proposed; decision matrix lives in step-classification.md) |
| Production-like end-to-end integration | None; no live run (no API key, orchestrator has no shell tool) | Gap |
| Reliability and cost controls | docs/reliability-and-cost-controls.md (implemented vs planned) | Partly met |
| Tool-evolution drill | docs/tool-evolution-drill.md (policy-versus-config only) | Partly met |
| Impact report with required metrics | docs/impact-report.md (proxies named; no pipeline cost or cycle time) | Partly met |
| Governance stopping an over-reaching agent | eval/red-team-results.md, enforcement-verification.md, storage audit log denials | Met |
| Architecture write-up, one-pager, runbook | docs/architecture-writeup.md, stakeholder-one-pager.md, runbook.md | Met |
| Walkthrough video, PDFs | Not started | Gap |
| Sanitization | .gitignore blocks secrets; final scan still to run | Partly met |

## Honest summary
Strongest: enforced governance with tests, CI gates proved to block, and candid evidence. Weakest: no live end-to-end run, so impact claims rest on the baseline, policy tests, the handoff check and the drill.
