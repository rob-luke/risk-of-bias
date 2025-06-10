from pathlib import Path

from risk_of_bias.types._framework_types import Framework


def export_framework_as_markdown(framework: Framework, path: Path) -> None:
    """Export a completed framework as a Markdown document.

    Parameters
    ----------
    framework : Framework
        The framework instance containing the assessment results.
    path : Path
        Destination file for the Markdown representation.

    Notes
    -----
    Only Markdown format is currently supported. Additional formats may be
    added in future releases.
    """
    lines: list[str] = [f"# {framework.name}"]

    for domain in framework.domains:
        lines.append(f"\n## Domain {domain.index}: {domain.name}")

        if not domain.questions:
            lines.append("No questions defined.")
            continue

        for question in domain.questions:
            lines.append(f"\n### Question {question.index}")
            lines.append(question.question)

            if question.allowed_answers is not None:
                answers = ", ".join(question.allowed_answers)
            else:
                answers = "Any text"
            lines.append(f"*Allowed answers:* {answers}")

            if question.response is None:
                lines.append("**Response:** Not answered")
                continue

            lines.append(f"**Response:** {question.response.response}")
            if question.response.reasoning:
                lines.append(f"**Reasoning:** {question.response.reasoning}")
            if question.response.evidence:
                lines.append("**Evidence:**")
                for evidence in question.response.evidence:
                    lines.append(f"- {evidence}")

    path.write_text("\n".join(lines))
