"""Lightweight static checks used by the verification agent."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class StaticIssue(BaseModel):
    path: str
    message: str
    severity: str = "error"


class StaticResult(BaseModel):
    passed: bool
    issues: list[StaticIssue] = Field(default_factory=list)


def run_static_checks(target: Path) -> StaticResult:
    """Return a clean result for an existing target.

    The policy and capability checks provide the substantive validation for
    the current reference tool; this hook is intentionally ready for future
    AST and secret-scanning checks.
    """
    if not target.exists():
        return StaticResult(
            passed=False,
            issues=[StaticIssue(path=str(target), message="Target does not exist")],
        )
    return StaticResult(passed=True)
