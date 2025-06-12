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

    # Ask for assessor name
    assessor_name = console.input("Enter assessor name (human): ")
    framework.assessor = assessor_name if assessor_name.strip() else "human"

    for domain in framework.domains:
        console.rule(f"Domain {domain.index}: {domain.name}")
        for question in domain.questions:
            console.print(
                f"[bold]Question {question.index}:[/bold] {question.question}"
            )
            response_text: Optional[str] = None
            while response_text is None:
                if question.allowed_answers:
                    # Multiple choice question - user must select from options
                    table = Table(show_header=False)
                    for i, option in enumerate(question.allowed_answers, start=1):
                        table.add_row(str(i), option)
                    console.print(table)

                    question_text = "Select option (number) "
                    if not question.is_required:
                        question_text += "[optional, press enter to skip]"
                    question_text += ": "

                    user_input = console.input(question_text)
                    if user_input == "" and not question.is_required:
                        break
                    if user_input.isdigit() and 1 <= int(user_input) <= len(
                        question.allowed_answers
                    ):
                        response_text = question.allowed_answers[int(user_input) - 1]
                    elif user_input in question.allowed_answers:
                        response_text = user_input
                    else:
                        console.print("Invalid response. Please select a valid option.")
                else:
                    # Free text question - user can enter any string
                    question_text = "Response "
                    if not question.is_required:
                        question_text += "[optional, press enter to skip]"
                    question_text += ": "

                    user_input = console.input(question_text)
                    if user_input == "" and not question.is_required:
                        break
                    elif user_input == "" and question.is_required:
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
