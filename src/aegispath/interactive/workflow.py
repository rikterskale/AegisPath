"""Small, human-gated workflows built on the decision log."""

from __future__ import annotations

from pathlib import Path

from aegispath.core.decisions import DecisionLog
from aegispath.llm import LLMBackend


class DesignWorkflow:
    """Record the start of a design session without writing implementation files."""

    def __init__(self, root: Path | None = None, backend: LLMBackend | None = None) -> None:
        self.root = root or Path.cwd()
        self.backend = backend
        self.log = DecisionLog(root=self.root)

    def start(self, tool_family: str) -> None:
        """Record a design-session start for later human review."""
        self.log.record(
            "start",
            tool_family=tool_family,
            phase="design",
            note="Design workflow started",
        )
