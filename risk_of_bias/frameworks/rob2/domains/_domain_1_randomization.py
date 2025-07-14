from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._question_types import Question

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


def _compute_judgement(domain: Domain) -> str | None:
    """
    Compute the risk of bias judgement for Domain 1 (Randomization Process).

    This function implements the ROB 2.0 algorithm for determining the overall
    risk of bias arising from the randomization process. The judgement is based
    on responses to three signalling questions about allocation sequence
    randomization, concealment, and baseline differences.

    Parameters
    ----------
    domain : Domain
        A Domain object containing the three required questions for randomization
        assessment:
        - questions[0]: Q1.1 - Was the allocation sequence random?
        - questions[1]: Q1.2 - Was the allocation sequence concealed?
        - questions[2]: Q1.3 - Did baseline differences suggest problems?

        Each question should have a response with one of the allowed answers:
        ["Yes", "Probably Yes", "Probably No", "No", "No Information", "Not Applicable"]

    Returns
    -------
    str or None
        The overall risk of bias judgement for this domain:
        - "High" : Serious concerns about randomization, concealment, or baseline
                   balance
        - "Low" : Minimal risk when both randomization and concealment are
                  adequate
        - "Some concerns" : Intermediate risk when criteria for Low/High are not met
        - None : Assessment incomplete due to missing responses

    Notes
    -----
    This function implements the ROB 2.0 guidance for Domain 1 as specified in:
    Sterne et al. (2019). RoB 2: a revised tool for assessing risk of bias in
    randomised trials. BMJ, 366, l4898.

    The assessment prioritizes identifying high-risk studies through a
    conservative approach where any major methodological flaw results in a
    "High" risk judgement. Only studies with clear evidence of both adequate
    randomization and concealment receive "Low" risk ratings.
    """
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


domain_1_randomization = Domain(
    questions=[q1_1, q1_2, q1_3, q_o],
    name="Bias arising from the randomization process.",
    index=1,
    judgement_function=_compute_judgement,
)
