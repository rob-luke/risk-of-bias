from pathlib import Path
from typing import Optional

import typer

from risk_of_bias.config import settings
from risk_of_bias.frameworks.rob2._rob2 import rob2_framework
from risk_of_bias.run_framework import run_framework

app = typer.Typer(help="Run risk of bias assessment")


@app.command()
def main(
    manuscript: Path = typer.Argument(
        ..., exists=True, readable=True, help="Path to the manuscript PDF"
    ),
    model: str = typer.Option(settings.fast_ai_model, help="OpenAI model name"),
    guidance_document: Optional[Path] = typer.Option(
        None, exists=True, readable=True, help="Optional guidance document"
    ),
) -> None:
    """Execute the risk of bias analysis."""

    response = run_framework(
        manuscript=manuscript,
        model=model,
        framework=rob2_framework,
        guidance_document=guidance_document,
    )
    typer.echo(response)


if __name__ == "__main__":  # pragma: no cover - entry point behaviour
    app()
