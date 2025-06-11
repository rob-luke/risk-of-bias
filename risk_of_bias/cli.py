from pathlib import Path
from typing import List, Optional

import typer

from risk_of_bias.config import settings
from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.run_framework import run_framework
from risk_of_bias.summary import export_summary
from risk_of_bias.summary import print_summary
from risk_of_bias.summary import summarise_frameworks
from risk_of_bias.types._framework_types import Framework

app = typer.Typer(help="Run risk of bias assessment", pretty_exceptions_enable=False)


@app.command()
def analyse(
    manuscript: str = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="Path to the manuscript PDF or directory containing PDFs",
    ),
    model: str = typer.Option(settings.fast_ai_model, help="OpenAI model name"),
    temperature: float = typer.Option(
        settings.temperature, help="Temperature for the OpenAI model"
    ),
    guidance_document: Optional[str] = typer.Option(
        None, exists=True, readable=True, help="Optional guidance document"
    ),
    verbose: bool = typer.Option(True, help="Enable verbose output for debugging"),
    force: bool = typer.Option(
        False, help="Force reprocessing even if JSON file exists"
    ),
) -> Optional[Framework]:
    """
    Run risk of bias assessment on a manuscript or directory of manuscripts.

    Processes a manuscript PDF file or all PDF files in a directory using the specified
    AI model and optional guidance document to perform risk of bias
    evaluation using the ROB2 framework.

    If a JSON file with the same name as the manuscript already exists,
    it will be loaded instead of reprocessing the PDF (unless --force is used).

    If a directory is provided, all PDF files within that directory will be processed,
    and a summary CSV file will be generated containing the risk of bias assessments
    for each manuscript that is compatible with tools such as robvis.
    """
    manuscript_path = Path(manuscript)

    # If input is a directory, process all PDFs in it
    if manuscript_path.is_dir():
        if verbose:
            typer.echo(f"Processing directory: {manuscript_path}")

        results: List[Framework] = []
        pdf_files = sorted(
            [
                p
                for p in manuscript_path.iterdir()
                if p.is_file() and p.suffix.lower() == ".pdf"
            ]
        )

        if not pdf_files:
            typer.echo(f"No PDF files found in directory: {manuscript_path}")
            return None

        for pdf_path in pdf_files:
            if verbose:
                typer.echo(f"Analysing {pdf_path.name}")
            framework = analyse(
                manuscript=str(pdf_path),
                model=model,
                temperature=temperature,
                guidance_document=guidance_document,
                verbose=verbose,
                force=force,
            )
            if framework is not None:
                results.append(framework)

            frameworks_summary = summarise_frameworks(results)
            print_summary(frameworks_summary)
            export_summary(
                frameworks_summary,
                path=manuscript_path / "risk_of_bias_summary.csv",
            )

        if verbose:
            typer.echo(f"Processed {len(results)} PDF files from directory")

        # Return the last framework for consistency with single file processing
        return results[-1] if results else None

    # Single file processing (existing logic)
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
                temperature=temperature,
            )

    else:
        completed_framework = run_framework(
            manuscript=manuscript_path,
            framework=get_rob2_framework(),
            model=model,
            guidance_document=guidance_document_path,
            verbose=verbose,
            temperature=temperature,
        )

        completed_framework.save(output_json_path)
        if verbose:
            typer.echo(f"Assessment saved to: {output_json_path}")

    completed_framework.export_to_markdown(output_md_path)
    completed_framework.export_to_html(output_html_path)

    return completed_framework


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
