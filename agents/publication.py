"""Agent 8 — Publication Agent."""

from __future__ import annotations

import json
from typing import Any

from agents.base import BaseAgent


class PublicationAgent(BaseAgent):
    name = "publication"
    instructions = """\
You are a product content publication specialist for RAJA Group.

Your input is approved, multilingual product content in JSON.
Format it into the required schemas for each publication channel.

Generate a JSON object with these four keys:

1. ecommerce_json — full structured record for PIM/CMS containing:
   sku, approved_label, raja_category, dimensions_mm, weight_g, material, color,
   pack_quantity, market_availability, compliance_tags,
   short_description, long_description, customer_benefits,
   recommended_use_cases, industry_applications, cross_sell_suggestions, upsell_suggestion,
   seo (h1, h2_list, meta_description, primary_keyword, secondary_keywords),
   multilingual (en, de, es, it),
   quality_status, citation_coverage_score, run_id

2. marketplace_ready — flat JSON with:
   sku, title, description, bullet_points, keywords, price_note, availability

3. crm_short — plain text paragraph, max 60 words, English only

4. catalog_text_block — plain text with H1, short description, benefit bullets,
   dimensions, weight, material, SKU

Rules:
- Do not add content not in the input.
- Respect field length limits.
- Preserve run_id and citation references for audit purposes.
- Return all four formats in one JSON object.
"""

    def _build_user_message(self, context: dict[str, Any]) -> str:
        return json.dumps(
            {
                "run_id": context.get("run_id"),
                "normalized_product": context.get("normalization", {}).get("normalized_product"),
                "enrichment": context.get("enrichment"),
                "seo": context.get("seo"),
                "multilingual": context.get("multilingual"),
                "quality": context.get("quality"),
            },
            indent=2,
            ensure_ascii=False,
        )
