"""Deterministic offline LLM backend for tests and local development."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from aegispath.llm.base import LLMBackend, LLMMessage, LLMResponse


class MockLLMBackend(LLMBackend):
    """Return a stable response without making network calls."""

    name = "mock"

    def __init__(self, response: str = "Mock response", **_: Any) -> None:
        self.response = response

    def complete(
        self,
        messages: Sequence[LLMMessage],
        *,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> LLMResponse:
        return LLMResponse(content=self.response, model="mock", usage={})
