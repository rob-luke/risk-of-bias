"""Utilities for comparing risk-of-bias assessments."""

from __future__ import annotations

import pandas as pd

from risk_of_bias.types._framework_types import Framework


def compare_frameworks(fw1: Framework, fw2: Framework) -> pd.DataFrame:
    """Compare two completed risk-of-bias frameworks.

    Parameters
    ----------
    fw1, fw2 : Framework
        Completed risk-of-bias frameworks to compare. The domain and question
        structure must be identical between the two frameworks.

    Returns
    -------
    pandas.DataFrame
        Long-form table with ``domain_short``, ``question_short``, ``domain``,
        ``question`` and one column per assessor containing their responses.
        If a question was unanswered, the value will be ``None``.
    """

    assessor1 = fw1.assessor or "assessor_1"
    assessor2 = fw2.assessor or "assessor_2"

    rows: list[dict[str, str | None]] = []
    if len(fw1.domains) != len(fw2.domains):
        raise ValueError("Frameworks have different numbers of domains")

    for d1, d2 in zip(fw1.domains, fw2.domains):
        if d1.name != d2.name:
            raise ValueError("Domain names do not match")
        if len(d1.questions) != len(d2.questions):
            raise ValueError(f"Domain {d1.name} has different numbers of questions")
        for q1, q2 in zip(d1.questions, d2.questions):
            if q1.question != q2.question:
                raise ValueError(
                    "Questions do not match in domain "
                    f"{d1.name}: {q1.question} vs {q2.question}"
                )
            a1 = q1.response.response if q1.response else None
            a2 = q2.response.response if q2.response else None
            rows.append(
                {
                    "domain_short": f"D{int(d1.index)}",
                    "question_short": f"Q{q1.index}",
                    "domain": d1.name,
                    "question": q1.question,
                    assessor1: a1,
                    assessor2: a2,
                }
            )

    return pd.DataFrame(rows)
