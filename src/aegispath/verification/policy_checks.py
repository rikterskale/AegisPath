"""Policy-level checks: notices, secrets, capability metadata & consistency."""

from __future__ import annotations

from pathlib import Path

from aegispath.core.policy import PolicyEngine, PolicyResult, PolicyViolation
from aegispath.verification.capabilities import (
    check_capability_consistency,
    infer_used_capabilities,
    load_capability_declaration,
)


def _collect_text(target: Path) -> str:
    texts: list[str] = []
    if target.is_file():
        try:
            texts.append(target.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            pass
    elif target.is_dir():
        for p in target.rglob("*"):
            if p.is_file() and p.suffix in {".md", ".py", ".txt", ".rst", ".yaml", ".yml"}:
                try:
                    texts.append(p.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    continue
    return "\n".join(texts)


def run_policy_checks(target: Path, engine: PolicyEngine | None = None) -> PolicyResult:
    """
    Charter-derived policy checks against a path.

    1. Authorized-use notice present
    2. No obvious secret patterns
    3. Capability declaration present (YAML or CAPABILITIES dict)
    4. Declared capabilities cover heuristically detected usage
    """
    engine = engine or PolicyEngine()
    all_violations: list[PolicyViolation] = []

    combined = _collect_text(target)

    notice_result = engine.check_authorized_use_notice(combined)
    all_violations.extend(notice_result.violations)

    secret_result = engine.check_secrets_patterns(combined)
    all_violations.extend(secret_result.violations)

    declaration, _source = load_capability_declaration(target)
    used = infer_used_capabilities(target)
    cap_result = check_capability_consistency(declaration, used, engine)
    all_violations.extend(cap_result.violations)

    errors = [v for v in all_violations if v.severity == "error"]
    return PolicyResult(passed=len(errors) == 0, violations=all_violations)
