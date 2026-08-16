"""Abstract LLM backend contract and shared types."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Literal, Sequence

from pydantic import BaseModel, Field


class LLMMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class LLMResponse(BaseModel):
    content: str
    model: str = "unknown"
    usage: dict[str, int] = Field(default_factory=dict)
    raw: dict[str, Any] = Field(default_factory=dict)
    finish_reason: str | None = None


class LLMBackend(ABC):
    """
    Minimal interface every backend must implement.

    Backends must never execute tools or write files; they only return text.
    All side effects (logging, etc.) are handled by the caller or a thin wrapper.
    """

    name: str = "base"

    @abstractmethod
    def complete(
        self,
        messages: Sequence[LLMMessage],
        *,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> LLMResponse:
        """Synchronous completion. Prefer low temperature for design work."""
        ...

    def complete_text(
        self,
        system: str,
        user: str,
        *,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> LLMResponse:
        """Convenience helper for the common system+user pattern."""
        messages = [
            LLMMessage(role="system", content=system),
            LLMMessage(role="user", content=user),
        ]
        return self.complete(
            messages, temperature=temperature, max_tokens=max_tokens, **kwargs
        )


class PromptLogEntry(BaseModel):
    """Structured record of a single LLM interaction for audit."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    backend: str
    model: str
    system_prompt_hash: str
    user_prompt_hash: str
    response_hash: str
    temperature: float
    max_tokens: int
    usage: dict[str, int] = Field(default_factory=dict)
    # Full content is optional / controlled by config to avoid leaking sensitive prompts
    store_full_content: bool = False
    system_prompt: str | None = None
    user_prompt: str | None = None
    response: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
