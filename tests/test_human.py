from pathlib import Path

from rich.console import Console

from risk_of_bias.human import run_human_framework
from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._framework_types import Framework
from risk_of_bias.types._question_types import Question


def test_run_human_framework_records_responses(monkeypatch):
    domain = Domain(
        name="D1",
        index=1,
        questions=[
            Question(question="Did it work?", allowed_answers=["Yes", "No"], index=1.0)
        ],
    )
    framework = Framework(name="Test", domains=[domain])

    inputs = iter(["TestAssessor", "1", "Because", "Evidence"])
    console = Console()
    monkeypatch.setattr(console, "input", lambda *args, **kwargs: next(inputs))

    run_human_framework(Path("manuscript.pdf"), framework, console=console)

    assert framework.assessor == "TestAssessor"
    response = framework.domains[0].questions[0].response
    assert response is not None
    assert response.response == "Yes"
    assert response.reasoning == "Because"
    assert response.evidence == ["Evidence"]


def test_run_human_framework_skips_optional(monkeypatch):
    domain = Domain(
        name="D1",
        index=1,
        questions=[
            Question(
                question="Optional?",
                allowed_answers=["Yes", "No"],
                index=1.0,
                is_required=False,
            )
        ],
    )
    framework = Framework(name="Test", domains=[domain])

    inputs = iter(["TestAssessor", ""])
    console = Console()
    monkeypatch.setattr(console, "input", lambda *args, **kwargs: next(inputs))

    run_human_framework(Path("manuscript.pdf"), framework, console=console)

    assert framework.assessor == "TestAssessor"
    assert framework.domains[0].questions[0].response is None
