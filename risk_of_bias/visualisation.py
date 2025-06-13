"""Simple plotting utilities."""

from __future__ import annotations

import textwrap

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd


def plot_assessor_agreement(df: pd.DataFrame) -> Figure:
    """Visualise agreement between two assessors.

    Parameters
    ----------
    df : pandas.DataFrame
        Table returned by :func:`compare_frameworks`.

    Returns
    -------
    matplotlib.figure.Figure
        Figure with scatter points for each assessor.
    """

    required_cols = {
        "domain_short",
        "question_short",
        "domain",
        "question",
        "agreement",
    }
    if not required_cols.issubset(df.columns):
        raise ValueError("DataFrame does not appear to come from compare_frameworks")

    assessor_cols: list[str] = [c for c in df.columns if c not in required_cols]
    if len(assessor_cols) != 2:
        raise ValueError("DataFrame must contain results from exactly two assessors")

    assessor1, assessor2 = assessor_cols

    # Define the preferred order for categories
    preferred_order = [
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
        "Not Applicable",
        "High",
        "Some Concerns",
        "Low",
        "Favours experimental",
        "Favours comparator",
        "Towards null",
        "Away from null",
        "Unpredictable",
    ]

    all_responses: set[str | None] = set(df[assessor1]) | set(df[assessor2])
    # Order categories according to preferred order, then add any others found
    categories: list[str] = []
    for cat in preferred_order:
        if cat in all_responses:
            categories.append(cat)

    # Add any other categories not in the preferred order
    for response in all_responses:
        if response is not None and response not in categories:
            categories.append(response)

    # Add "Unanswered" for None values if present
    if None in all_responses:
        categories.append("Unanswered")

    cat_map: dict[str | None, int] = {c: i for i, c in enumerate(categories)}
    cat_map[None] = cat_map.get("Unanswered", len(categories))

    x_positions = range(len(df))
    fig, ax = plt.subplots(figsize=(12, 4))

    for i, (_, row) in enumerate(df.iterrows()):
        y1 = cat_map[row[assessor1]]
        y2 = cat_map[row[assessor2]]
        colour = "black" if row["agreement"] else "red"
        ax.scatter(i, y1, marker="x", color=colour)
        ax.scatter(i, y2, marker="o", facecolors="none", edgecolors=colour)

        # Add a red vertical line between points if they disagree
        if not row["agreement"]:
            ax.plot([i, i], [y1, y2], color="red", linewidth=1, alpha=0.7)

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(df["question_short"], rotation=45, ha="right")
    ax.set_xlim(-0.5, len(df) - 0.5)
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories)

    # Add domain names and horizontal lines
    domains_seen = set()
    for i, domain_short in enumerate(df["domain_short"]):
        if domain_short not in domains_seen:
            domains_seen.add(domain_short)

            # Get the full domain name for this domain_short
            domain_full = df[df["domain_short"] == domain_short]["domain"].iloc[0]

            # Find all questions in this domain
            domain_positions = [
                j for j, d in enumerate(df["domain_short"]) if d == domain_short
            ]
            start_pos = min(domain_positions)
            end_pos = max(domain_positions)
            center_pos = (start_pos + end_pos) / 2

            # Add horizontal line below the x-axis labels
            ax.plot(
                [start_pos - 0.4, end_pos + 0.4],
                [-0.2, -0.2],
                color="gray",
                linewidth=1,
                alpha=0.7,
                clip_on=False,
                transform=ax.get_xaxis_transform(),
            )

            # Add domain name below the x-axis labels (with text wrapping)
            # Calculate approximate character width based on domain span
            domain_span = end_pos - start_pos + 1
            max_chars_per_line = max(
                15, domain_span * 5
            )  # Minimum 15 chars, scale with domain width
            wrapped_text = textwrap.fill(domain_full, width=max_chars_per_line)

            ax.text(
                center_pos,
                -0.25,
                wrapped_text,
                ha="center",
                va="top",
                fontsize=7,
                color="gray",
                clip_on=False,
                transform=ax.get_xaxis_transform(),
            )

    agreement_pct = df["agreement"].mean() * 100
    ax.text(
        1.00 - 0.005,
        1.04,
        f"Agreement: {agreement_pct:.0f}%",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        bbox=dict(facecolor="white", alpha=0.8),
    )

    fig.tight_layout()
    return fig
