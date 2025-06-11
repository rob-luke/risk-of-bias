import functools
from pathlib import Path
from typing import Any, cast, Optional

from openai import OpenAI

from risk_of_bias.config import settings
from risk_of_bias.frameworks import get_rob2_framework
from risk_of_bias.oai._utils import create_openai_message
from risk_of_bias.oai._utils import pdf_to_base64
from risk_of_bias.prompts import SYSTEM_MESSAGE
from risk_of_bias.types._framework_types import Framework
from risk_of_bias.types._response_types import create_custom_constrained_response_class
from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData


def _union_types(a: type, b: type) -> object:
    """Return the union of two types."""
    return a | b


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
    4. **Systematic Questioning**: Sends all questions within a domain in a
       single request, reducing the number of API calls while maintaining
       conversation context
    5. **Evidence-Based Responses**: For each domain the AI returns a list of
       structured answers corresponding to each question. Each item includes:
       - The chosen response from predefined options
       - Detailed reasoning explaining the assessment
       - Specific evidence excerpts from the manuscript
    6. **Result Integration**: Stores all parsed responses back into the framework
       structure for easy access and analysis

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

    # Ask the AI model each domain's questions in a single request.
    for domain in framework.domains:
        if verbose:
            print(f"\n\nDomain {domain.index}: {domain.name}")

        response_classes = []
        for question in domain.questions:
            response_classes.append(
                create_custom_constrained_response_class(
                    domain.index, question.index, question.allowed_answers
                )
            )

        # Create a Union type for parsing a list of heterogeneous responses
        ResponseUnion = cast(
            type,
            functools.reduce(_union_types, response_classes),  # type: ignore[arg-type]
        )
        text_format = list[ResponseUnion]  # type: ignore[valid-type]

        questions_text = "\n".join(q.question for q in domain.questions)

        chat_input.append(create_openai_message("user", text=questions_text))

        raw_response = client.responses.parse(
            model=model,
            input=chat_input,
            text_format=text_format,
            temperature=0.1,
        )
        parsed_responses = raw_response.output_parsed or []

        chat_input.append(
            create_openai_message(
                "assistant", text=raw_response.output_text, content_type="output"
            )
        )

        for q, parsed in zip(domain.questions, parsed_responses):  # type: ignore[misc]
            if verbose:
                print(f"  Question {q.index}: {q.question} ({q.allowed_answers})")
                print(f"    Response: {parsed.response}")  # type: ignore[attr-defined]
                print(
                    f"      Reasoning: {parsed.reasoning}"  # type: ignore[attr-defined]
                )
                for evidence in parsed.evidence:  # type: ignore[attr-defined]
                    print(f"        Evidence: {evidence}")
                print("\n\n")

            q.response = ReasonedResponseWithEvidenceAndRawData(
                response=parsed.response,  # type: ignore[attr-defined]
                reasoning=parsed.reasoning,  # type: ignore[attr-defined]
                evidence=parsed.evidence,  # type: ignore[attr-defined]
                raw_data=raw_response,
            )  # type: ignore[arg-type]

    return framework
