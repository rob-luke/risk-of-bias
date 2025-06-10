from pydantic import BaseModel

from risk_of_bias.types._question_types import Question


class Domain(BaseModel):
    questions: list[Question] = []
    name: str = ""
    index: int = 0
