"""Design agent – produces architecture, threat model, and acceptance criteria."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aegispath.agents.base import AgentResult, BaseAgent
from aegispath.core.context import ContextBundle
from aegispath.llm import LLMBackend, get_backend
from aegispath.llm.base import LLMMessage
from aegispath.llm.logging import PromptLogger
from aegispath.llm.prompts import SYSTEM_PROMPT_DESIGN, build_design_user_prompt


class DesignAgent(BaseAgent):
    name = "design"

    def __init__(
        self,
        backend: LLMBackend | None = None,
        logger: PromptLogger | None = None,
        log_dir: Path | None = None,
    ) -> None:
        self.backend = backend or get_backend()
        self.logger = logger or PromptLogger(log_dir=log_dir)

    def run(self, context: ContextBundle, **kwargs: Any) -> AgentResult:
        """
        Produce a design document for the requested tool family.

        The LLM is given a strict system prompt that restates the Development
        Charter. Output is treated as untrusted and returned for human review
        and later verification; nothing is written to the repository by this
        agent.
        """
        operator_notes = kwargs.get("operator_notes", "")
        extra_context = "\n\n".join(context.relevant_docs[:3])  # keep prompt size reasonable

        user_prompt = build_design_user_prompt(
            tool_family=context.tool_family,
            coding_standards=context.coding_standards,
            extra_context=extra_context,
            operator_notes=operator_notes,
        )

        try:
            response = self.backend.complete_text(
                system=SYSTEM_PROMPT_DESIGN,
                user=user_prompt,
                temperature=0.2,
                max_tokens=4096,
            )
        except Exception as e:  # noqa: BLE001 – surface backend errors cleanly
            return AgentResult(
                success=False,
                message=f"LLM backend error: {e}",
                artifacts={"tool_family": context.tool_family},
            )

        # Audit log (hashes by default)
        log_entry = self.logger.log(
            backend_name=self.backend.name,
            messages=[
                LLMMessage(role="system", content=SYSTEM_PROMPT_DESIGN),
                LLMMessage(role="user", content=user_prompt),
            ],
            response=response,
            temperature=0.2,
            max_tokens=4096,
            metadata={
                "tool_family": context.tool_family,
                "task": context.task,
                "agent": self.name,
            },
        )

        return AgentResult(
            success=True,
            message=(
                f"Design produced by {self.backend.name} "
                f"(model={response.model}). "
                "Human review required before any implementation."
            ),
            artifacts={
                "tool_family": context.tool_family,
                "design_markdown": response.content,
                "model": response.model,
                "usage": response.usage,
                "log_entry_hashes": {
                    "system": log_entry.system_prompt_hash,
                    "user": log_entry.user_prompt_hash,
                    "response": log_entry.response_hash,
                },
            },
            raw_model_output=response.content,
        )
