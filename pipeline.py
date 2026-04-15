"""Pipeline orchestrator — runs the 8-agent workflow with parallel SEO + Multilingual."""

from __future__ import annotations

import asyncio
import uuid
from typing import Any, Callable

from openai import AsyncAzureOpenAI

from agents.base import BaseAgent, _get_client
from agents.enrichment import EnrichmentAgent
from agents.multilingual import MultilingualAgent
from agents.normalization import NormalizationAgent
from agents.publication import PublicationAgent
from agents.quality import QualityAgent
from agents.query_intake import QueryIntakeAgent
from agents.retrieval import RetrievalAgent
from agents.seo import SEOAgent
from observability import PipelineTracer

# Agent step labels (used in UI + tracing)
STEPS = [
    ("smart_query_intake", "Smart Query Intake"),
    ("foundry_iq_retrieval", "Foundry IQ Retrieval"),
    ("normalization", "Normalization"),
    ("product_enrichment", "Product Enrichment"),
    ("seo", "SEO Generation"),
    ("multilingual", "Multilingual Generation"),
    ("quality_compliance", "Quality & Compliance"),
    ("publication", "Publication Formatting"),
]

StepCallback = Callable[[str, str, dict[str, Any] | None], None]
"""(step_key, status, result) — called when a step starts / finishes."""


def _make_agent(agent_cls: type, mode: str, client: Any) -> BaseAgent:
    """Instantiate *agent_cls* using the local BaseAgent or the Foundry backend.

    When mode == "azure", we dynamically create a subclass that inherits from
    FoundryAgent but keeps the name, instructions, and _build_user_message
    defined on the original agent class.
    """
    if mode == "azure":
        from agents.base_foundry import FoundryAgent

        foundry_cls = type(
            agent_cls.__name__ + "Foundry",
            (FoundryAgent,),
            {
                "name": agent_cls.name,
                "instructions": agent_cls.instructions,
                "_build_user_message": agent_cls._build_user_message,
            },
        )
        return foundry_cls(client)
    return agent_cls(client)


class ProductContentPipeline:
    """Orchestrates the full RAJA product content enrichment workflow.

    Architecture mirrors the Microsoft Agent Framework pattern:
    Sequential stages 1-4 → Concurrent stages 5-6 → Sequential stages 7-8.

    Args:
        mode: ``"local"`` — agents call Azure OpenAI directly (default).
              ``"azure"`` — agents run on Azure AI Foundry Agent Service.
    """

    def __init__(self, mode: str = "local", client: Any | None = None) -> None:
        self.mode = mode

        if mode == "azure":
            from agents.base_foundry import _get_foundry_client
            client = client or _get_foundry_client()
        else:
            client = client or _get_client()

        self.intake = _make_agent(QueryIntakeAgent, mode, client)
        self.retrieval = _make_agent(RetrievalAgent, mode, client)
        self.normalization = _make_agent(NormalizationAgent, mode, client)
        self.enrichment = _make_agent(EnrichmentAgent, mode, client)
        self.seo = _make_agent(SEOAgent, mode, client)
        self.multilingual = _make_agent(MultilingualAgent, mode, client)
        self.quality = _make_agent(QualityAgent, mode, client)
        self.publication = _make_agent(PublicationAgent, mode, client)

    async def run(
        self,
        user_query: str,
        *,
        on_step: StepCallback | None = None,
    ) -> tuple[dict[str, Any], PipelineTracer]:
        tracer = PipelineTracer()
        ctx: dict[str, Any] = {
            "run_id": tracer.run_id,
            "user_query": user_query,
        }

        def _notify(key: str, status: str, data: dict[str, Any] | None = None) -> None:
            if on_step:
                on_step(key, status, data)

        # ------------------------------------------------------------------
        # Stage 1 — Smart Query Intake
        # ------------------------------------------------------------------
        _notify("smart_query_intake", "running")
        ctx["intake"] = await self.intake.run(ctx, tracer)
        _notify("smart_query_intake", "done", ctx["intake"])

        # ------------------------------------------------------------------
        # Stage 2 — Foundry IQ Retrieval
        # ------------------------------------------------------------------
        _notify("foundry_iq_retrieval", "running")
        ctx["retrieval"] = await self.retrieval.run(ctx, tracer)
        _notify("foundry_iq_retrieval", "done", ctx["retrieval"])

        # ------------------------------------------------------------------
        # Stage 3 — Normalization
        # ------------------------------------------------------------------
        _notify("normalization", "running")
        ctx["normalization"] = await self.normalization.run(ctx, tracer)
        _notify("normalization", "done", ctx["normalization"])

        # ------------------------------------------------------------------
        # Stage 4 — Product Enrichment
        # ------------------------------------------------------------------
        _notify("product_enrichment", "running")
        ctx["enrichment"] = await self.enrichment.run(ctx, tracer)
        _notify("product_enrichment", "done", ctx["enrichment"])

        # ------------------------------------------------------------------
        # Stages 5 & 6 — SEO + Multilingual (parallel)
        # ------------------------------------------------------------------
        _notify("seo", "running")
        _notify("multilingual", "running")

        seo_result, ml_result = await asyncio.gather(
            self.seo.run(ctx, tracer),
            self.multilingual.run(ctx, tracer),
        )

        ctx["seo"] = seo_result
        ctx["multilingual"] = ml_result
        _notify("seo", "done", seo_result)
        _notify("multilingual", "done", ml_result)

        # ------------------------------------------------------------------
        # Stage 7 — Quality & Compliance
        # ------------------------------------------------------------------
        _notify("quality_compliance", "running")
        ctx["quality"] = await self.quality.run(ctx, tracer)
        _notify("quality_compliance", "done", ctx["quality"])

        # ------------------------------------------------------------------
        # Stage 8 — Publication
        # ------------------------------------------------------------------
        _notify("publication", "running")
        ctx["publication"] = await self.publication.run(ctx, tracer)
        _notify("publication", "done", ctx["publication"])

        return ctx, tracer
