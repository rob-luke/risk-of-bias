from pathlib import Path
from typing import Optional

import typer

from risk_of_bias.config import settings
from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.run_framework import run_framework
from risk_of_bias.types._framework_types import Framework

app = typer.Typer(help="Run risk of bias assessment")


@app.command()
def main(
    manuscript: str = typer.Argument(
        ..., exists=True, readable=True, help="Path to the manuscript PDF"
    ),
    model: str = typer.Option(settings.fast_ai_model, help="OpenAI model name"),
    guidance_document: Optional[str] = typer.Option(
        None, exists=True, readable=True, help="Optional guidance document"
    ),
    verbose: bool = typer.Option(True, help="Enable verbose output for debugging"),
) -> Framework:
    """
    Run risk of bias assessment on a manuscript.

    Processes a manuscript PDF file using the specified
    AI model and optional guidance document to perform risk of bias
    evaluation using the ROB2 framework.
    """
    manuscript_path = Path(manuscript)
    guidance_document_path = Path(guidance_document) if guidance_document else None

    completed_framework = run_framework(
        manuscript=manuscript_path,
        framework=get_rob2_framework(),
        model=model,
        guidance_document=guidance_document_path,
        verbose=verbose,
    )

    return completed_framework


if __name__ == "__main__":
    app()
