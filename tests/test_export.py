from pathlib import Path

from openai.types.responses.parsed_response import ParsedResponse

from risk_of_bias.export import export_framework_as_html
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


def test_export_framework_as_html(tmp_path: Path) -> None:
    framework = get_rob2_framework()
    export_path = tmp_path / "framework.html"
    export_framework_as_html(framework, export_path)

    assert export_path.exists()
    content = export_path.read_text()
    assert framework.name in content
    assert "Domain 1" in content


def test_export_framework_as_html_with_responses(tmp_path: Path) -> None:
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

    export_path = tmp_path / "framework.html"
    export_framework_as_html(framework, export_path)

    content = export_path.read_text()
    assert "<strong>Yes</strong>" in content
    assert "<li>text</li>" in content


def test_export_markdown_includes_manuscript_name(tmp_path: Path) -> None:
    """Test that Markdown export includes manuscript name when set."""
    framework = get_rob2_framework()
    framework.manuscript = "test_study.pdf"

    export_path = tmp_path / "framework_with_manuscript.md"
    export_framework_as_markdown(framework, export_path)

    assert export_path.exists()
    content = export_path.read_text()
    assert f"# {framework.name}" in content
    assert "**Manuscript:** test_study.pdf" in content
    assert "Domain 1" in content

    # Verify manuscript appears between title and first domain
    lines = content.split("\n")
    title_line = next(
        i for i, line in enumerate(lines) if line.startswith(f"# {framework.name}")
    )
    manuscript_line = next(
        i for i, line in enumerate(lines) if "**Manuscript:**" in line
    )
    domain_line = next(i for i, line in enumerate(lines) if "## Domain 1" in line)

    assert title_line < manuscript_line < domain_line


def test_export_markdown_without_manuscript_name(tmp_path: Path) -> None:
    """Test that Markdown export works normally when manuscript name is not set."""
    framework = get_rob2_framework()
    framework.manuscript = None

    export_path = tmp_path / "framework_no_manuscript.md"
    export_framework_as_markdown(framework, export_path)

    assert export_path.exists()
    content = export_path.read_text()
    assert f"# {framework.name}" in content
    assert "**Manuscript:**" not in content
    assert "Domain 1" in content


def test_export_html_includes_manuscript_name(tmp_path: Path) -> None:
    """Test that HTML export includes manuscript name when set."""
    framework = get_rob2_framework()
    framework.manuscript = "research_paper.pdf"

    export_path = tmp_path / "framework_with_manuscript.html"
    export_framework_as_html(framework, export_path)

    assert export_path.exists()
    content = export_path.read_text()
    assert f"<h1>{framework.name}</h1>" in content
    assert "<strong>Manuscript: </strong>research_paper.pdf" in content
    assert "<h2>Domain 1" in content


def test_export_html_without_manuscript_name(tmp_path: Path) -> None:
    """Test that HTML export works normally when manuscript name is not set."""
    framework = get_rob2_framework()
    framework.manuscript = None

    export_path = tmp_path / "framework_no_manuscript.html"
    export_framework_as_html(framework, export_path)

    assert export_path.exists()
    content = export_path.read_text()
    assert f"<h1>{framework.name}</h1>" in content
    assert "Manuscript:" not in content
    assert "<h2>Domain 1" in content


def test_end_to_end_framework_with_manuscript_exports(tmp_path: Path) -> None:
    """Test complete workflow from framework creation to export with manuscript name."""
    framework = get_rob2_framework()
    framework.manuscript = "end_to_end_test.pdf"

    # Test both export formats
    md_path = tmp_path / "complete_test.md"
    html_path = tmp_path / "complete_test.html"

    framework.export_to_markdown(md_path)
    framework.export_to_html(html_path)

    # Verify both files exist and contain manuscript name
    assert md_path.exists()
    assert html_path.exists()

    md_content = md_path.read_text()
    html_content = html_path.read_text()

    assert "**Manuscript:** end_to_end_test.pdf" in md_content
    assert "<strong>Manuscript: </strong>end_to_end_test.pdf" in html_content
