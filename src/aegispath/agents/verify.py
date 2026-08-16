"""Verify agent – runs static, policy, and capability consistency checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aegispath.agents.base import AgentResult, BaseAgent
from aegispath.core.context import ContextBundle
from aegispath.core.policy import PolicyEngine
from aegispath.verification.capabilities import (
    infer_used_capabilities,
    load_capability_declaration,
)
from aegispath.verification.policy_checks import run_policy_checks
from aegispath.verification.static import run_static_checks


class VerifyAgent(BaseAgent):
    name = "verify"

    def __init__(self) -> None:
        self.policy_engine = PolicyEngine()

    def run(self, context: ContextBundle, **kwargs: Any) -> AgentResult:
        target_path: Path | None = kwargs.get("target_path")
        if target_path is None:
            return AgentResult(
                success=False,
                message="verify requires target_path=Path(...)",
            )

        target_path = Path(target_path)
        if not target_path.exists():
            return AgentResult(
                success=False,
                message=f"Target path does not exist: {target_path}",
            )

        static_result = run_static_checks(target_path)
        policy_result = run_policy_checks(target_path, self.policy_engine)
        declaration, cap_source = load_capability_declaration(target_path)
        used = infer_used_capabilities(target_path)

        overall_passed = static_result.passed and policy_result.passed

        findings = {
            "static": static_result.model_dump(),
            "policy": policy_result.model_dump(),
            "capabilities": {
                "declaration": declaration.model_dump() if declaration else None,
                "source": cap_source or None,
                "inferred_usage": used,
            },
        }

        error_count = len(static_result.issues) + len(policy_result.errors)
        message = (
            f"Verification {'passed' if overall_passed else 'failed'} ({error_count} issue(s))"
        )

        return AgentResult(
            success=overall_passed,
            message=message,
            artifacts={"findings": findings, "target": str(target_path)},
        )
