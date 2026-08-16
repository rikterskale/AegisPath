"""Base agent contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field

from aegispath.core.context import ContextBundle


class AgentResult(BaseModel):
    success: bool
    message: str = ""
    artifacts: dict[str, Any] = Field(default_factory=dict)
    raw_model_output: str | None = None  # for audit logging later


class BaseAgent(ABC):
    """
    All agents share a common contract:

    - They receive a ContextBundle.
    - They may only write within an allow-listed set of paths (enforced by orchestrator).
    - They return an AgentResult; they never commit or release by themselves.
    """

    name: str = "base"

    @abstractmethod
    def run(self, context: ContextBundle, **kwargs: Any) -> AgentResult:
        ...
