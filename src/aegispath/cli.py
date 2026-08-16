"""Command-line entry points for AegisPath."""

from __future__ import annotations

from pathlib import Path

import typer

from aegispath.agents.verify import VerifyAgent
from aegispath.core.context import ContextEngine

app = typer.Typer(add_completion=False)


@app.command()
def verify(target: Path) -> None:
    """Verify a tool directory against static and policy checks."""
    result = VerifyAgent().run(
        ContextEngine(target).get_context("verification", "verify"),
        target_path=target,
    )
    typer.echo(result.message)
    raise typer.Exit(code=0 if result.success else 1)


@app.command()
def decisions(root: Path = Path(".")) -> None:
    """List the most recent recorded decisions."""
    from aegispath.core.decisions import DecisionLog

    for record in DecisionLog(root=root).list_recent():
        typer.echo(record.model_dump_json())


if __name__ == "__main__":
    app()
