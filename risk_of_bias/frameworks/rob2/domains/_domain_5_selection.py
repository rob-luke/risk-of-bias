from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._question_types import Question

q5_1 = Question(
    question=(
        "Question 5.1: Were the data that produced this "
        "result analysed in accordance with a "
        "pre-specified analysis plan that was finalized "
        "before unblinded outcome data were available?"
    ),
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=5.1,
    is_required=True,
)

q5_2 = Question(
    question=(
        "Question 5.2: Is the numerical result being "
        "assessed likely to have been selected, "
        "on the basis of the results, from multiple eligible outcome measurements "
        "(e.g. scales, definitions, time points) within the outcome domain?"
    ),
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=5.2,
    is_required=True,
)

q5_3 = Question(
    question=(
        "Question 5.3: Is the numerical result "
        "being assessed likely to have been selected, "
        "on the basis of the results, from multiple eligible analyses of the data?"
    ),
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=5.3,
    is_required=True,
)

q5_o = Question(
    question=(
        "Optional Questions: What is the predicted direction of bias due to selection "
        "of the reported result?"
    ),
    allowed_answers=[
        "NA",
        "Favours experimental",
        "Favours comparator",
        "Towards null",
        "Away from null",
        "Unpredictable",
    ],
    index=5.5,
    is_required=False,
)


def _compute_judgement(domain: Domain) -> str | None:
    """
    Risk-of-bias algorithm for Domain 5 – selection of the reported result.
    Diagram logic:

        • If either Q5.2 or Q5.3 = Y/PY  → High risk
        • If neither Y/PY but ≥1 NI      → Some concerns
        • If both Q5.2 & Q5.3 = N/PN:
              – Q5.1 = Y/PY              → Low risk
              – Q5.1 = N/PN/NI           → Some concerns
    """
    q1 = (
        domain.questions[0].response.response if domain.questions[0].response else None
    )  # 5.1
    q2 = (
        domain.questions[1].response.response if domain.questions[1].response else None
    )  # 5.2
    q3 = (
        domain.questions[2].response.response if domain.questions[2].response else None
    )  # 5.3

    if None in (q1, q2, q3):
        return None  # incomplete

    YES = {"Yes", "Probably Yes"}
    NO = {"No", "Probably No"}
    NI = {"No Information"}

    # 1. Either Q5.2 or Q5.3 signals multiplicity ⇒ High risk
    if q2 in YES or q3 in YES:
        return "High risk"

    # 2. No Y/PY but at least one NI ⇒ Some concerns
    if q2 in NI or q3 in NI:
        return "Some concerns"

    # 3. Both Q5.2 & Q5.3 are N/PN ⇒ assess Q5.1
    if q2 in NO and q3 in NO:
        if q1 in YES:
            return "Low risk"
        elif q1 in NO or q1 in NI:
            return "Some concerns"

    return None  # should not be reached if all answers valid


domain_5_selection = Domain(
    questions=[q5_1, q5_2, q5_3, q5_o],
    name="Selection of the reported result",
    index=5,
    judgement_function=_compute_judgement,
)
