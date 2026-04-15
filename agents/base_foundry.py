"""Base agent — runs on Azure AI Foundry Agent Service via azure-ai-agents SDK."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    AgentThreadCreationOptions,
    MessageRole,
    ThreadMessageOptions,
)
from azure.identity import DefaultAzureCredential

from config import settings
from observability import PipelineTracer, TraceSpan

logger = logging.getLogger(__name__)

_client_cache: AgentsClient | None = None


def _get_foundry_client() -> AgentsClient:
    global _client_cache
    if _client_cache is None:
        _client_cache = AgentsClient(
            endpoint=settings.foundry_project_endpoint,
            credential=DefaultAzureCredential(),
        )
    return _client_cache


class FoundryAgent:
    """A single-purpose agent that runs on Azure AI Foundry Agent Service.

    Each call creates a hosted agent, creates a thread with the user message,
    runs the agent, retrieves the response, and cleans up.
    """

    name: str = "base_foundry_agent"
    instructions: str = "You are a helpful assistant. Return valid JSON only."

    def __init__(self, client: AgentsClient | None = None) -> None:
        self.client = client or _get_foundry_client()
        self._agent_id: str | None = None

    def _ensure_agent(self) -> str:
        """Create (or reuse) the hosted agent definition."""
        if self._agent_id is None:
            agent = self.client.create_agent(
                model=settings.azure_openai_model,
                name=self.name,
                instructions=self.instructions,
                temperature=0.3,
            )
            self._agent_id = agent.id
            logger.info("Created Foundry agent %s -> %s", self.name, self._agent_id)
        return self._agent_id

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
            agent_id = await asyncio.to_thread(self._ensure_agent)

            # Build thread with initial user message
            thread_opts = AgentThreadCreationOptions(
                messages=[
                    ThreadMessageOptions(role=MessageRole.USER, content=user_content),
                ],
            )

            # Create thread + run and poll until completion (sync, off-loaded)
            run = await asyncio.to_thread(
                self.client.create_thread_and_process_run,
                agent_id=agent_id,
                thread=thread_opts,
            )

            # Retrieve the assistant's last text message
            msg_content = await asyncio.to_thread(
                self.client.messages.get_last_message_text_by_role,
                run.thread_id,
                MessageRole.AGENT,
            )
            raw = msg_content.text.value if msg_content and msg_content.text else ""

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
                tracer.end_span(
                    span,
                    tokens_prompt=getattr(run.usage, "prompt_tokens", 0) if run.usage else 0,
                    tokens_completion=getattr(run.usage, "completion_tokens", 0) if run.usage else 0,
                    status="ok",
                )

            # Clean up thread
            try:
                await asyncio.to_thread(self.client.threads.delete, run.thread_id)
            except Exception:
                pass

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
        """Delete the hosted agent definition."""
        if self._agent_id:
            try:
                self.client.delete_agent(self._agent_id)
                logger.info("Deleted Foundry agent %s", self._agent_id)
            except Exception:
                pass
            self._agent_id = None
