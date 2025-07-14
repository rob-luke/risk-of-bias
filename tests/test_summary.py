from pathlib import Path

from rich.console import Console

from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.summary import (
    export_summary,
    load_frameworks_from_directory,
    print_summary,
    summarise_frameworks,
)
from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._framework_types import Framework
from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData


def test_load_frameworks_from_directory(tmp_path: Path) -> None:
    framework = get_rob2_framework()
    framework.manuscript = "paper1.pdf"
    for domain in framework.domains:
        domain.judgement_function = lambda _d: "Low"

    json_path = tmp_path / "paper1.json"
    framework.save(json_path)

    loaded = load_frameworks_from_directory(tmp_path)
    assert len(loaded) == 1
    assert loaded[0].manuscript == "paper1.pdf"


def test_summarise_frameworks(tmp_path: Path) -> None:
    framework = get_rob2_framework()
    framework.manuscript = "paper1.pdf"
    for domain in framework.domains:
        domain.judgement_function = lambda _d: "High"

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
        domain.judgement_function = lambda _d: "Low"

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
        domain.judgement_function = lambda _d: "Low"

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
        if domain.name == "Overall":
            domain.judgement_function = lambda _d: "High"
        else:
            domain.judgement_function = lambda _d: "Low"

    summary = summarise_frameworks([framework])
    export_path = tmp_path / "summary.csv"
    export_summary(summary, export_path)

    rows = [line.split(",") for line in export_path.read_text().splitlines()]
    header = rows[0]
    data = rows[1]
    assert header[-1] == "Overall"
    assert data[-1] == "High"


def test_export_summary_uses_framework_judgement(tmp_path: Path) -> None:
    domain1 = Domain(index=1, name="D1", judgement_function=lambda d: "Low")
    domain2 = Domain(index=2, name="D2", judgement_function=lambda d: "High")
    framework = Framework(name="T", domains=[domain1, domain2])
    framework.manuscript = "studyC.pdf"

    summary = summarise_frameworks([framework])
    export_path = tmp_path / "summary.csv"
    export_summary(summary, export_path)

    rows = [line.split(",") for line in export_path.read_text().splitlines()]
    header = rows[0]
    data = rows[1]
    assert header[-1] == "Overall"
    assert data[-1] == "High"


def test_summarise_multiple_frameworks_independent_results(tmp_path: Path) -> None:
    """Test that multiple frameworks maintain independent results."""
    # Create first framework with specific judgements
    framework1 = get_rob2_framework()
    framework1.manuscript = "study1.pdf"
    judgements1 = ["Low", "High", "Some Concerns", "Low", "High", "Low"]

    for i, domain in enumerate(framework1.domains):
        domain.judgement_function = lambda _d, j=judgements1[i]: j  # type: ignore[misc]

    # Create second framework with different judgements
    framework2 = get_rob2_framework()
    framework2.manuscript = "study2.pdf"
    judgements2 = ["High", "Low", "Low", "Some Concerns", "Low", "High"]

    for i, domain in enumerate(framework2.domains):
        domain.judgement_function = lambda _d, j=judgements2[i]: j  # type: ignore[misc]

    # Summarise both frameworks
    summary = summarise_frameworks([framework1, framework2])

    # Verify both studies are in summary
    assert "study1.pdf" in summary
    assert "study2.pdf" in summary

    # Verify each study has correct results
    study1_results = list(summary["study1.pdf"].values())
    study2_results = list(summary["study2.pdf"].values())

    assert study1_results == judgements1
    assert study2_results == judgements2

    # Ensure they are different (regression test for the bug)
    assert study1_results != study2_results
