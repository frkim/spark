"""Agent 2 — Foundry IQ Retrieval Agent."""

from __future__ import annotations

import json
from typing import Any

from agents.base import BaseAgent
from demo_data import ALL_SOURCES


class RetrievalAgent(BaseAgent):
    name = "foundry_iq_retrieval"
    instructions = """\
You are a grounded retrieval specialist for RAJA Group.

Your input is a resolved product context and a retrieval query.
Your task is to retrieve the most relevant evidence from Foundry IQ.

The following enterprise data sources are indexed in Foundry IQ:
{sources}

Search across these source types:
- IQ product exports
- Supplier technical sheets
- RAJA taxonomy references
- Compliance and sustainability references
- Existing catalog content
- ERP or stock feeds

Return a JSON object with:
- retrieved_sources (array with source_id, source_type, excerpt, confidence)
- extracted_attributes (object with all product attributes found)
- missing_critical_fields (array of field names not found in any source)
- retrieval_notes (string)

Rules:
- Prioritize trusted internal sources over stylistic examples.
- Preserve source identifiers for downstream citations.
- Do not generate product content.
- Return valid JSON only.
""".format(sources=json.dumps(ALL_SOURCES, indent=2, ensure_ascii=False))

    def _build_user_message(self, context: dict[str, Any]) -> str:
        return json.dumps(
            {
                "run_id": context.get("run_id"),
                "resolved_sku": context.get("intake", {}).get("resolved_sku"),
                "supplier_ref": context.get("intake", {}).get("supplier_ref"),
                "retrieval_query": context.get("intake", {}).get("retrieval_query"),
                "market_scope": context.get("intake", {}).get("market_scope"),
            },
            indent=2,
            ensure_ascii=False,
        )
