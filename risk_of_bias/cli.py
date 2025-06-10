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
    force: bool = typer.Option(
        False, help="Force reprocessing even if JSON file exists"
    ),
) -> Framework:
    """
    Run risk of bias assessment on a manuscript.

    Processes a manuscript PDF file using the specified
    AI model and optional guidance document to perform risk of bias
    evaluation using the ROB2 framework.

    If a JSON file with the same name as the manuscript already exists,
    it will be loaded instead of reprocessing the PDF (unless --force is used).
    """
    manuscript_path = Path(manuscript)
    guidance_document_path = Path(guidance_document) if guidance_document else None

    output_json_path = manuscript_path.with_suffix(manuscript_path.suffix + ".json")
    output_md_path = manuscript_path.with_suffix(manuscript_path.suffix + ".md")
    output_html_path = manuscript_path.with_suffix(manuscript_path.suffix + ".html")

    # Check if JSON file already exists and load it if not forcing reprocessing
    if output_json_path.exists() and not force:
        if verbose:
            typer.echo(f"Found existing JSON file: {output_json_path}")
            typer.echo("Loading saved assessment instead of reprocessing...")

        try:
            completed_framework = Framework.load(output_json_path)
            # Ensure manuscript filename is set (for backward compatibility)
            if not completed_framework.manuscript:
                completed_framework.manuscript = manuscript_path.name
                # Save the updated framework with manuscript filename
                completed_framework.save(output_json_path)
                if verbose:
                    typer.echo(
                        "Updated existing assessment with manuscript"
                        f" filename: {manuscript_path.name}"
                    )
            if verbose:
                typer.echo("Successfully loaded existing assessment.")
        except Exception as e:
            if verbose:
                typer.echo(f"Error loading existing JSON file: {e}")
                typer.echo("Proceeding with fresh assessment...")
            completed_framework = run_framework(
                manuscript=manuscript_path,
                framework=get_rob2_framework(),
                model=model,
                guidance_document=guidance_document_path,
                verbose=verbose,
            )

    else:
        completed_framework = run_framework(
            manuscript=manuscript_path,
            framework=get_rob2_framework(),
            model=model,
            guidance_document=guidance_document_path,
            verbose=verbose,
        )

        completed_framework.save(output_json_path)
        if verbose:
            typer.echo(f"Assessment saved to: {output_json_path}")

    completed_framework.export_to_markdown(output_md_path)
    completed_framework.export_to_html(output_html_path)

    return completed_framework


if __name__ == "__main__":
    app()
