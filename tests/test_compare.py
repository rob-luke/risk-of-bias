from risk_of_bias.compare import compare_frameworks
from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData


def test_compare_frameworks() -> None:
    fw1 = get_rob2_framework()
    fw1.assessor = "Reviewer 1"
    fw1.domains[0].questions[0].response = ReasonedResponseWithEvidenceAndRawData(
        evidence=[], reasoning="", response="Yes"
    )
    fw1.domains[0].questions[1].response = ReasonedResponseWithEvidenceAndRawData(
        evidence=[], reasoning="", response="Yes"
    )
    fw1.domains[1].questions[0].response = ReasonedResponseWithEvidenceAndRawData(
        evidence=[], reasoning="", response="No"
    )

    fw2 = get_rob2_framework()
    fw2.assessor = "Reviewer 2"
    fw2.domains[0].questions[0].response = ReasonedResponseWithEvidenceAndRawData(
        evidence=[], reasoning="", response="No"
    )
    fw2.domains[0].questions[1].response = ReasonedResponseWithEvidenceAndRawData(
        evidence=[], reasoning="", response="Yes"
    )
    fw2.domains[1].questions[0].response = ReasonedResponseWithEvidenceAndRawData(
        evidence=[], reasoning="", response="No"
    )

    df = compare_frameworks(fw1, fw2)

    assert list(df.columns[:4]) == [
        "domain_short",
        "question_short",
        "domain",
        "question",
    ]
    assert "Reviewer 1" in df.columns
    assert "Reviewer 2" in df.columns

    first_row = df.iloc[0]
    assert first_row["domain_short"] == "D1"
    assert first_row["question_short"] == "Q1.1"
    assert first_row["Reviewer 1"] == "Yes"
    assert first_row["Reviewer 2"] == "No"

    second_row = df[
        (df["domain"] == fw1.domains[0].name)
        & (df["question"] == fw1.domains[0].questions[1].question)
    ].iloc[0]
    assert second_row["domain_short"] == "D1"
    assert second_row["question_short"] == "Q1.2"
    assert second_row["Reviewer 1"] == "Yes"
    assert second_row["Reviewer 2"] == "Yes"

    third_row = df[
        (df["domain"] == fw1.domains[1].name)
        & (df["question"] == fw1.domains[1].questions[0].question)
    ].iloc[0]
    assert third_row["domain_short"] == "D2"
    assert third_row["question_short"] == "Q2.1"
    assert third_row["Reviewer 1"] == "No"
    assert third_row["Reviewer 2"] == "No"
    assert len(df) == sum(len(d.questions) for d in fw1.domains)
