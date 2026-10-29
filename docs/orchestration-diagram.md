# Orchestration Diagram: todo-list-python (8 roles)

The orchestrator (the main Claude session) delegates to scoped subagents. Each arrow says what is handed down and what comes back. The handoff check is deterministic code, and the human checkpoints are marked.

```mermaid
graph TD
    H([Human: feature request, approvals])
    O[Orchestrator - autonomy medium]
    H -->|"feature request + repo path"| O

    O -->|"feature request + read-only codebase access"| P[Planner - high]
    P -->|"numbered plan + file list + cited lessons"| O
    O -.->|"human checkpoint: approve plan"| H

    O -->|"plan + file list"| I[Implementer - medium]
    I -->|"modified files + descriptions + lesson entry_id"| O

    O -->|"handoff JSON"| V{{"Handoff check - deterministic code<br/>scripts/validate_handoff_deterministic.py"}}
    V -->|"valid / problems list"| O

    O -->|"modified files"| R[Security-reviewer - high, read-only]
    R -->|"review report"| O

    O -->|"modified files"| T[Tester - medium]
    T -->|"pass/fail report"| O

    O -->|"final outcome"| PM[Project-manager - medium]
    PM -->|"ticket updated"| O
    O -.->|"human checkpoint: confirm before ticket update"| H

    O -.->|"on demand"| TCA[Test-coverage-analyzer - low, read-only]
    O -.->|"on demand"| DA[Dependency-auditor - low, read-only]
```

## Role summary

| Role | Responsibility | Autonomy | Workspace |
|---|---|---|---|
| Orchestrator | Decompose, delegate, evaluate, assemble | medium | read-write |
| Planner | Ordered plan and file list | high | read-only |
| Implementer | Write the code in the plan | medium | read-write |
| Security-reviewer | Report problems, never edit | high | read-only |
| Tester | Run tests, report pass/fail | medium | read-only |
| Project-manager | Update the ticket only | medium | read-only |
| Test-coverage-analyzer | Recommend tests (on demand) | not declared in file; policy sets low | read-only |
| Dependency-auditor | Report risky dependencies (on demand) | low | read-only |

## Agent, deterministic code, or human
- **Agent:** planner, implementer, security-reviewer, tester, project-manager, test-coverage-analyzer, dependency-auditor (judgment or synthesis).
- **Deterministic code:** the handoff check (ADR-003, Proposed), the MCP allow-list and classification checks, the policy test suite.
- **Human:** plan approval and ticket confirmation. A subagent cannot confirm human approval, so the main session plays the orchestrator for real checkpoints.

## Limits
- The tester's `test_runner` returns placeholder PASS output, so test results are unverified.
- The handoff check is wired as orchestrator step 2a, but the orchestrator has no shell tool to run it.
