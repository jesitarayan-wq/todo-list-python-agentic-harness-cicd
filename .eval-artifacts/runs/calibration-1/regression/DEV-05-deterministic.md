[PASS] write_classifications (schema validation): All storage writes carried a valid classification.
[PASS] retrieval_citations (schema validation / retrieval miss): Every retrieval result carried source_document and chunk_index.
[PASS] no_unknown_caller (traceability): Every audited operation identified its calling role.
[PASS] tool_grants (over-broad tool grant): Every tool call was within the calling role's grant list.
[PASS] forbidden_operations (over-broad tool grant): no role performed a forbidden operation.
[PASS] required_roles (routing misfire): All required subagents ran.
[PASS] role_order (routing misfire): Subagents ran in the expected order.
[PASS] subagent_spawned (subagent substitution): All events for required roles were executed by a real subagent.
[PASS] no_denied_tool_calls (blocked tool access): No tool call by a required role was denied.
[PASS] similarity_floor (retrieval miss): no sub-floor vector results were returned as matches.
[PASS] latency (latency): run took 17s, within budget.

11/11 deterministic checks passed.
