"""Policy engine – machine-enforceable rules derived from the Development Charter."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class CapabilityLevel(str, Enum):
    NONE = "none"
    LIMITED = "limited"
    UNRESTRICTED = "unrestricted"


class CapabilityDeclaration(BaseModel):
    """Structured declaration that every tool must provide."""

    network: CapabilityLevel = CapabilityLevel.NONE
    filesystem: CapabilityLevel = CapabilityLevel.NONE
    process: CapabilityLevel = CapabilityLevel.NONE
    credentials: CapabilityLevel = CapabilityLevel.NONE
    persistence: CapabilityLevel = CapabilityLevel.NONE
    required_privileges: list[str] = Field(default_factory=list)
    notes: str = ""


class PolicyViolation(BaseModel):
    rule_id: str
    severity: str  # "error" | "warning"
    message: str
    location: str | None = None


class PolicyResult(BaseModel):
    passed: bool
    violations: list[PolicyViolation] = Field(default_factory=list)

    @property
    def errors(self) -> list[PolicyViolation]:
        return [v for v in self.violations if v.severity == "error"]


class PolicyEngine:
    """
    Evaluates artifacts against AegisPath policy rules.

    This is intentionally conservative. New high-risk patterns should be
    added here (or in rule plugins) rather than relying on the model to
    self-censor.
    """

    def __init__(self) -> None:
        self._rules: list[Any] = []  # placeholder for future rule plugins

    def check_capability_declaration(
        self, declaration: CapabilityDeclaration | None
    ) -> PolicyResult:
        violations: list[PolicyViolation] = []

        if declaration is None:
            violations.append(
                PolicyViolation(
                    rule_id="CAP-001",
                    severity="error",
                    message="Missing capability declaration. Every tool must declare its capabilities.",
                )
            )
            return PolicyResult(passed=False, violations=violations)

        # Basic completeness checks – expand later
        if not declaration.required_privileges and any(
            level != CapabilityLevel.NONE
            for level in (
                declaration.network,
                declaration.filesystem,
                declaration.process,
                declaration.credentials,
                declaration.persistence,
            )
        ):
            violations.append(
                PolicyViolation(
                    rule_id="CAP-002",
                    severity="warning",
                    message="Capabilities are declared but required_privileges list is empty.",
                )
            )

        return PolicyResult(
            passed=len([v for v in violations if v.severity == "error"]) == 0,
            violations=violations,
        )

    def check_authorized_use_notice(self, text: str) -> PolicyResult:
        """Require an explicit authorized-use / dual-use notice in documentation."""
        required_phrases = [
            "authorized",
            "authorization",
            "authorized use",
            "dual-use",
            "authorized testing",
        ]
        text_lower = text.lower()
        found = any(phrase in text_lower for phrase in required_phrases)

        if not found:
            return PolicyResult(
                passed=False,
                violations=[
                    PolicyViolation(
                        rule_id="NOTICE-001",
                        severity="error",
                        message=(
                            "Missing authorized-use / dual-use notice. "
                            "Documentation must clearly state that the tool is for authorized testing only."
                        ),
                    )
                ],
            )
        return PolicyResult(passed=True)

    def check_secrets_patterns(self, content: str) -> PolicyResult:
        """Very basic secret pattern detection. Replace with proper scanner later."""
        # Intentionally minimal – real implementation should use detect-secrets / trufflehog / etc.
        suspicious = [
            "AKIA",  # AWS key prefix
            "-----BEGIN PRIVATE KEY-----",
            "-----BEGIN RSA PRIVATE KEY-----",
            "password = ",
            "api_key = ",
            "secret = ",
        ]
        violations: list[PolicyViolation] = []
        for pattern in suspicious:
            if pattern.lower() in content.lower():
                violations.append(
                    PolicyViolation(
                        rule_id="SECRET-001",
                        severity="error",
                        message=f"Possible secret or credential pattern detected: '{pattern}'",
                    )
                )
        return PolicyResult(
            passed=len(violations) == 0,
            violations=violations,
        )
