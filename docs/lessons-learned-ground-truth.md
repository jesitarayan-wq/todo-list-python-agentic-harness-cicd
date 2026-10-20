# Lessons Learned Ground-Truth Query Set

Project: `proj-lessons`

Confidence threshold: `0.65`

Default pass criterion for precision queries: expected document appears in the top 3 results with `similarity_score >= 0.65`.

## GT1 — mcp version pinning (plain precision)
- Query: "Why do we pin the mcp package version below 2 in this project?"
- Expected top result: `lesson-mcp-version-pinning.md`
- Filters: `project = proj-lessons`, `classification_ceiling = internal`
- Pass: `lesson-mcp-version-pinning.md` appears in top 3 with score `>= 0.65`.
- Purpose: plain precision.

## GT2 — pymongo/bson conflict vs npm engine mismatch decoy (near-miss resistance)
- Query: "Why did pymongo stop finding the bson module after a pip uninstall?"
- Expected top result: `lesson-pymongo-bson-conflict.md`
- Decoy present: `lesson-npm-engine-version-mismatch.md` (both describe a "package version conflict" causing a confusing failure, but in unrelated ecosystems -- Python/pymongo vs Node/npm)
- Filters: `project = proj-lessons`, `classification_ceiling = internal`
- Pass: `lesson-pymongo-bson-conflict.md` appears in top 3 with score `>= 0.65`; the npm-engine decoy does not outrank it.
- Purpose: resistance to near-miss.

## GT3 — EAI_AGAIN literal error lookup (literal-keyword fallback)
- Query: "What does the error EAI_AGAIN mean in our container network setup?"
- Expected result: `lesson-network-isolation-tradeoffs.md`
- Filters: `project = proj-lessons`, `classification_ceiling = internal`
- Pass: `lesson-network-isolation-tradeoffs.md` is returned. Keyword fallback is acceptable and expected if vector matching is not confident.
- Purpose: literal-keyword fallback.

## GT4 — Rework cost ceiling enforcement (must NOT leak confidential doc)
- Query: "What was the actual dollar cost of the stale memory incident?"
- Best semantic match in corpus: `lesson-rework-cost-incident.md` (`classification: confidential`)
- Filters: `project = proj-lessons`, `classification_ceiling = internal`
- Pass: `lesson-rework-cost-incident.md` does **not** appear in results. The tool returns only internal-or-below matches, or an empty result if none qualify.
- Purpose: classification ceiling.

## GT5 — chmod bypass under root (plain precision)
- Query: "Why does chmod 444 fail to protect the knowledge directory in this container?"
- Expected top result: `lesson-chmod-bypass-root.md`
- Filters: `project = proj-lessons`, `classification_ceiling = internal`
- Pass: `lesson-chmod-bypass-root.md` appears in top 3 with score `>= 0.65`.
- Purpose: plain precision for Reviewer/Implementer roles.

## GT6 — Live MongoDB test dependency (plain precision)
- Query: "Why do route-level tests hang instead of failing in this environment?"
- Expected top result: `lesson-live-mongodb-test-dependency.md`
- Filters: `project = proj-lessons`, `classification_ceiling = internal`
- Pass: `lesson-live-mongodb-test-dependency.md` appears in top 3 with score `>= 0.65`.
- Purpose: plain precision for Tester role.

## GT7 — Orchestrator subagent checkpoint limitation (plain precision)
- Query: "Why can't an Orchestrator running as a subagent complete its own human checkpoints?"
- Expected top result: `lesson-orchestrator-subagent-checkpoint-limitation.md`
- Filters: `project = proj-lessons`, `classification_ceiling = internal`
- Pass: `lesson-orchestrator-subagent-checkpoint-limitation.md` appears in top 3 with score `>= 0.65`.
- Purpose: plain precision for Planner role.
