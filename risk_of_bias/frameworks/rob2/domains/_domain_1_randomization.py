from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._question_types import Question


def _compute_judgement(domain: Domain) -> str | None:
    """Return the risk judgement for Domain 1 based on question responses."""
    q1 = domain.questions[0].response.response if domain.questions[0].response else None
    q2 = domain.questions[1].response.response if domain.questions[1].response else None
    q3 = domain.questions[2].response.response if domain.questions[2].response else None

    if None in (q1, q2, q3):
        return None

    if q1 in {"No", "Probably No"}:
        return "High"
    if q2 in {"No", "Probably No"}:
        return "High"
    if q3 in {"Yes", "Probably Yes"}:
        return "High"

    if q1 in {"Yes", "Probably Yes"} and q2 in {"Yes", "Probably Yes"}:
        return "Low"
    return "Some concerns"


q1_1 = Question(
    question="Question 1.1: Was the allocation sequence random?",
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
        "Not Applicable",
    ],
    index=1.1,
    is_required=True,
)

q1_2 = Question(
    question=(
        "Question 1.2: Was the allocation sequence concealed until participants were "
        "enrolled and assigned to interventions?"
    ),
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
        "Not Applicable",
    ],
    index=1.2,
    is_required=True,
)

q1_3 = Question(
    question=(
        "Question 1.3: Did baseline differences between intervention groups suggest "
        "a problem with the randomization process?"
    ),
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
        "Not Applicable",
    ],
    index=1.3,
    is_required=True,
)

q_o = Question(
    question=(
        "Optional Question: What is the predicted direction of bias arising from "
        "the randomization process?"
    ),
    allowed_answers=[
        "NA",
        "Favours experimental",
        "Favours comparator",
        "Towards null",
        "Away from null",
        "Unpredictable",
    ],
    index=1.5,
    is_required=False,
)

domain_1_randomization = Domain(
    questions=[q1_1, q1_2, q1_3, q_o],
    name="Bias arising from the randomization process.",
    index=1,
    judgement_function=_compute_judgement,
)
