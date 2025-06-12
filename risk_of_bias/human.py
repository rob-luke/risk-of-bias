from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table

from risk_of_bias.frameworks import get_rob2_framework
from risk_of_bias.types._framework_types import Framework
from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData


def run_human_framework(
    manuscript: Path,
    framework: Framework = get_rob2_framework(),
    console: Optional[Console] = None,
) -> Framework:
    """Interactively complete a risk-of-bias framework.

    This function guides the user through each question in the framework using
    a Rich console. Users select or type responses and may provide optional
    reasoning and evidence. Required questions must be answered; optional
    questions can be skipped by pressing Enter. Reasoning and evidence prompts
    can also be skipped with Enter.

    Parameters
    ----------
    manuscript : Path
        Path to the manuscript being assessed. Only the file name is stored in
        the resulting framework.
    framework : Framework, default=get_rob2_framework()
        Framework to populate with user responses.
    console : Console, optional
        Console instance for input and output. A new one is created if ``None``.

    Returns
    -------
    Framework
        The provided framework populated with user responses.
    """

    if console is None:
        console = Console()

    framework.manuscript = manuscript.name

    for domain in framework.domains:
        console.rule(f"Domain {domain.index}: {domain.name}")
        for question in domain.questions:
            console.print(
                f"[bold]Question {question.index}:[/bold] {question.question}"
            )
            response_text: Optional[str] = None
            while response_text is None:
                if question.allowed_answers:
                    table = Table(show_header=False)
                    for i, option in enumerate(question.allowed_answers, start=1):
                        table.add_row(str(i), option)
                    console.print(table)
                    user_input = console.input("Select option (number or text): ")
                    if user_input == "" and not question.is_required:
                        break
                    if user_input.isdigit() and 1 <= int(user_input) <= len(
                        question.allowed_answers
                    ):
                        response_text = question.allowed_answers[int(user_input) - 1]
                    elif user_input in question.allowed_answers:
                        response_text = user_input
                    else:
                        console.print("Invalid response. Please try again.")
                else:
                    user_input = console.input("Response: ")
                    if user_input == "" and not question.is_required:
                        break
                    if user_input == "":
                        console.print("Response required.")
                    else:
                        response_text = user_input

            if response_text is None:
                continue

            reasoning = console.input("Reasoning (optional): ")
            evidence_input = console.input("Evidence (optional): ")
            evidence = [evidence_input] if evidence_input else []

            question.response = ReasonedResponseWithEvidenceAndRawData(
                response=response_text,
                reasoning=reasoning,
                evidence=evidence,
                raw_data=None,
            )

    return framework
