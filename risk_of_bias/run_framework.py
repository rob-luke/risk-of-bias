from pathlib import Path
from typing import Any, Optional

from openai import OpenAI

from risk_of_bias.config import settings
from risk_of_bias.frameworks import get_rob2_framework
from risk_of_bias.oai._utils import create_openai_message
from risk_of_bias.oai._utils import pdf_to_base64
from risk_of_bias.prompts import SYSTEM_MESSAGE
from risk_of_bias.types._framework_types import Framework
from risk_of_bias.types._response_types import create_domain_response_class
from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData


def run_framework(
    manuscript: Path,
    framework: Framework = get_rob2_framework(),
    model: str = settings.fast_ai_model,
    guidance_document: Optional[Path] = None,
    verbose: bool = False,
    temperature: float = settings.temperature,
    api_key: Optional[str] = None,
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
    3. **Guidance Integration**: If provided, incorporates domain-specific guidance
       document to calibrate AI responses and provide specialized assessment criteria
    4. **Document Processing**: Converts the manuscript PDF to a format the AI can
       analyze
    5. **Systematic Questioning**: Sends all questions within a domain in a
       single request, reducing the number of API calls while maintaining
       conversation context
    6. **Evidence-Based Responses**: For each domain the AI returns a list of
       structured answers corresponding to each question. Each item includes:
       - The chosen response from predefined options
       - Detailed reasoning explaining the assessment
       - Specific evidence excerpts from the manuscript
    7. **Result Integration**: Stores all parsed responses back into the framework
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
        Optional path to a PDF guidance document that provides domain-specific
        assessment criteria and AI calibration instructions. This feature enables:

        - **Domain-specific expertise**: Specialized interpretation criteria for
          fields like pediatric studies, surgical interventions, or rare diseases
        - **AI bias correction**: Systematic adjustments when the AI consistently
          misinterprets methodological aspects or shows patterns of being overly
          lenient or conservative in specific assessment domains
        - **Standardization**: Consistent application of journal-specific guidelines
          or institutional assessment standards across multiple manuscripts
        - **Contextual clarification**: Detailed explanations for ambiguous scenarios
          that frequently arise in specialized research contexts

        The guidance document is presented to the AI before manuscript analysis,
        ensuring that your specified criteria and calibrations are consistently
        applied throughout the entire assessment process.
    verbose : bool, default=False
        Whether to print detailed progress information during assessment. When True,
        displays each question, response, reasoning, and evidence in real-time.
        Useful for debugging, monitoring progress, or understanding the assessment
        process in detail.
    temperature : float, default=settings.temperature
        Sampling temperature passed to the OpenAI model. Higher values yield more
        diverse answers while lower values make outputs more deterministic. If a
        negative value is provided, the temperature parameter is omitted and the
        server default is used.
    api_key : Optional[str], default=None
        API key to use for OpenAI calls. If ``None``, ``OPENAI_API_KEY`` from the
        environment will be used.

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
        and analysis of results. This complete data structure can be serialized
        to JSON format for persistence, caching, and data sharing workflows.
    """

    client = OpenAI(api_key=api_key)

    # Send system message to set context for the AI model
    chat_input: list[Any] = [create_openai_message("system", text=SYSTEM_MESSAGE)]

    # Set the manuscript filename and model name on the framework
    framework.manuscript = manuscript.name
    framework.assessor = model

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

        # Create a single response class for all questions in the domain
        domain_response_class = create_domain_response_class(domain)

        questions_text = "\n".join(q.question for q in domain.questions)

        chat_input.append(create_openai_message("user", text=questions_text))

        parse_kwargs: dict[str, Any] = {
            "model": model,
            "input": chat_input,
            "text_format": domain_response_class,
        }
        if temperature >= 0:
            parse_kwargs["temperature"] = temperature

        raw_response = client.responses.parse(**parse_kwargs)
        parsed_response = raw_response.output_parsed

        chat_input.append(
            create_openai_message(
                "assistant", text=raw_response.output_text, content_type="output"
            )
        )

        # Process each question response from the domain response
        if parsed_response:
            for question in domain.questions:
                field_name = (
                    f"question_{int(question.index * 10)}"  # 1.1 -> 11, 1.2 -> 12
                )

                if hasattr(parsed_response, field_name):
                    parsed = getattr(parsed_response, field_name)

                    if verbose:
                        print(
                            f"  Question {question.index}: {question.question} "
                            f"({question.allowed_answers})"
                        )
                        print(f"    Response: {parsed.response}")
                        print(f"      Reasoning: {parsed.reasoning}")
                        print(f"        Evidence: {parsed.evidence}")
                        print("\n\n")

                    question.response = ReasonedResponseWithEvidenceAndRawData(
                        response=parsed.response,
                        reasoning=parsed.reasoning,
                        evidence=[parsed.evidence],  # Convert string to list
                        raw_data=raw_response,
                    )

    return framework
