"""Prompt / response logging for auditability."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from aegispath.llm.base import LLMMessage, LLMResponse, PromptLogEntry


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


class PromptLogger:
    """
    Writes structured JSONL logs of LLM interactions.

    By default only hashes are stored (safer). Set AEGISPATH_LLM_LOG_FULL=1
    to store full prompts and responses (useful for local debugging, risky
    if prompts ever contain sensitive data).
    """

    def __init__(self, log_dir: Path | None = None) -> None:
        self.log_dir = log_dir or Path(os.environ.get("AEGISPATH_LOG_DIR", ".aegispath/llm_logs"))
        self.store_full = os.environ.get("AEGISPATH_LLM_LOG_FULL", "").lower() in (
            "1",
            "true",
            "yes",
        )
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        backend_name: str,
        messages: list[LLMMessage],
        response: LLMResponse,
        *,
        temperature: float,
        max_tokens: int,
        metadata: dict[str, Any] | None = None,
    ) -> PromptLogEntry:
        system = next((m.content for m in messages if m.role == "system"), "")
        user = next((m.content for m in messages if m.role == "user"), "")
        # If multiple user messages, concatenate for logging simplicity
        if not user:
            user = "\n".join(m.content for m in messages if m.role == "user")

        entry = PromptLogEntry(
            backend=backend_name,
            model=response.model,
            system_prompt_hash=_hash(system),
            user_prompt_hash=_hash(user),
            response_hash=_hash(response.content),
            temperature=temperature,
            max_tokens=max_tokens,
            usage=response.usage,
            store_full_content=self.store_full,
            system_prompt=system if self.store_full else None,
            user_prompt=user if self.store_full else None,
            response=response.content if self.store_full else None,
            metadata=metadata or {},
        )

        log_file = self.log_dir / "interactions.jsonl"
        with log_file.open("a", encoding="utf-8") as f:
            f.write(entry.model_dump_json() + "\n")

        return entry
