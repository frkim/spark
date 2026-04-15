"""Base agent — runs on the new Microsoft Foundry Agent Service experience.

Uses the Responses API (azure-ai-projects ≥ 2.0) instead of the deprecated
Assistants/classic agents API.  Agents created this way appear under
Build → Agents in the Foundry portal.

Reference: https://learn.microsoft.com/azure/foundry/agents/how-to/migrate
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential

from config import settings
from observability import PipelineTracer, TraceSpan

logger = logging.getLogger(__name__)

_project_cache: AIProjectClient | None = None


def _get_foundry_client() -> AIProjectClient:
    """Return a cached AIProjectClient (used for agent CRUD)."""
    global _project_cache
    if _project_cache is None:
        _project_cache = AIProjectClient(
            endpoint=settings.foundry_project_endpoint,
            credential=DefaultAzureCredential(),
        )
    return _project_cache


class FoundryAgent:
    """A single-purpose agent that runs on the new Foundry Agent Service.

    Lifecycle per call:
    1. ``create_version`` — register (or reuse) the agent definition.
    2. ``conversations.create`` — open a conversation with the user message.
    3. ``responses.create`` — invoke the agent via the Responses API.
    4. Parse the JSON output.
    """

    name: str = "base-foundry-agent"
    instructions: str = "You are a helpful assistant. Return valid JSON only."

    def __init__(self, client: AIProjectClient | None = None) -> None:
        self.project = client or _get_foundry_client()
        self.openai = self.project.get_openai_client()
        self._agent_name: str | None = None

    def _ensure_agent(self) -> str:
        """Create (or reuse) the prompt-agent version and return its name."""
        if self._agent_name is None:
            agent = self.project.agents.create_version(
                agent_name=self.name,
                definition=PromptAgentDefinition(
                    model=settings.azure_openai_model,
                    instructions=self.instructions,
                    temperature=0.3,
                ),
            )
            self._agent_name = agent.name
            logger.info(
                "Created Foundry agent %s (version %s)", agent.name, agent.version
            )
        return self._agent_name

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
            agent_name = await asyncio.to_thread(self._ensure_agent)

            # Create a conversation with the user message
            conversation = await asyncio.to_thread(
                self.openai.conversations.create,
                items=[
                    {
                        "type": "message",
                        "role": "user",
                        "content": user_content,
                    }
                ],
            )

            # Invoke the agent via the Responses API
            response = await asyncio.to_thread(
                self.openai.responses.create,
                input=user_content,
                conversation=conversation.id,
                extra_body={
                    "agent_reference": {
                        "name": agent_name,
                        "type": "agent_reference",
                    }
                },
            )

            raw = response.output_text or ""

            # Parse JSON (strip markdown fences if present)
            text = raw.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                lines = lines[1:]  # skip opening fence
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                text = "\n".join(lines)

            result = json.loads(text) if text else {}

            if span and tracer:
                usage = getattr(response, "usage", None)
                tracer.end_span(
                    span,
                    tokens_prompt=getattr(usage, "input_tokens", 0) if usage else 0,
                    tokens_completion=getattr(usage, "output_tokens", 0) if usage else 0,
                    status="ok",
                )

            return result

        except Exception as exc:
            logger.error("Foundry Agent %s failed: %s", self.name, exc)
            if span and tracer:
                tracer.end_span(span, status="error", flags=[str(exc)])
            return {"error": str(exc)}

    def _build_user_message(self, context: dict[str, Any]) -> str:
        """Override in subclasses to customise the user prompt."""
        return json.dumps(context, indent=2, ensure_ascii=False)

    def cleanup(self) -> None:
        """Delete all versions of this agent definition."""
        if self._agent_name:
            try:
                self.project.agents.delete(self._agent_name)
                logger.info("Deleted Foundry agent %s", self._agent_name)
            except Exception:
                pass
            self._agent_name = None
