"""Capability declaration loading and conservative usage inference."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from aegispath.core.policy import (
    CapabilityDeclaration,
    CapabilityLevel,
    PolicyEngine,
    PolicyResult,
    PolicyViolation,
)


def load_capability_declaration(
    target: Path,
) -> tuple[CapabilityDeclaration | None, str | None]:
    """Load ``CAPABILITIES.yaml`` from a file or directory target."""
    path = target if target.is_file() else target / "CAPABILITIES.yaml"
    if not path.is_file():
        return None, None
    try:
        data: Any = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return CapabilityDeclaration.model_validate(data), str(path)
    except (OSError, ValueError):
        return None, str(path)


def infer_used_capabilities(target: Path) -> dict[str, CapabilityLevel]:
    """Infer only obvious capability markers from source text."""
    paths = [target] if target.is_file() else [p for p in target.rglob("*") if p.is_file()]
    text = "\n".join(
        p.read_text(encoding="utf-8", errors="replace") for p in paths if p.suffix == ".py"
    ).lower()
    markers = {
        "network": ("socket", "requests", "http://", "https://"),
        "filesystem": ("open(", "pathlib", "read_text", "write_text"),
        "process": ("subprocess", "os.system", "popen("),
        "credentials": ("api_key", "password =", "getpass"),
        "persistence": ("database", "sqlite", "registry"),
    }
    return {
        name: CapabilityLevel.LIMITED
        for name, terms in markers.items()
        if any(term in text for term in terms)
    }


def check_capability_consistency(
    declaration: CapabilityDeclaration | None,
    used: dict[str, CapabilityLevel],
    engine: PolicyEngine,
) -> PolicyResult:
    """Report inferred capabilities absent from the declaration."""
    result = engine.check_capability_declaration(declaration)
    if declaration is None:
        return result
    for name in used:
        if getattr(declaration, name) == CapabilityLevel.NONE:
            result.violations.append(
                PolicyViolation(
                    rule_id="CAP-003",
                    severity="error",
                    message=f"Inferred {name} capability is not declared.",
                )
            )
    result.passed = not result.errors
    return result
