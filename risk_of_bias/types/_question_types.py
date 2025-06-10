from pydantic import BaseModel

from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData


class Question(BaseModel):
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
