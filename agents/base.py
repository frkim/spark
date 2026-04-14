"""Base agent — wraps Azure OpenAI chat completion with JSON output."""

from __future__ import annotations

import json
import logging
from typing import Any

from openai import AsyncAzureOpenAI

from config import settings
from observability import PipelineTracer, TraceSpan

logger = logging.getLogger(__name__)


def _get_client() -> AsyncAzureOpenAI:
    return AsyncAzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
    )


class BaseAgent:
    """A single-purpose agent that calls Azure OpenAI and returns JSON."""

    name: str = "base_agent"
    instructions: str = "You are a helpful assistant. Return valid JSON only."

    def __init__(self, client: AsyncAzureOpenAI | None = None) -> None:
        self.client = client or _get_client()

    async def run(
        self,
        context: dict[str, Any],
        tracer: PipelineTracer | None = None,
    ) -> dict[str, Any]:
        span: TraceSpan | None = None
        if tracer:
            span = tracer.start_span(self.name)

        user_content = self._build_user_message(context)

        try:
            response = await self.client.chat.completions.create(
                model=settings.azure_openai_model,
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": user_content},
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )

            raw = response.choices[0].message.content or "{}"
            result = json.loads(raw)

            if span and tracer:
                usage = response.usage
                tracer.end_span(
                    span,
                    tokens_prompt=usage.prompt_tokens if usage else 0,
                    tokens_completion=usage.completion_tokens if usage else 0,
                    status="ok",
                )

            return result

        except Exception as exc:
            logger.error("Agent %s failed: %s", self.name, exc)
            if span and tracer:
                tracer.end_span(span, status="error", flags=[str(exc)])
            return {"error": str(exc)}

    def _build_user_message(self, context: dict[str, Any]) -> str:
        """Override in subclasses to customise the user prompt."""
        return json.dumps(context, indent=2, ensure_ascii=False)
