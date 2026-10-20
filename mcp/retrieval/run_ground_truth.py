from __future__ import annotations

import asyncio
from typing import Any

from fastmcp import Client

THRESHOLD = 0.65
SERVER_URL = "http://localhost:8002/mcp"

CASES: list[dict[str, Any]] = [
    {
        "id": "GT1",
        "kind": "precision",
        "query": "Why do we pin the mcp package version below 2 in this project?",
        "project_id": "proj-lessons",
        "ceiling": "internal",
        "filters": {},
        "expected": "lesson-mcp-version-pinning.md",
    },
    {
        "id": "GT2",
        "kind": "precision",
        "query": "Why did pymongo stop finding the bson module after a pip uninstall?",
        "project_id": "proj-lessons",
        "ceiling": "internal",
        "filters": {},
        "expected": "lesson-pymongo-bson-conflict.md",
    },
    {
        "id": "GT3",
        "kind": "keyword",
        "query": "What does the error EAI_AGAIN mean in our container network setup?",
        "project_id": "proj-lessons",
        "ceiling": "internal",
        "filters": {},
        "expected": "lesson-network-isolation-tradeoffs.md",
    },
    {
        "id": "GT4",
        "kind": "ceiling",
        "query": "What was the actual dollar cost of the stale memory incident?",
        "project_id": "proj-lessons",
        "ceiling": "internal",
        "filters": {},
        "forbidden": "lesson-rework-cost-incident.md",
    },
    {
        "id": "GT5",
        "kind": "precision",
        "query": "Why does chmod 444 fail to protect the knowledge directory in this container?",
        "project_id": "proj-lessons",
        "ceiling": "internal",
        "filters": {},
        "expected": "lesson-chmod-bypass-root.md",
    },
    {
        "id": "GT6",
        "kind": "precision",
        "query": "Why do route-level tests hang instead of failing in this environment?",
        "project_id": "proj-lessons",
        "ceiling": "internal",
        "filters": {},
        "expected": "lesson-live-mongodb-test-dependency.md",
    },
    {
        "id": "GT7",
        "kind": "precision",
        "query": "Why can't an Orchestrator running as a subagent complete its own human checkpoints?",
        "project_id": "proj-lessons",
        "ceiling": "internal",
        "filters": {},
        "expected": "lesson-orchestrator-subagent-checkpoint-limitation.md",
    },
]


def extract_hits(result: Any) -> list[dict[str, Any]]:
    if hasattr(result, "data") and result.data is not None:
        return result.data
    if hasattr(result, "structured_content") and result.structured_content is not None:
        return result.structured_content
    if hasattr(result, "structuredContent") and result.structuredContent is not None:
        return result.structuredContent
    if isinstance(result, list):
        return result
    raise RuntimeError(f"Could not extract structured hits from result: {result!r}")


def judge(case: dict[str, Any], hits: list[dict[str, Any]]) -> bool:
    docs = [hit["source_document"] for hit in hits]
    if case["kind"] == "ceiling":
        return case["forbidden"] not in docs
    if case["kind"] == "keyword":
        return case["expected"] in docs
    return any(
        hit["source_document"] == case["expected"]
        and (hit.get("similarity_score") or 0) >= THRESHOLD
        for hit in hits
    )


def summarize(hits: list[dict[str, Any]]) -> str:
    if not hits:
        return "(no results)"
    return ", ".join(
        f"{hit['source_document']}#{hit['chunk_index']}"
        f"({hit['retrieval_method']},{hit.get('similarity_score')})"
        for hit in hits
    )


async def main() -> None:
    passed = 0
    async with Client(SERVER_URL) as client:
        for case in CASES:
            result = await client.call_tool(
                "retrieve",
                {
                    "query": case["query"],
                    "project_id": case["project_id"],
                    "top_k": 3,
                    "classification_ceiling": case["ceiling"],
                    "metadata_filters": case.get("filters", {}),
                },
            )
            hits = extract_hits(result)
            ok = judge(case, hits)
            passed += int(ok)
            print(f"{case['id']}: {'PASS' if ok else 'FAIL'} [{summarize(hits)}]")

    print(f"\n{passed}/{len(CASES)} passed")
    if passed / len(CASES) < 0.80:
        raise SystemExit("Retrieval pass rate is below the 80% floor")


if __name__ == "__main__":
    asyncio.run(main())
