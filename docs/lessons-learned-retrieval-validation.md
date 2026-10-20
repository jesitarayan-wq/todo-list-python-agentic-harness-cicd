# Lessons Learned Retrieval Validation Report

Corpus: .memory/reference/ (8 documents, project proj-lessons)
Server: mcp/retrieval/server.py on port 8002
Threshold: 0.65   top_k: 3
Pass rate (first run): 5/7 (71.4%) -- BELOW the 80% floor
Pass rate (after fix): 7/7 (100%)

## GT1 -- mcp version pinning (plain precision)
- Query: "Why do we pin the mcp package version below 2 in this project?"
- Expected: lesson-mcp-version-pinning.md in top 3, score >= 0.65
- Actual (first run): found only via keyword fallback (similarity_score: None in all positions); vector search returned zero confident candidates.
- Result (first run): FAIL
- Actual (after fix): lesson-mcp-version-pinning.md (chunk 0), score 0.737, vector
- Result (final): PASS

## GT2 -- pymongo/bson conflict vs npm engine mismatch decoy (near-miss resistance)
- Query: "Why did pymongo stop finding the bson module after a pip uninstall?"
- Expected: lesson-pymongo-bson-conflict.md in top 3, decoy (lesson-npm-engine-version-mismatch.md) does not outrank it
- Actual: lesson-pymongo-bson-conflict.md (chunk 0), score 0.873, vector; (chunk 1), score 0.725, vector. Decoy absent from results entirely.
- Result: PASS (both runs, unaffected by the GT1/GT6 fix)

## GT3 -- EAI_AGAIN literal error lookup (literal-keyword fallback)
- Query: "What does the error EAI_AGAIN mean in our container network setup?"
- Expected: lesson-network-isolation-tradeoffs.md returned
- Actual: lesson-network-isolation-tradeoffs.md, all 3 chunks returned via keyword fallback (similarity_score: None)
- Result: PASS (both runs). Note: resolved via keyword fallback as this query type anticipated, unlike the earlier Module 3 Lesson 2 corpus where a similar literal-keyword query was unexpectedly resolved by vector search instead -- this ground-truth entry genuinely exercises the keyword-fallback code path.

## GT4 -- Classification ceiling enforcement (must not leak confidential doc)
- Query: "What was the actual dollar cost of the stale memory incident?"
- Forbidden: lesson-rework-cost-incident.md (classification: confidential)
- Actual: lesson-rework-cost-incident.md absent from results in both runs. Returned results (keyword fallback) were not relevant to the cost question specifically, but the security property held correctly.
- Result: PASS (both runs) -- the core security guarantee was never at risk; only GT1 and GT6 (plain precision queries) were affected by the chunking issue.

## GT5 -- chmod bypass under root (plain precision)
- Query: "Why does chmod 444 fail to protect the knowledge directory in this container?"
- Expected: lesson-chmod-bypass-root.md in top 3, score >= 0.65
- Actual: lesson-chmod-bypass-root.md (chunk 0), score 0.763, vector
- Result: PASS (both runs)

## GT6 -- Live MongoDB test dependency (plain precision)
- Query: "Why do route-level tests hang instead of failing in this environment?"
- Expected: lesson-live-mongodb-test-dependency.md in top 3, score >= 0.65
- Actual (first run): found only via keyword fallback (similarity_score: None); vector search returned zero confident candidates. Same failure pattern as GT1.
- Result (first run): FAIL
- Actual (after fix): lesson-live-mongodb-test-dependency.md (chunk 0), score 0.701, vector
- Result (final): PASS

## GT7 -- Orchestrator subagent checkpoint limitation (plain precision)
- Query: "Why can't an Orchestrator running as a subagent complete its own human checkpoints?"
- Expected: lesson-orchestrator-subagent-checkpoint-limitation.md in top 3, score >= 0.65
- Actual: lesson-orchestrator-subagent-checkpoint-limitation.md, 3 chunks returned via vector (scores 0.807, 0.751, 0.742)
- Result: PASS (both runs)

## Investigation and Fix (GT1 and GT6)

**Diagnosis:** both failing documents shared the same structural pattern: the document's heading directly matched the natural-language phrasing of its ground-truth query, but under paragraph chunking, that heading was merged into chunk 0 alongside a dense, jargon-heavy "What happened" paragraph (full of specific error messages, library names, and technical identifiers). This diluted the chunk's embedding away from the general, natural-language question the query actually asked, causing vector search to return zero confident candidates and falling back to keyword search instead.

**Fix attempt 1 (insufficient):** inserted a single short sentence between the heading and the "What happened" paragraph. This did not resolve either failure, because the inserted sentence was too short to stand as its own chunk and was merged back into chunk 0 by the chunker's "merge pieces that are too small" logic, reproducing the identical dilution problem.

**Fix attempt 2 (successful):** rewrote the inserted text into a substantially longer, self-contained paragraph (2-3 sentences) that directly answers the query's natural-language framing in plain language, before the jargon-heavy "What happened" detail. Restarted the server to re-index and re-ran the full 7-query set.

**Result:** 7/7 (100%) passed, with GT1 and GT6 now resolved confidently via vector search (0.737 and 0.701 respectively), and no regressions introduced in the 5 previously-passing queries (GT2, GT3, GT4, GT5, GT7 all confirmed unchanged).

## Conclusion

The corpus required one genuine fix, discovered and resolved through direct testing rather than assumption: documents whose natural-language "trigger phrase" is immediately followed by dense technical jargon in the same chunk can fail plain-precision vector matching, even though the correct document is eventually found via keyword fallback. The fix -- giving the natural-language answer its own substantial, isolated paragraph -- resolved both instances of this pattern without introducing any regression, confirmed by re-running the complete ground-truth set after the change rather than only the two previously-failing queries. The classification-ceiling guarantee (GT4) was never at risk during this investigation; it held correctly throughout both the failing and passing runs.
