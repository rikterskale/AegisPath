from pathlib import Path

from aegispath.core.context import ContextEngine


def test_context_engine_returns_requested_context(tmp_path: Path) -> None:
    context = ContextEngine(root=tmp_path).get_context("example", "build a tool")

    assert context.tool_family == "example"
    assert context.task == "build a tool"
    assert context.extra["root"] == str(tmp_path)
