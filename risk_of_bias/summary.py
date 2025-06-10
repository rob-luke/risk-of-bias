from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Mapping

from rich.console import Console
from rich.table import Table

from risk_of_bias.types._framework_types import Framework


def load_frameworks_from_directory(directory: Path | str) -> List[Framework]:
    """Load all JSON frameworks from ``directory``.

    Parameters
    ----------
    directory : Path | str
        Directory containing previously saved framework JSON files.

    Returns
    -------
    list[Framework]
        List of loaded frameworks. Files that cannot be parsed are ignored.
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
    """Create a summary representation of completed frameworks.

    Parameters
    ----------
    frameworks : list[Framework]
        Frameworks to summarise.

    Returns
    -------
    dict[str, dict[str, str | None]]
        Mapping of manuscript name to domain-level risk of bias judgements.
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
    """Export ``summary`` to ``path`` as a CSV table.

    The exported CSV follows the format required by tools such as RobVis,
    containing a ``Study`` column, one column for each domain (``D1`` ... ``Dn``)
    and an ``Overall`` column representing the highest risk rating across
    domains.

    Parameters
    ----------
    summary : Mapping[str, Mapping[str, str | None]]
        Output from :func:`summarise_frameworks`.
    path : Path | str
        Destination for the CSV file.
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
