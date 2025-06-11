from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Mapping

from rich.console import Console
from rich.table import Table

from risk_of_bias.types._framework_types import Framework


def load_frameworks_from_directory(directory: Path | str) -> List[Framework]:
    """Load multiple completed risk-of-bias assessments for batch analysis.

    This function enables systematic reviews and meta-analyses by batch-loading
    previously completed framework assessments from a directory. After conducting
    individual risk-of-bias assessments on multiple studies, researchers typically
    need to analyze patterns across their entire study collection. This function
    streamlines that process by automatically discovering and loading all completed
    assessments.

    The function is fault-tolerant, continuing to load valid frameworks even if
    some files are corrupted or incompatible. This robustness is essential when
    working with large collections of assessments that may have been created over
    time or by different researchers.

    Common use cases include:
    - Preparing data for systematic review summary tables
    - Generating cross-study bias pattern visualizations
    - Creating inputs for meta-analysis software
    - Quality assurance checks across assessment batches

    Parameters
    ----------
    directory : Path | str
        Directory containing previously saved framework JSON files from completed
        risk-of-bias assessments.

    Returns
    -------
    list[Framework]
        List of successfully loaded frameworks. Files that cannot be parsed
        (due to corruption, format changes, etc.) are silently ignored to
        ensure batch processing continues.

    Examples
    --------
    >>> frameworks = load_frameworks_from_directory("./completed_assessments/")
    >>> print(f"Loaded {len(frameworks)} completed assessments")
    """
    path = Path(directory)
    frameworks: list[Framework] = []
    for json_file in path.glob("*.json"):
        try:
            frameworks.append(Framework.load(json_file))
        except Exception:
            continue
    return frameworks


def summarise_frameworks(
    frameworks: List[Framework],
) -> Dict[str, Dict[str, str | None]]:
    """Extract domain-level risk judgements for comparative analysis across studies.

    This function transforms detailed framework assessments into a simplified summary
    format suitable for systematic review tables, meta-analysis inputs, and cross-study
    comparisons. By extracting only the final risk-of-bias judgements for each domain,
    it creates a standardized view that facilitates pattern recognition and evidence
    synthesis across multiple studies.

    The function specifically looks for "Risk-of-bias judgement" questions within each
    domain, which represent the final assessment conclusions after considering all
    signaling questions and evidence. This approach aligns with established risk-of-bias
    assessment methodologies where detailed questioning leads to domain-level
    judgements.

    Key applications include:
    - Creating summary tables for systematic review publications
    - Identifying studies with consistent bias patterns across domains
    - Preparing data for risk-of-bias visualization tools (e.g., RobVis)
    - Supporting meta-analysis decisions about study inclusion/weighting

    Parameters
    ----------
    frameworks : list[Framework]
        Completed framework assessments to summarise. These should contain
        domain-level "Risk-of-bias judgement" responses.

    Returns
    -------
    dict[str, dict[str, str | None]]
        Nested mapping structure where:
        - Outer keys: manuscript/study identifiers
        - Inner keys: domain names
        - Values: risk-of-bias judgements ("low", "some concerns", "high")
          or None if no judgement was recorded

    Examples
    --------
    >>> summary = summarise_frameworks(loaded_frameworks)
    >>> print(summary["Smith2023"]["Randomization Process"])
    'low'
    """
    summary: dict[str, dict[str, str | None]] = {}
    for fw in frameworks:
        manuscript = fw.manuscript or ""
        domain_results: dict[str, str | None] = {}
        for domain in fw.domains:
            judgement = None
            for question in domain.questions:
                if question.question == "Risk-of-bias judgement" and question.response:
                    judgement = question.response.response
                    break
            domain_results[domain.name] = judgement
        summary[manuscript] = domain_results
    return summary


def print_summary(
    summary: Mapping[str, Mapping[str, str | None]],
    console: Console | None = None,
) -> None:
    """Display a summary table of risk-of-bias assessments.

    Parameters
    ----------
    summary : Mapping[str, Mapping[str, str | None]]
        Output from :func:`summarise_frameworks`.
    console : Console, optional
        Rich console used for output. If ``None``, a default console is created.

    Returns
    -------
    None
        ``None`` is returned after printing the table.
    """

    if console is None:
        console = Console()

    if not summary:
        console.print("No summaries to display.")
        return

    domain_names = list(next(iter(summary.values())).keys())
    table = Table(show_header=True, header_style="bold")
    table.add_column("Study")
    for i, _ in enumerate(domain_names, start=1):
        table.add_column(f"D{i}", justify="center")

    judgement_symbols = {
        "low": "+",
        "some concerns": "-",
        "high": "x",
    }

    for manuscript, domains in summary.items():
        row = [manuscript]
        for domain in domain_names:
            judgement = domains.get(domain)
            symbol = judgement_symbols.get(
                (judgement or "").lower(),
                "?",
            )
            row.append(symbol)
        table.add_row(*row)

    console.print(table)


def export_summary(
    summary: Mapping[str, Mapping[str, str | None]],
    path: Path | str,
) -> None:
    """Export risk-of-bias summary to a CSV file for analysis and visualization.

    This function saves the risk-of-bias assessment summary as a CSV (Comma-Separated
    Values) file, a widely-supported standard format that can be opened in spreadsheet
    applications like Excel, imported into statistical software like R or Python, or
    used with specialized risk-of-bias visualization tools.

    The exported CSV is specifically formatted to be compatible with RobVis, a popular
    R package and web application for creating publication-ready risk-of-bias
    visualizations. This ensures seamless interoperability between this tool and the
    broader risk-of-bias assessment ecosystem. The RobVis tool can generate traffic
    light plots and summary plots that are commonly used in systematic reviews and
    meta-analyses.

    The CSV structure includes:
    - A ``Study`` column containing manuscript/study identifiers
    - Domain columns (``D1``, ``D2``, ..., ``Dn``) for each risk-of-bias domain
    - An ``Overall`` column representing the highest (worst) risk rating across all
      domains

    Risk judgements are formatted according to RobVis conventions:
    - "Low" for low risk of bias
    - "Some concerns" for moderate risk of bias
    - "High" for high risk of bias

    Parameters
    ----------
    summary : Mapping[str, Mapping[str, str | None]]
        Output from :func:`summarise_frameworks` containing the risk-of-bias
        assessments.
    path : Path | str
        Destination file path for the CSV export. The file will be created or
        overwritten.

    Notes
    -----
    The exported CSV can be directly uploaded to the RobVis web interface at
    https://www.riskofbias.info/welcome/robvis-visualization-tool or used with
    the RobVis R package for programmatic visualization generation.
    """

    if not summary:
        Path(path).write_text("")
        return

    domain_names = list(next(iter(summary.values())).keys())
    path = Path(path)

    with path.open("w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ["Study"] + [f"D{i}" for i in range(1, len(domain_names) + 1)] + ["Overall"]
        )

        ranking = {"low": 0, "some concerns": 1, "high": 2}
        inverse_ranking = {0: "Low", 1: "Some concerns", 2: "High"}

        for manuscript, domains in summary.items():
            row: list[str | None] = [manuscript]
            worst = -1
            for domain in domain_names:
                judgement = domains.get(domain)
                # robvis requires a specific format
                if judgement is not None:
                    judgement_robvis = judgement.replace("Concerns", "concerns")
                else:
                    judgement_robvis = None
                row.append(judgement_robvis)
                if judgement:
                    score = ranking.get(judgement.lower(), -1)
                    if score > worst:
                        worst = score

            overall = inverse_ranking.get(worst, "")
            row.append(overall)
            writer.writerow(row)
