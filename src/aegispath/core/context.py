"""Context engine – repository and policy awareness for agents."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ContextBundle(BaseModel):
    """Everything an agent should see for a given task."""

    tool_family: str
    task: str
    coding_standards: str = ""
    relevant_docs: list[str] = Field(default_factory=list)
    previous_designs: list[str] = Field(default_factory=list)
    capability_templates: dict[str, Any] = Field(default_factory=dict)
    policy_summary: str = ""
    extra: dict[str, Any] = Field(default_factory=dict)


class ContextEngine:
    """
    Provides structured context to agents.

    v0 is deliberately simple: it reads from known template and docs locations.
    Later versions will add indexing, embeddings, and change-aware retrieval.
    """

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.cwd()
        self.templates_dir = self.root / "templates"
        self.docs_dir = self.root / "docs"

    def get_context(self, tool_family: str, task: str) -> ContextBundle:
        coding_standards = self._read_if_exists(self.templates_dir / "coding_standards.md")
        design_template = self._read_if_exists(self.templates_dir / "tool_design.md")
        threat_template = self._read_if_exists(self.templates_dir / "threat_model.md")
        charter = self._read_if_exists(self.docs_dir / "development-charter.md")

        return ContextBundle(
            tool_family=tool_family,
            task=task,
            coding_standards=coding_standards,
            relevant_docs=[d for d in (design_template, threat_template, charter) if d],
            policy_summary=(
                "All work must comply with the AegisPath Development Charter. "
                "Capability declarations, authorized-use notices, and verification gates are mandatory."
            ),
            extra={
                "root": str(self.root),
                "templates_available": [
                    p.name for p in self.templates_dir.glob("*.md")
                ]
                if self.templates_dir.exists()
                else [],
            },
        )

    def _read_if_exists(self, path: Path) -> str:
        try:
            if path.is_file():
                return path.read_text(encoding="utf-8")
        except OSError:
            pass
        return ""
