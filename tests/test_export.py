from pathlib import Path

from openai.types.responses.parsed_response import ParsedResponse

from risk_of_bias.export import export_framework_as_markdown
from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._framework_types import Framework
from risk_of_bias.types._question_types import Question
from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData


def test_export_framework_as_markdown(tmp_path: Path) -> None:
    framework = get_rob2_framework()
    export_path = tmp_path / "framework.md"
    export_framework_as_markdown(framework, export_path)

    assert export_path.exists()
    content = export_path.read_text()
    assert framework.name in content
    assert "Domain 1" in content


def test_export_framework_as_markdown_with_responses(tmp_path: Path) -> None:
    parsed: ParsedResponse = ParsedResponse.model_construct(
        id="1",
        created_at=0.0,
        model="",
        object="",
        output=[],
        parallel_tool_calls=None,
        tool_choice=None,
        tools=[],
        temperature=0.0,
        top_p=0.0,
    )
    question = Question(question="Did it work?", index=1.0)
    question.response = ReasonedResponseWithEvidenceAndRawData(
        response="Yes",
        reasoning="Because",
        evidence=["text"],
        raw_data=parsed,
    )
    domain = Domain(name="Test", index=1, questions=[question])
    framework = Framework(name="Test Framework", domains=[domain])

    export_path = tmp_path / "framework.md"
    export_framework_as_markdown(framework, export_path)

    content = export_path.read_text()
    assert "Response: **Yes**" in content
    assert "- text" in content
