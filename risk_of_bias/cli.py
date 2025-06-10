from pathlib import Path
from typing import List, Optional

import typer

from risk_of_bias.config import settings
from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.run_framework import run_framework
from risk_of_bias.types._framework_types import Framework

app = typer.Typer(help="Run risk of bias assessment")


@app.command()
def analyse(
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


@app.command()
def analyse_directory(
    directory: str = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        help="Directory containing manuscript PDFs",
    ),
    model: str = typer.Option(settings.fast_ai_model, help="OpenAI model name"),
    guidance_document: Optional[str] = typer.Option(
        None,
        exists=True,
        readable=True,
        help="Optional guidance document",
    ),
    verbose: bool = typer.Option(True, help="Enable verbose output for debugging"),
    force: bool = typer.Option(
        False,
        help="Force reprocessing even if JSON file exists",
    ),
) -> List[Framework]:
    """Analyse every PDF found directly in a directory.

    Parameters
    ----------
    directory : str
        Path to the directory containing PDF manuscripts.
    model : str
        OpenAI model to use for all analyses.
    guidance_document : Optional[str]
        Optional guidance document passed to each analysis.
    verbose : bool
        Enable verbose output from the ``analyse`` command.
    force : bool
        Force reprocessing even if JSON files already exist.

    Returns
    -------
    list[Framework]
        List of completed frameworks, one per processed manuscript.
    """

    directory_path = Path(directory)
    guidance_document_path = Path(guidance_document) if guidance_document else None

    results: list[Framework] = []
    for pdf_path in sorted(
        p
        for p in directory_path.iterdir()
        if p.is_file() and p.suffix.lower() == ".pdf"
    ):
        if verbose:
            typer.echo(f"Analysing {pdf_path.name}")
        framework = analyse(
            manuscript=str(pdf_path),
            model=model,
            guidance_document=(
                str(guidance_document_path) if guidance_document_path else None
            ),
            verbose=verbose,
            force=force,
        )
        results.append(framework)

    return results


@app.command()
def web(
    host: str = typer.Option("127.0.0.1", help="Host address"),
    port: int = typer.Option(8000, help="Port number"),
    reload: bool = typer.Option(
        True, "--reload/--no-reload", help="Enable auto-reload during development"
    ),
) -> None:
    """Launch the web interface using uvicorn."""
    import uvicorn

    uvicorn.run(
        "risk_of_bias.web:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    app()
