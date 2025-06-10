from enum import Enum

from openai.types.responses.parsed_response import ParsedResponse
from pydantic import BaseModel


class Response(BaseModel):
    response: str


class ReasonedResponse(BaseModel):
    reasoning: str
    response: str


class ReasonedResponseWithEvidence(BaseModel):
    """
    A structured response container that captures comprehensive AI assessment data.
    
    This class represents the core output of the AI bias assessment process,
    combining three essential components that make automated assessment both
    reliable and transparent: the actual response, the reasoning behind it,
    and the supporting evidence from the manuscript.
    
    The Transparency Imperative
    ---------------------------
    Traditional bias assessment often involves subjective expert judgment that
    can be difficult to audit or reproduce. This structured response format
    addresses these limitations by making the assessment process transparent:
    
    - **Explicit Reasoning**: Every assessment includes detailed explanation
      of the logic and criteria used to reach the conclusion
    - **Evidence-Based**: All conclusions are anchored to specific text
      from the manuscript, enabling verification and quality control
    - **Reproducible**: The structured format allows for consistent review,
      comparison, and potential re-evaluation of assessments
    
    Multi-Modal Assessment Support
    ------------------------------
    The evidence component is designed to work with various types of
    supporting information:
    
    - **Direct Quotes**: Exact text excerpts from methodology sections
    - **Paraphrased Content**: Summarized information when direct quotes
      would be too lengthy or fragmented
    - **Multi-Source Evidence**: Citations from different parts of the
      manuscript that collectively support the assessment
    - **Contextual Information**: Background details that inform the
      interpretation of methodological choices
    
    Attributes
    ----------
    evidence : list[str]
        A collection of text excerpts from the manuscript that support
        the assessment conclusion. Each item should be a meaningful
        piece of evidence that directly relates to the question being
        assessed. Evidence items are typically:
        
        - Direct quotations from relevant manuscript sections
        - Specific methodological details described by the authors
        - Quantitative information (sample sizes, response rates, etc.)
        - Procedural descriptions that inform bias assessment
        
        Multiple evidence items allow for comprehensive support of
        complex assessments that may depend on information scattered
        throughout the manuscript.
        
    reasoning : str
        A detailed explanation of the assessment logic connecting the
        evidence to the conclusion. This should include:
        
        - Interpretation of the evidence in methodological context
        - Application of relevant bias assessment criteria
        - Consideration of alternative interpretations
        - Explanation of how the evidence leads to the specific response
        
        High-quality reasoning demonstrates methodological sophistication
        and provides the rationale needed for assessment validation.
        
    response : str
        The actual assessment answer, either selected from predefined
        options (for structured questions) or provided as free-form text
        (for open-ended questions). This represents the final conclusion
        of the assessment process based on the evidence and reasoning.
    """
    evidence: list[str]
    reasoning: str
    response: str


class ReasonedResponseWithEvidenceAndRawData(BaseModel):
    evidence: list[str]
    reasoning: str
    response: str
    raw_data: ParsedResponse


def create_custom_constrained_response_class(
    domain_index: int | float,
    question_index: int | float,
    allowed_answers: list[str] | None = None,
) -> type:
    """
    Create a constrained response class for a specific domain and question.

    Args:
        domain_index: The domain index for unique naming
        question_index: The question index for unique naming
        allowed_answers: Optional list of allowed answers. If provided,
                        creates an enum constraint.
                        If None, uses str type for the response.

    Returns:
        A dynamically created class that inherits from ReasonedResponseWithEvidence
        with the appropriate response type constraint.
    """
    class_name = f"ConstrainedResponse_D{int(domain_index)}_Q{int(question_index)}"

    if allowed_answers is not None:
        # Create enum members dynamically using functional API that MyPy can understand
        enum_members = [
            (answer.replace(" ", "_").replace("-", "_"), answer)
            for answer in allowed_answers
        ]
        AllowedResponses = Enum("AllowedResponses", enum_members)  # type: ignore[misc]

        return type(
            class_name,
            (ReasonedResponseWithEvidence,),
            {"__annotations__": {"response": AllowedResponses}},
        )
    else:
        return type(
            class_name,
            (ReasonedResponseWithEvidence,),
            {"__annotations__": {"response": str}},
        )
