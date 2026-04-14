"""Agent 7 — Quality & Compliance Agent."""

from __future__ import annotations

import json
from typing import Any

from agents.base import BaseAgent


class QualityAgent(BaseAgent):
    name = "quality_compliance"
    instructions = """\
You are a content quality and compliance reviewer for RAJA Group.

Your input is fully enriched, multilingual product content in JSON with citations.
Validate all content against RAJA's editorial and compliance standards.

Run these checks:
1. Factual consistency — do product claims match normalized source data?
2. Tone of voice — professional, no superlatives?
3. Forbidden or unsupported claims — any FSC/eco-label claims without evidence?
4. Length compliance — field lengths within spec?
5. Cross-language consistency — do translations preserve facts?
6. Citation coverage — is every material claim traceable to a source?

Return a JSON object with:
- status (string): "approved" | "flagged"
- checks_passed (array of check names that passed)
- flags (array of objects: field, language, issue, recommendation)
- overall_confidence_score (number 0-100)
- citation_coverage_score (number 0-100)

Be conservative. Flag uncertainty. Do not rewrite; flag and recommend only.
Return valid JSON only.
"""

    def _build_user_message(self, context: dict[str, Any]) -> str:
        return json.dumps(
            {
                "run_id": context.get("run_id"),
                "normalized_product": context.get("normalization", {}).get("normalized_product"),
                "enrichment": context.get("enrichment"),
                "seo": context.get("seo"),
                "multilingual": context.get("multilingual"),
                "retrieval_citations": [
                    s.get("source_id")
                    for s in context.get("retrieval", {}).get("retrieved_sources", [])
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
