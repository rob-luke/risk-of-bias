from pathlib import Path
from typing import Any, Optional

from openai import OpenAI

from risk_of_bias.oai._utils import create_openai_message
from risk_of_bias.oai._utils import pdf_to_base64
from risk_of_bias.prompts import SYSTEM_MESSAGE
from risk_of_bias.types._framework_types import Framework
from risk_of_bias.types._response_types import create_custom_constrained_response_class
from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData

client = OpenAI()


def run_framework(
    manuscript: Path,
    model: str,
    framework: Framework,
    guidance_document: Optional[Path] = None,
) -> Framework:
    """Run the selected framework on a manuscript.

    Parameters
    ----------
    manuscript
        Path to the manuscript file to analyse.
    model
        Name of the OpenAI model to use.
    framework
        Framework describing the risk of bias questions.
    guidance_document
        Optional path to a guidance document providing additional context.

    Returns
    -------
    Framework
        The populated framework with responses from the model.
    """

    file_as_base64_string = pdf_to_base64(manuscript)

    # guidance_document_as_base64_string = (
    #     pdf_to_base64(guidance_document) if guidance_document else ""
    # )

    chat_input: list[Any] = [
        create_openai_message("system", text=SYSTEM_MESSAGE),
        # create_message(
        #     "user",
        #     text="This document provides guidance on how to answer the "
        #          "risk of bias questions.",
        #     file_data=f"data:application/pdf;base64,"
        #               f"{guidance_document_as_base64_string}",
        #     filename="guidance_document.pdf",
        # ),
        create_openai_message(
            "user",
            text="This is the paper we will be analyzing for risk of bias.",
            file_data=f"data:application/pdf;base64,{file_as_base64_string}",
            filename=manuscript.name.split("/")[-1],
        ),
    ]

    for domain in framework.domains:
        print(f"\n\nDomain {domain.index}: {domain.name}")
        for question in domain.questions:
            print(
                f"  Question {question.index}: {question.question} "
                f"({question.allowed_answers})"
            )

            ConstrainedResponse = create_custom_constrained_response_class(
                domain.index, question.index, question.allowed_answers
            )

            chat_input.append(create_openai_message("user", text=question.question))

            raw_response = client.responses.parse(
                model=model,
                input=chat_input,
                text_format=ConstrainedResponse,
                temperature=0.1,
            )
            parsed_response = raw_response.output_parsed

            chat_input.append(
                create_openai_message(
                    "assistant", text=raw_response.output_text, content_type="output"
                )
            )

            if parsed_response is None:
                print("    No response received.")
            else:
                print(f"    Response: {parsed_response.response}")
                print(f"      Reasoning: {parsed_response.reasoning}")
                for evidence in parsed_response.evidence:
                    print(f"        Evidence: {evidence}")
                print("\n\n")

            question.response = ReasonedResponseWithEvidenceAndRawData(
                response=parsed_response.response if parsed_response else "",
                reasoning=parsed_response.reasoning if parsed_response else "",
                evidence=parsed_response.evidence if parsed_response else [],
                raw_data=raw_response,
            )

    return framework
