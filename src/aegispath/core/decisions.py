"""Decision logging – durable accept/reject/back records for audit."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field

DecisionAction = Literal[
    "accept",
    "reject",
    "back",
    "regenerate",
    "start",
    "write",
    "abort",
    "note",
]


class DecisionRecord(BaseModel):
    """One human or system decision in a design/implement session."""

    id: str = Field(default_factory=lambda: str(uuid4())[:12])
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    session_id: str = ""
    tool_family: str = ""
    phase: str = ""
    action: DecisionAction
    note: str = ""
    content_hash: str = ""  # hash of design draft or file package when relevant
    metadata: dict[str, Any] = Field(default_factory=dict)


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


class DecisionLog:
    """
    Append-only JSONL decision log under .aegispath/decisions/.

    Does not commit or release anything – audit trail only.
    """

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.cwd()
        self.log_dir = self.root / ".aegispath" / "decisions"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "decisions.jsonl"

    def record(
        self,
        action: DecisionAction,
        *,
        session_id: str = "",
        tool_family: str = "",
        phase: str = "",
        note: str = "",
        content: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> DecisionRecord:
        rec = DecisionRecord(
            session_id=session_id,
            tool_family=tool_family,
            phase=phase,
            action=action,
            note=note,
            content_hash=content_hash(content) if content else "",
            metadata=metadata or {},
        )
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(rec.model_dump_json() + "\n")
        return rec

    def list_recent(self, limit: int = 20) -> list[DecisionRecord]:
        if not self.log_file.is_file():
            return []
        lines = self.log_file.read_text(encoding="utf-8").strip().splitlines()
        records: list[DecisionRecord] = []
        for line in lines[-limit:]:
            try:
                records.append(DecisionRecord.model_validate_json(line))
            except Exception:  # noqa: BLE001
                continue
        return list(reversed(records))

    def list_for_session(self, session_id: str) -> list[DecisionRecord]:
        return [r for r in self.list_recent(limit=500) if r.session_id == session_id]
