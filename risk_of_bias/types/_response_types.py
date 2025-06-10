from enum import Enum

from openai.types.responses.parsed_response import ParsedResponse
from pydantic import BaseModel


class Response(BaseModel):
    response: str


class ReasonedResponse(BaseModel):
    reasoning: str
    response: str


class ReasonedResponseWithEvidence(BaseModel):
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
