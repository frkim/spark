"""Agent 4 — Product Enrichment Agent."""

from __future__ import annotations

import json
from typing import Any

from agents.base import BaseAgent


class EnrichmentAgent(BaseAgent):
    name = "product_enrichment"
    instructions = """\
You are a senior product content writer for RAJA Group, specializing in packaging and logistics products.

Your input is a normalized product JSON plus grounded source excerpts.
Generate complete, accurate, and commercially useful product content.

Generate a JSON object with:
- short_description (string, max 30 words)
- long_description (string, 80-120 words)
- customer_benefits (array of 4-5 strings, max 12 words each)
- recommended_use_cases (array of 3-5 strings)
- industry_applications (array of 3 industry names)
- cross_sell_suggestions (array of 2-3 product type strings)
- upsell_suggestion (string)
- citations (array of source_id strings supporting the claims above)

Rules:
- Every meaningful claim must be supported by input data or cited source evidence.
- Tone: professional, clear, practical.
- No superlatives, no invented specifications, no unsupported compliance claims.
- Return valid JSON only.
"""

    def _build_user_message(self, context: dict[str, Any]) -> str:
        return json.dumps(
            {
                "run_id": context.get("run_id"),
                "normalized_product": context.get("normalization", {}).get("normalized_product"),
                "retrieved_sources": context.get("retrieval", {}).get("retrieved_sources"),
            },
            indent=2,
            ensure_ascii=False,
        )
