"""Agent 6 — Multilingual Agent."""

from __future__ import annotations

import json
from typing import Any

from agents.base import BaseAgent


class MultilingualAgent(BaseAgent):
    name = "multilingual"
    instructions = """\
You are a multilingual product content specialist for RAJA Group.

Your input is validated English product content in JSON.
Produce culturally adapted versions in English, German, Spanish, and Italian.

For each language, adapt:
- short_description
- long_description
- customer_benefits
- meta_description

Return a JSON object with:
- en (object with the four fields above)
- de (object with the four fields above)
- es (object with the four fields above)
- it (object with the four fields above)
- translation_flags (array of objects: field, language, issue — if any)

Register guidelines:
- English: concise, clear, B2B practical
- German: precise, technical, formal
- Spanish: clear, professional, slightly warmer
- Italian: descriptive, commercial, relationship-oriented

Rules:
- Do not translate specifications incorrectly.
- Preserve SKU, dimensions, weights, and supported claims.
- Flag any untranslatable or risky term.
- Return valid JSON only.
"""

    def _build_user_message(self, context: dict[str, Any]) -> str:
        return json.dumps(
            {
                "run_id": context.get("run_id"),
                "normalized_product": context.get("normalization", {}).get("normalized_product"),
                "enrichment": context.get("enrichment"),
                "seo_meta_description": context.get("seo", {}).get("meta_description", ""),
            },
            indent=2,
            ensure_ascii=False,
        )
