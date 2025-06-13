from pathlib import Path
from typing import List, Optional

import typer

from risk_of_bias.compare import compare_frameworks
from risk_of_bias.config import settings
from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.human import run_human_framework
from risk_of_bias.run_framework import run_framework
from risk_of_bias.summary import export_summary, print_summary, summarise_frameworks
from risk_of_bias.types._framework_types import Framework
from risk_of_bias.visualisation import plot_assessor_agreement

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
        None,
        exists=True,
        readable=True,
        help="PDF guidance document with domain-specific"
        " assessment criteria and AI calibration instructions",
    ),
    verbose: bool = typer.Option(True, help="Enable verbose output for debugging"),
    force: bool = typer.Option(
        False,
        help="Force reprocessing even if JSON file exists (ignore cached results)",
    ),
) -> Optional[Framework]:
    """
    Run risk of bias assessment on a manuscript or directory of manuscripts.

    Processes a manuscript PDF file or all PDF files in a directory using the specified
    AI model and optional guidance document to perform risk of bias
    evaluation using the ROB2 framework.

    The guidance document feature allows you to provide domain-specific assessment
    criteria, correct systematic AI interpretation issues, or apply specialized
    evaluation standards. This is particularly useful for specialized research
    domains or when consistent AI calibration is needed across multiple assessments.

    Results are automatically saved in JSON format containing complete assessment
    data including raw AI responses, evidence excerpts, and reasoning. If a JSON
    file with the same name as the manuscript already exists, it will be loaded
    instead of reprocessing the PDF (unless --force is used). This caching system
    enables efficient batch processing, data sharing, and reproducible research
    workflows.

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
def human(
    manuscript: str = typer.Argument(
        ..., exists=True, readable=True, help="Path to the manuscript PDF"
    ),
    force: bool = typer.Option(False, help="Force re-entry even if JSON file exists"),
) -> Framework:
    """Enter risk-of-bias results manually using the terminal."""

    manuscript_path = Path(manuscript)

    output_json_path = manuscript_path.with_suffix(manuscript_path.suffix + ".json")
    output_md_path = manuscript_path.with_suffix(manuscript_path.suffix + ".md")
    output_html_path = manuscript_path.with_suffix(manuscript_path.suffix + ".html")

    if output_json_path.exists() and not force:
        typer.echo(f"Found existing JSON file: {output_json_path}")
        framework = Framework.load(output_json_path)
    else:
        framework = run_human_framework(manuscript_path, get_rob2_framework())
        framework.save(output_json_path)
        typer.echo(f"Assessment saved to: {output_json_path}")

    framework.export_to_markdown(output_md_path)
    framework.export_to_html(output_html_path)

    return framework


@app.command()
def compare(
    framework1: str = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="Path to the first JSON assessment file",
    ),
    framework2: str = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="Path to the second JSON assessment file",
    ),
    output: Optional[str] = typer.Option(
        None,
        help="Output path for the comparison plot (PNG)."
        " If not specified, saves to comparison_plot.png",
    ),
    verbose: bool = typer.Option(True, help="Enable verbose output"),
) -> None:
    """
    Compare two risk-of-bias assessments from JSON files.

    Loads two completed risk-of-bias assessments and compares them,
    displaying a comparison table in the terminal and generating
    a visualization plot saved as a PNG file.

    The comparison shows agreement between the two assessments
    for each question in the framework.
    """
    framework1_path = Path(framework1)
    framework2_path = Path(framework2)

    if verbose:
        typer.echo(f"Loading first assessment: {framework1_path}")

    try:
        fw1 = Framework.load(framework1_path)
    except Exception as e:
        typer.echo(f"Error loading first framework: {e}", err=True)
        raise typer.Exit(1)

    if verbose:
        typer.echo(f"Loading second assessment: {framework2_path}")

    try:
        fw2 = Framework.load(framework2_path)
    except Exception as e:
        typer.echo(f"Error loading second framework: {e}", err=True)
        raise typer.Exit(1)

    if verbose:
        typer.echo("Comparing frameworks...")

    try:
        comparison_df = compare_frameworks(fw1, fw2)
    except Exception as e:
        typer.echo(f"Error comparing frameworks: {e}", err=True)
        raise typer.Exit(1)

    # Print the comparison table
    typer.echo("\nComparison Results:")
    typer.echo("=" * 80)

    # Display the table in a readable format
    for _, row in comparison_df.iterrows():
        assessor_cols = [
            c
            for c in comparison_df.columns
            if c
            not in {"domain_short", "question_short", "domain", "question", "agreement"}
        ]
        assessor1, assessor2 = assessor_cols[:2]

        agreement_mark = "✓" if row["agreement"] else "✗"
        typer.echo(
            f"{row['domain_short']}.{row['question_short']}: "
            f"{row[assessor1] or 'N/A'} vs {row[assessor2] or 'N/A'} "
            f"[{agreement_mark}]"
        )

    # Calculate and display overall agreement
    agreement_pct = comparison_df["agreement"].mean() * 100
    typer.echo("=" * 80)
    typer.echo(f"Overall Agreement: {agreement_pct:.1f}%")

    # Generate and save the plot
    if output is None:
        output_path = Path("comparison_plot.png")
    else:
        output_path = Path(output)

    if verbose:
        typer.echo(f"Generating comparison plot: {output_path}")

    try:
        fig = plot_assessor_agreement(comparison_df)
        fig.savefig(output_path, dpi=300, bbox_inches="tight")

        if verbose:
            typer.echo(f"Plot saved successfully to: {output_path}")

    except Exception as e:
        typer.echo(f"Error generating plot: {e}", err=True)
        raise typer.Exit(1)
    finally:
        # Close the figure to free memory
        import matplotlib.pyplot as plt

        plt.close(fig)


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
