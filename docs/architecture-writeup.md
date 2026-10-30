# Architecture write-up: todo-list-python governed multi-agent harness

## 1. Workflow and roles
A feature request enters the orchestrator (the main Claude session, instructions in CLAUDE.md and .claude/agents/orchestrator.md). Sequence: planner, implementer, deterministic handoff check, security-reviewer, tester, project-manager. Test-coverage-analyzer and dependency-auditor run on demand. Diagram: docs/orchestration-diagram.md. Roles, autonomy and grants: docs/governance-policy.md, docs/routing-and-tool-grant-map.md.

## 2. Agent, deterministic code, or human
- Agent (judgment): planner, implementer, security-reviewer, tester, project-manager, test-coverage-analyzer, dependency-auditor.
- Deterministic code: handoff field check (scripts/validate_handoff_deterministic.py, ADR-003, Proposed), MCP role and classification checks, policy test suite.
- Human: plan approval and ticket confirmation. A subagent cannot confirm human approval, so the main session plays the orchestrator at real checkpoints.
Rationale per step: docs/step-classification.md.

## 3. Data flow, storage, retrieval, MCP boundaries
Roles call MCP servers (mcp-servers/storage, mcp-servers/retrieval). Each operation is checked against a per-role allow-list and a classification ceiling; refusals are logged to logs/*-audit-log.jsonl (template: docs/audit-log-template.md). Memory layers: .memory/project, knowledge, reference (docs/memory-architecture.md).

## 4. Retrieval quality
Corpus: .memory/reference/, 8 documents. Threshold 0.65, top_k 3. First run 5/7 (71.4%), below the 80% floor; after fix 7/7 (100%). Source: docs/lessons-learned-retrieval-validation.md. The first run found one lesson only through keyword fallback, which is the silent-miss risk the report exists to catch.

## 5. CI/CD and governance enforcement
Layers, inside out: policy document; run-agent.sh container permissions (read-only or read-write per role); MCP allow-lists; eval/test_policy.py (37 checks); CI workflow with classifier, policy gate, governed-file check, evaluation harness, pipeline integrity check, advisory review and audit trail; GitHub ruleset protect-main requiring Policy Test Suite, Evaluation Harness and Pipeline Integrity Check.
Proofs: a branch over-granting delete_entry turned the Policy Test Suite red; continue-on-error on policy-gate failed the integrity job (CI #13); a revoked write_entry grant was caught by test_storage_allowlist_matches_policy[implementer] (docs/tool-evolution-drill.md); direct pushes to main are rejected (GH013).

## 6. Decisions
ADR-003 to ADR-008 in docs/adr/. ADR-003 and ADR-004 are Proposed; ADR-005 to ADR-008 are Accepted.

## 7. Limits
No live end-to-end run (the orchestrator has no shell tool; eval/orchestrator.py is a simulation). No API key, so the AI review and rubric have never run. The eval gate replays one saved transcript (HO-01). Skill scope is enforced by instruction and a policy test, not a runtime lock. The tester's test_runner returns placeholder PASS output. Direct merges to main used a temporary ruleset bypass because PRs on this fork defaulted to the parent repo.
