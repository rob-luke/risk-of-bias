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

    # Add manuscript name if available
    if framework.manuscript:
        lines.append(f"\n**Manuscript:** {framework.manuscript}")

    for domain in framework.domains:
        lines.append(f"\n## Domain {domain.index}: {domain.name}")

        if not domain.questions:
            lines.append("No questions defined.")
            continue

        for question in domain.questions:
            lines.append(f"\n### Question {question.question}\n")

            if question.response is None:
                lines.append("**Response:** Not answered")
                continue

            lines.append(f"Response: **{question.response.response}**\n")
            if question.response.reasoning:
                lines.append(f"Reasoning: {question.response.reasoning}\n")
            if question.response.evidence:
                lines.append("Evidence:")
                for evidence in question.response.evidence:
                    lines.append(f"- {evidence}")
            lines.append("")
            lines.append("")

    path.write_text("\n".join(lines))


def export_framework_as_html(framework: Framework, path: Path) -> None:
    """Export a completed framework as an HTML document.

    Parameters
    ----------
    framework : Framework
        The framework instance containing the assessment results.
    path : Path
        Destination file for the HTML representation.
    """
    from htpy import body
    from htpy import h1
    from htpy import h2
    from htpy import h3
    from htpy import html
    from htpy import li
    from htpy import p
    from htpy import strong
    from htpy import ul

    children = [h1[framework.name]]

    # Add manuscript name if available
    if framework.manuscript:
        children.append(p[strong["Manuscript: "], framework.manuscript])

    for domain in framework.domains:
        children.append(h2[f"Domain {domain.index}: {domain.name}"])

        if not domain.questions:
            children.append(p["No questions defined."])
            continue

        for question in domain.questions:
            children.append(h3[f"Question {question.question}"])

            if question.response is None:
                children.append(p[strong["Response:"], " Not answered"])
                continue

            children.append(
                p[
                    "Response: ",
                    strong[question.response.response],
                ]
            )
            if question.response.reasoning:
                children.append(p[f"Reasoning: {question.response.reasoning}"])
            if question.response.evidence:
                children.append(
                    ul[[li[evidence] for evidence in question.response.evidence]]
                )

    document = html[body[children]]
    path.write_text(document.__html__())
