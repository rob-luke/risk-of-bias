from pathlib import Path

import matplotlib.figure

from risk_of_bias.compare import compare_frameworks
from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData
from risk_of_bias.visualisation import plot_assessor_agreement


def test_plot_assessor_agreement(tmp_path: Path) -> None:
    fw1 = get_rob2_framework()
    fw1.assessor = "Reviewer 1"
    fw1.domains[0].questions[0].response = ReasonedResponseWithEvidenceAndRawData(
        evidence=[], reasoning="", response="Yes"
    )
    fw1.domains[0].questions[1].response = ReasonedResponseWithEvidenceAndRawData(
        evidence=[], reasoning="", response="Yes"
    )

    fw2 = get_rob2_framework()
    fw2.assessor = "Reviewer 2"
    fw2.domains[0].questions[0].response = ReasonedResponseWithEvidenceAndRawData(
        evidence=[], reasoning="", response="No"
    )
    fw2.domains[0].questions[1].response = ReasonedResponseWithEvidenceAndRawData(
        evidence=[], reasoning="", response="Yes"
    )

    df = compare_frameworks(fw1, fw2)

    fig = plot_assessor_agreement(df)

    assert isinstance(fig, matplotlib.figure.Figure)
    assert len(fig.axes[0].collections) == len(df) * 2
    agreement_pct = df["agreement"].mean() * 100
    assert f"{agreement_pct:.0f}%" in fig.axes[0].texts[0].get_text()
