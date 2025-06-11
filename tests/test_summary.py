from pathlib import Path

from rich.console import Console

from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.summary import export_summary
from risk_of_bias.summary import load_frameworks_from_directory
from risk_of_bias.summary import print_summary
from risk_of_bias.summary import summarise_frameworks
from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData


def test_load_frameworks_from_directory(tmp_path: Path) -> None:
    framework = get_rob2_framework()
    framework.manuscript = "paper1.pdf"
    # add simple judgements
    for domain in framework.domains:
        for question in domain.questions:
            if question.question == "Risk-of-bias judgement":
                question.response = ReasonedResponseWithEvidenceAndRawData(
                    evidence=[], reasoning="", response="Low"
                )

    json_path = tmp_path / "paper1.json"
    framework.save(json_path)

    loaded = load_frameworks_from_directory(tmp_path)
    assert len(loaded) == 1
    assert loaded[0].manuscript == "paper1.pdf"


def test_summarise_frameworks(tmp_path: Path) -> None:
    framework = get_rob2_framework()
    framework.manuscript = "paper1.pdf"
    for domain in framework.domains:
        for question in domain.questions:
            if question.question == "Risk-of-bias judgement":
                question.response = ReasonedResponseWithEvidenceAndRawData(
                    evidence=[], reasoning="", response="High"
                )

    summary = summarise_frameworks([framework])
    assert "paper1.pdf" in summary
    assessments = summary["paper1.pdf"]
    assert len(assessments) == len(framework.domains)
    for domain in framework.domains:
        assert assessments[domain.name] == "High"


def test_print_summary_outputs_table() -> None:
    framework = get_rob2_framework()
    framework.manuscript = "study1.pdf"
    for domain in framework.domains:
        for question in domain.questions:
            if question.question == "Risk-of-bias judgement":
                question.response = ReasonedResponseWithEvidenceAndRawData(
                    evidence=[], reasoning="", response="Low"
                )

    summary = summarise_frameworks([framework])
    console = Console(width=80, record=True)
    print_summary(summary, console=console)
    output = console.export_text()
    assert "study1.pdf" in output
    assert "D1" in output
    assert "+" in output


def test_export_summary_creates_csv(tmp_path: Path) -> None:
    framework = get_rob2_framework()
    framework.manuscript = "studyA.pdf"
    for domain in framework.domains:
        for question in domain.questions:
            if question.question == "Risk-of-bias judgement":
                question.response = ReasonedResponseWithEvidenceAndRawData(
                    evidence=[], reasoning="", response="Low"
                )

    summary = summarise_frameworks([framework])
    export_path = tmp_path / "summary.csv"
    export_summary(summary, export_path)

    content = export_path.read_text().splitlines()
    assert content[0].startswith("Study,D1")
    assert "studyA.pdf" in content[1]


def test_export_summary_uses_overall_domain(tmp_path: Path) -> None:
    framework = get_rob2_framework()
    framework.manuscript = "studyB.pdf"
    for domain in framework.domains:
        for question in domain.questions:
            if question.question == "Risk-of-bias judgement":
                if domain.name == "Overall":
                    response = "High"
                else:
                    response = "Low"
                question.response = ReasonedResponseWithEvidenceAndRawData(
                    evidence=[], reasoning="", response=response
                )

    summary = summarise_frameworks([framework])
    export_path = tmp_path / "summary.csv"
    export_summary(summary, export_path)

    rows = [line.split(",") for line in export_path.read_text().splitlines()]
    header = rows[0]
    data = rows[1]
    assert header[-1] == "Overall"
    assert data[-1] == "High"
