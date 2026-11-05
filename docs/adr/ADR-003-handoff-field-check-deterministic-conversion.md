# ADR-003: Convert the handoff field check from agent convention to deterministic code

## Status
Proposed

## Context
Agent handoffs (implementer to orchestrator) were a convention in the agent prompts: a list of modified files, a description of each change, and any lesson entry_id. Nothing checked them. HO-04 probed this "output format mismatch" risk, and its referenced handoff spec file never existed. The rule can be written exactly.

## Decision
Check each handoff with scripts/validate_handoff_deterministic.py against schemas/handoff.json. Required: task_id, role, summary, and modified_files (a non-empty list whose items each have a non-empty path and description). Invalid handoffs exit 1 with a list of problems.

## Alternatives considered
- Keep it as an agent convention. Rejected: no check, variance, and governance overhead for a fixed rule.
- Ask an agent to validate. Rejected, with measurement: three agent runs on the same bad input, given only the schema, each judged it valid while the script rejects it, with varying wording and a session cost of about $0.10 to $0.16 (see the 2026-11-05 evidence update below).
- Convert to code. Accepted.

## Consequences
Measured: the script took 0.193s, 0.170s and 0.175s over three runs on the same input, with identical output each time, no token cost, and the 7 existing step tests still pass. Trade-off: the result is a terse problem list, not prose. Limits: stability was not measured (one calibration cycle), and no agent baseline was measured.

## Evidence
- docs/step-classification.md
- examples/handoff_good.json (valid, exit 0) and examples/handoff_bad.json (empty description, exit 1)
- eval/test_deterministic_step.py: 7 passed

## Process note
The validator and sample handoffs were written before this ADR, and the ADR was committed together with the code (89a35bc). That reverses the intended order (ADR first, as Proposed). Status is Proposed because acceptance requires the script to be wired into a running workflow, an end-to-end regression check, and a calibration log entry. None of these exist yet.

## Evidence update (2026-10-22)
See docs/calibration-log.md, "Handoff field check: conversion measurements". After-conversion: about 0.18s, zero token cost, identical output on three runs, 15 tests passing. Before-conversion: not measurable. Status remains Proposed until the script is wired into a workflow and an end-to-end check passes.

## Open risks
- Stability was not measured: there was one calibration cycle.
- Agent baseline: three runs on one input, now measured (see the 2026-11-05 evidence update). It is not a rate, and it covers one input and one agent setup.
- The check is wired as an orchestrator step, but the orchestrator has no shell tool to run it, so no end-to-end check has passed.

## Evidence update (2026-11-05): agent versus script on the same input

Input: `examples/handoff_bad.json` (an empty description in `modified_files[0]`), checked against `schemas/handoff.json`. Reference: the script returns `valid: false` with one problem naming the empty description, exit 1.

Agent: Claude Code, a fresh container each time, the read-only dependency-auditor role, told to use only those two files and not to run any script. Three runs, the same prompt.

| | Script | Agent run A | Agent run B | Agent run C |
| --- | --- | --- | --- | --- |
| Verdict | invalid | valid | valid | valid |
| Empty description | named as the problem | noted as something a stricter check would reject | noted as a content problem the schema does not catch | noted as a weak spot the schema misses |
| Time | about 0.18 s | 11 s API, 1 m 5 s wall | 9 s API, 43 s wall | 12 s API, 40 s wall |
| Session cost | zero tokens | $0.1614 | $0.1042 | $0.1207 |
| Output tokens | zero | 948 | 773 | 866 |
| Code changes | none | 0 lines | 0 lines | 0 lines |

Findings:

- Predictability: the script gave identical output on three runs. The agent gave the same verdict three times, but different wording, length and cost (session cost varied by about 55%).
- Accuracy against the project rule: with only the schema, the agent's verdict disagreed with the script in 3 of 3 runs, because the schema does not enforce non-empty values; that rule lives in the script. In a pilot where the agent could read the script's source it matched the script. The pilot is not counted, and its cost was not captured.
- Audit clarity: the script returns a structured result and an exit code a pipeline can act on; the agent returns prose.
- Cost and latency: the agent step took about 40 to 65 s and about $0.10 to $0.16 per session, against about 0.18 s and zero tokens for the script. Session cost includes the main session's own turns and a warm prompt cache, so it is the cost of the session, not of the check alone.

Limits: three runs of one input with one agent setup, so this is not a rate. Timings differ in kind (agent API and wall time versus script runtime).

Effect on the decision: the measurement supports converting this step to code. The status stays Proposed, because the script has not yet been exercised end to end in a running workflow.
