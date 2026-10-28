# ADR-003: Convert the handoff field check from agent convention to deterministic code

## Status
Proposed

## Context
Agent handoffs (implementer to orchestrator) were a convention in the agent prompts: a list of modified files, a description of each change, and any lesson entry_id. Nothing checked them. HO-04 probed this "output format mismatch" risk, and its referenced handoff spec file never existed. The rule can be written exactly.

## Decision
Check each handoff with scripts/validate_handoff_deterministic.py against schemas/handoff.json. Required: task_id, role, summary, and modified_files (a non-empty list whose items each have a non-empty path and description). Invalid handoffs exit 1 with a list of problems.

## Alternatives considered
- Keep it as an agent convention. Rejected: no check, variance, and governance overhead for a fixed rule.
- Ask an agent to validate. Not measured (no agent version of this step exists). Qualitatively it adds token cost, latency and variance to a rule with no ambiguity.
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
