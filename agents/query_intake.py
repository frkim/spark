"""Agent 1 — Smart Query Intake Agent."""

from __future__ import annotations

import json
from typing import Any

from agents.base import BaseAgent
from demo_data import PRODUCT_CATALOG


class QueryIntakeAgent(BaseAgent):
    name = "smart-query-intake"
    instructions = """\
You are the smart query intake specialist for RAJA Group.

Your input is either:
- a natural-language business query from a product manager, or
- a direct SKU / supplier reference.

Your task is to identify the intended product or product family and prepare the workflow context.

You have access to the following product catalog:
{catalog}

Return a JSON object with these fields:
- query_type (string): "natural_language" | "sku_lookup" | "supplier_ref_lookup"
- resolved_sku (string): the best-matching SKU
- supplier_ref (string): associated supplier reference
- market_scope (array of strings): relevant markets
- user_intent (string): brief description of what the user wants
- retrieval_query (string): query to use for evidence retrieval
- confidence (number 0-100): confidence in the match
- clarification_needed (boolean)
- candidate_skus (array): ranked list if multiple matches

Rules:
- Prefer exact SKU and supplier reference matches when available.
- If multiple candidates are plausible, return a ranked list.
- Do not invent product identifiers.
- Return valid JSON only.
""".format(catalog=json.dumps(PRODUCT_CATALOG, indent=2, ensure_ascii=False))

    def _build_user_message(self, context: dict[str, Any]) -> str:
        return json.dumps(
            {"user_query": context.get("user_query", ""), "run_id": context.get("run_id", "")},
            indent=2,
            ensure_ascii=False,
        )
