"""Orchestrator – sequences agents under policy and records decisions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aegispath.agents.base import AgentResult, BaseAgent
from aegispath.core.context import ContextEngine
from aegispath.core.policy import PolicyEngine
from aegispath.llm import LLMBackend, get_backend
from aegispath.llm.logging import PromptLogger


class Orchestrator:
    """
    Thin control plane.

    Responsibilities:
    - Load context
    - Inject the configured LLM backend into agents that need it
    - Invoke agents in the correct order
    - Enforce that verification runs before any “accept”
    - Record decisions (stubbed for now)
    - Never auto-commit or auto-release
    """

    def __init__(
        self,
        root: Path | None = None,
        backend: LLMBackend | None = None,
        log_dir: Path | None = None,
    ) -> None:
        self.root = root or Path.cwd()
        self.context_engine = ContextEngine(self.root)
        self.policy_engine = PolicyEngine()
        self.backend = backend or get_backend()
        self.logger = PromptLogger(log_dir=log_dir or (self.root / ".aegispath" / "llm_logs"))
        self._agents: dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent) -> None:
        self._agents[agent.name] = agent

    def run_design(self, tool_family: str, **kwargs: Any) -> AgentResult:
        context = self.context_engine.get_context(tool_family, task="design")
        agent = self._agents.get("design")
        if agent is None:
            return AgentResult(
                success=False,
                message="Design agent not registered. Register one before calling run_design.",
            )
        return agent.run(context, **kwargs)

    def run_verify(self, target_path: Path, **kwargs: Any) -> AgentResult:
        context = self.context_engine.get_context(tool_family="verification", task="verify")
        agent = self._agents.get("verify")
        if agent is None:
            return AgentResult(
                success=False,
                message="Verify agent not registered.",
            )
        return agent.run(context, target_path=target_path, **kwargs)

    def record_decision(self, decision: dict[str, Any]) -> None:
        """Placeholder for future structured decision logging."""
        # Future: write to decision_logs/ with timestamps, hashes, human decision.
        pass
