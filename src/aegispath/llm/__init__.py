"""Pluggable LLM backends for AegisPath agents."""

from aegispath.llm.base import LLMBackend, LLMMessage, LLMResponse
from aegispath.llm.mock import MockLLMBackend

__all__ = [
    "LLMBackend",
    "LLMMessage",
    "LLMResponse",
    "MockLLMBackend",
    "get_backend",
]


def get_backend(name: str | None = None, **kwargs) -> LLMBackend:
    """
    Factory for LLM backends.

    Supported names:
      - "mock" (default) – deterministic offline backend for tests and development
      - "openai" / "openai_compatible" – OpenAI-compatible HTTP API

    Configuration is also read from environment variables when not supplied:
      AEGISPATH_LLM_BACKEND, AEGISPATH_LLM_API_KEY, AEGISPATH_LLM_BASE_URL,
      AEGISPATH_LLM_MODEL
    """
    import os

    name = (name or os.environ.get("AEGISPATH_LLM_BACKEND", "mock")).lower().strip()

    if name in ("mock", "dummy", "test"):
        return MockLLMBackend(**kwargs)

    if name in ("openai", "openai_compatible", "compatible"):
        from aegispath.llm.openai_compatible import OpenAICompatibleBackend

        return OpenAICompatibleBackend(**kwargs)

    raise ValueError(f"Unknown LLM backend {name!r}. Supported: mock, openai_compatible")
