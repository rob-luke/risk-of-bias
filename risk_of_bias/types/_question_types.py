from pydantic import BaseModel

from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData


class Question(BaseModel):
    """
    An individual signaling question that guides bias assessment within a domain.

    Questions are the fundamental building blocks of systematic bias assessment,
    designed to probe specific methodological aspects that could introduce bias
    into research findings. Each question represents a focused inquiry that helps
    assessors systematically evaluate study quality and potential threats to validity.

    Question Types and Response Modes
    ---------------------------------
    Questions can be configured for different types of assessment needs:

    **Structured Assessment (default)**:
    When `allowed_answers` contains predefined options (like "Yes", "Probably Yes",
    "No", etc.), the AI must select from these specific choices. This approach:

    - Ensures consistency across assessments
    - Enables quantitative analysis and meta-analysis
    - Follows established assessment frameworks like RoB2
    - Facilitates automated processing and reporting

    **Free-Form Assessment**:
    When `allowed_answers = None`, the AI can provide any string response of
    arbitrary length. This mode is valuable for:

    - Exploratory questions requiring detailed explanations
    - Capturing nuanced methodological details
    - Gathering qualitative insights about study design
    - Custom assessment criteria not covered by standard frameworks
    - Collecting recommendations for study improvement

    Assessment Context and Evidence
    -------------------------------
    Regardless of response mode, each question generates comprehensive assessment
    data including:

    - **Response**: The selected answer (structured) or free-form text
    - **Reasoning**: Detailed explanation of the assessment logic
    - **Evidence**: Specific text excerpts from the manuscript supporting the conclusion

    This evidence-based approach ensures that assessments are transparent,
    auditable, and grounded in the actual study documentation.

    Attributes
    ----------
    question : str
        The text of the signaling question presented to the AI assessor.
        Should be clear, specific, and answerable based on typical manuscript
        content. Well-designed questions avoid ambiguity and focus on
        observable methodological features.
    allowed_answers : list[str] | None
        Defines the response mode for this question:

        - **List of strings**: Restricts responses to predefined options,
          ensuring standardized assessment (e.g., ["Yes", "No", "Unclear"])
        - **None**: Enables free-form text responses of any length,
          allowing detailed explanations and custom insights

        The default provides standard bias assessment options commonly
        used in systematic review methodologies.
    index : float, default=0.0
        The position of this question within its domain, determining assessment
        order. Float values allow for flexible question insertion (e.g., 1.5
        between questions 1 and 2) without renumbering entire sequences.
    is_required : bool, default=False
        Whether this question must be answered for a complete assessment.
        Required questions typically address fundamental methodological
        features essential for bias evaluation, while optional questions
        may provide additional insights or apply only to specific study types.
    response : ReasonedResponseWithEvidenceAndRawData | None, default=None
        The AI-generated assessment response, populated during framework
        execution. Contains the structured response, reasoning, supporting
        evidence, and raw model output data.
    """

    question: str
    allowed_answers: list[str] | None = [
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
        "Not Applicable",
    ]
    index: float = 0.0
    is_required: bool = False
    response: ReasonedResponseWithEvidenceAndRawData | None = None
