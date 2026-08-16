"""Tests for decision logging."""

from pathlib import Path

from aegispath.interactive.workflow import DesignWorkflow
from aegispath.llm.mock import MockLLMBackend

from aegispath.core.decisions import DecisionLog, content_hash


def test_content_hash_stable():
    assert content_hash("abc") == content_hash("abc")
    assert content_hash("abc") != content_hash("abd")


def test_decision_log_record_and_list(tmp_path: Path):
    log = DecisionLog(root=tmp_path)
    rec = log.record(
        "accept",
        session_id="s1",
        tool_family="demo",
        phase="done",
        note="test accept",
        content="# design",
    )
    assert rec.action == "accept"
    assert rec.content_hash
    recent = log.list_recent(limit=5)
    assert len(recent) >= 1
    assert recent[0].tool_family == "demo"


def test_design_workflow_logs_start(tmp_path: Path):
    wf = DesignWorkflow(root=tmp_path, backend=MockLLMBackend())
    wf.start("demo-tool")
    log = DecisionLog(root=tmp_path)
    records = log.list_recent(limit=10)
    assert any(r.action == "start" and r.tool_family == "demo-tool" for r in records)
