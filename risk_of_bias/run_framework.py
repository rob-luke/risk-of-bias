from pathlib import Path
from typing import Any, Optional

from openai import OpenAI

from risk_of_bias.config import settings
from risk_of_bias.frameworks import get_rob2_framework
from risk_of_bias.oai._utils import create_openai_message
from risk_of_bias.oai._utils import pdf_to_base64
from risk_of_bias.prompts import SYSTEM_MESSAGE
from risk_of_bias.types._framework_types import Framework
from risk_of_bias.types._response_types import create_custom_constrained_response_class
from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData

client = OpenAI()


def run_framework(
    manuscript: Path,
    framework: Framework = get_rob2_framework(),
    model: str = settings.fast_ai_model,
    guidance_document: Optional[Path] = None,
    verbose: bool = False,
) -> Framework:
    """
    Perform systematic risk-of-bias assessment on a research manuscript using AI.

    This function automates the process of evaluating potential sources of bias in
    research studies by systematically working through a structured assessment
    framework.
    It combines established methodological frameworks (like RoB2) with AI
    capabilities to provide evidence-based bias assessments.

    The Assessment Process
    ----------------------
    The function implements a comprehensive workflow:

    1. **Framework Setup**: Uses a pre-defined assessment framework containing
       organized domains and signaling questions
    2. **Context Establishment**: Sends system instructions to guide the AI model's
       assessment approach
    3. **Document Processing**: Converts the manuscript PDF to a format the AI can
       analyze
    4. **Systematic Questioning**: Works through each question in the framework
       sequentially, maintaining conversation context for coherent assessment
    5. **Evidence-Based Responses**: For each question, the AI provides:
       - A structured response from predefined options
       - Detailed reasoning explaining the assessment
       - Specific evidence excerpts from the manuscript
    6. **Result Integration**: Stores all responses back into the framework structure
       for easy access and analysis

    Parameters
    ----------
    manuscript : Path
        Path to the research manuscript PDF file to analyze. The file must exist
        and be readable. Supported formats include standard academic PDFs.
    framework : Framework, default=get_rob2_framework()
        The assessment framework defining the structure of the bias evaluation.
        Defaults to the complete RoB2 framework for randomized controlled trials.
        Custom frameworks can be provided for specialized assessments.
    model : str, default=settings.fast_ai_model
        The OpenAI model identifier to use for assessment. Different models may
        provide varying levels of analysis depth and accuracy. The default is
        optimized for speed while maintaining quality.
    guidance_document : Optional[Path], default=None
        Optional path to a PDF guidance document that provides additional context
        or instructions for the assessment. This could include journal-specific
        criteria, detailed methodology explanations, or domain-specific guidance.
        If provided, the AI will consider this context when making assessments.
    verbose : bool, default=False
        Whether to print detailed progress information during assessment. When True,
        displays each question, response, reasoning, and evidence in real-time.
        Useful for debugging, monitoring progress, or understanding the assessment
        process in detail.

    Returns
    -------
    Framework
        The original framework structure populated with AI-generated responses.
        Each question in the framework will contain a
        ReasonedResponseWithEvidenceAndRawData object with:

        - **response**: The selected answer from the allowed options
        - **reasoning**: Detailed explanation of the assessment logic
        - **evidence**: List of relevant text excerpts from the manuscript
        - **raw_data**: Complete raw response data from the AI model

        The populated framework maintains the hierarchical structure
        (Framework → Domains → Questions → Responses) for easy navigation
        and analysis of results.
    """

    # Send system message to set context for the AI model
    chat_input: list[Any] = [create_openai_message("system", text=SYSTEM_MESSAGE)]

    # Set the manuscript filename on the framework
    framework.manuscript = manuscript.name

    # Send the framework guidance to the AI model
    if guidance_document is not None:
        if not guidance_document.exists() or not guidance_document.is_file():
            raise ValueError(
                f"Guidance document {guidance_document} must exist and be a file."
            )
        guidance_document_as_base64_string = pdf_to_base64(guidance_document)

        chat_input.append(
            create_openai_message(
                "user",
                text="This document provides guidance on how to answer the "
                "risk of bias questions.",
                file_data=f"data:application/pdf;base64,"
                f"{guidance_document_as_base64_string}",
                filename="guidance_document.pdf",
            )
        )

        chat_input.append(
            create_openai_message(
                "assistant",
                text="Thank you for sharing the guidance document, "
                "please share the manuscript for me to review.",
                content_type="output",
            )
        )

    # Send the manuscript to the AI model
    file_as_base64_string = pdf_to_base64(manuscript)
    chat_input.append(
        create_openai_message(
            "user",
            text="This is the paper we will be analyzing for risk of bias.",
            file_data=f"data:application/pdf;base64,{file_as_base64_string}",
            filename=manuscript.name.split("/")[-1],
        )
    )

    # Ask the AI model each question in turn, parsing the responses.
    for domain in framework.domains:
        if verbose:
            print(f"\n\nDomain {domain.index}: {domain.name}")

        for question in domain.questions:

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

            # Print the question and response for debugging
            if verbose:
                print(
                    f"  Question {question.index}: {question.question} "
                    f"({question.allowed_answers})"
                )
                if parsed_response is None:
                    print("    No response received.")
                else:
                    print(f"    Response: {parsed_response.response}")
                    print(f"      Reasoning: {parsed_response.reasoning}")
                    for evidence in parsed_response.evidence:
                        print(f"        Evidence: {evidence}")
                    print("\n\n")

            # Store the response in the question object
            question.response = ReasonedResponseWithEvidenceAndRawData(
                response=parsed_response.response if parsed_response else "",
                reasoning=parsed_response.reasoning if parsed_response else "",
                evidence=parsed_response.evidence if parsed_response else [],
                raw_data=raw_response,
            )

    return framework
