"""Lightweight observability — trace spans, run metadata, and timing."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field


@dataclass
class TraceSpan:
    agent_name: str
    run_id: str
    start_time: float = 0.0
    end_time: float = 0.0
    latency_ms: float = 0.0
    tokens_prompt: int = 0
    tokens_completion: int = 0
    status: str = "pending"
    flags: list[str] = field(default_factory=list)


class PipelineTracer:
    """Collects trace spans for a single pipeline run."""

    def __init__(self) -> None:
        self.run_id: str = str(uuid.uuid4())
        self.spans: list[TraceSpan] = []
        self._active: TraceSpan | None = None

    def start_span(self, agent_name: str) -> TraceSpan:
        span = TraceSpan(agent_name=agent_name, run_id=self.run_id, start_time=time.time())
        self._active = span
        return span

    def end_span(
        self,
        span: TraceSpan,
        *,
        tokens_prompt: int = 0,
        tokens_completion: int = 0,
        status: str = "ok",
        flags: list[str] | None = None,
    ) -> None:
        span.end_time = time.time()
        span.latency_ms = round((span.end_time - span.start_time) * 1000, 1)
        span.tokens_prompt = tokens_prompt
        span.tokens_completion = tokens_completion
        span.status = status
        span.flags = flags or []
        self.spans.append(span)
        self._active = None

    @property
    def total_latency_ms(self) -> float:
        return round(sum(s.latency_ms for s in self.spans), 1)

    @property
    def total_tokens(self) -> int:
        return sum(s.tokens_prompt + s.tokens_completion for s in self.spans)

    def summary(self) -> dict:
        return {
            "run_id": self.run_id,
            "total_latency_ms": self.total_latency_ms,
            "total_tokens": self.total_tokens,
            "spans": [
                {
                    "agent": s.agent_name,
                    "latency_ms": s.latency_ms,
                    "tokens": s.tokens_prompt + s.tokens_completion,
                    "status": s.status,
                    "flags": s.flags,
                }
                for s in self.spans
            ],
        }
