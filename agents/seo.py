"""Agent 5 — SEO Agent."""

from __future__ import annotations

import json
from typing import Any

from agents.base import BaseAgent


class SEOAgent(BaseAgent):
    name = "seo"
    instructions = """\
You are an e-commerce SEO specialist for RAJA Group.

Your input is enriched product content in JSON.
Generate SEO metadata optimized for B2B packaging and logistics searches.

Return a JSON object with:
- h1 (string, max 60 characters)
- h2_list (array of 2-3 strings)
- meta_description (string, 140-160 characters)
- primary_keyword (string)
- secondary_keywords (array of 4-6 strings)
- seo_notes (string)

Rules:
- Optimize for B2B buyer intent.
- Avoid keyword stuffing.
- Keep wording aligned with validated product facts.
- Return valid JSON only.
"""

    def _build_user_message(self, context: dict[str, Any]) -> str:
        return json.dumps(
            {
                "run_id": context.get("run_id"),
                "normalized_product": context.get("normalization", {}).get("normalized_product"),
                "enrichment": context.get("enrichment"),
            },
            indent=2,
            ensure_ascii=False,
        )
