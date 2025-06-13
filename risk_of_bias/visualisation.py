"""Simple plotting utilities."""

from __future__ import annotations

from typing import Sequence

import matplotlib.pyplot as plt
import pandas as pd


def plot_assessor_agreement(df: pd.DataFrame) -> plt.Figure:
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

    all_responses: set[str | None] = set(df[assessor1]) | set(df[assessor2])
    categories: Sequence[str | None] = [r for r in all_responses if r is not None]
    if None in all_responses:
        categories = list(categories) + ["Unanswered"]

    cat_map = {c: i for i, c in enumerate(categories)}
    cat_map[None] = cat_map.get("Unanswered", len(categories))

    x_positions = range(len(df))
    fig, ax = plt.subplots(figsize=(8, 4))

    for i, row in df.iterrows():
        y1 = cat_map[row[assessor1]]
        y2 = cat_map[row[assessor2]]
        colour = "black" if row["agreement"] else "red"
        ax.scatter(i, y1, marker="x", color=colour)
        ax.scatter(i, y2, marker="o", facecolors="none", edgecolors=colour)

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(df["question_short"], rotation=45, ha="right")
    ax.set_xlim(-0.5, len(df) - 0.5)
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories)

    agreement_pct = df["agreement"].mean() * 100
    ax.text(
        0.99,
        0.01,
        f"Agreement: {agreement_pct:.0f}%",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    ax.set_title("Assessor Agreement")
    ax.set_xlabel("Question")
    ax.set_ylabel("Response")

    fig.tight_layout()
    return fig
