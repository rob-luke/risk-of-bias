from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._question_types import Question

q3_1 = Question(
    question=(
        "Question 3.1: Were data for this outcome available for all, or nearly all, "
        "participants randomized?"
    ),
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=3.1,
    is_required=True,
)

q3_2 = Question(
    question=(
        "Question 3.2: If No, Probably No or No Information to 3.1: "
        "Is there evidence that the result was not biased by missing outcome data?"
    ),
    allowed_answers=[
        "Not Applicable",
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
    ],
    index=3.2,
    is_required=True,
)

q3_3 = Question(
    question=(
        "Question 3.3: If No or Probably No to 3.2: "
        "Could missingness in the outcome depend on its true value?"
    ),
    allowed_answers=[
        "Not Applicable",
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=3.3,
    is_required=True,
)

q3_4 = Question(
    question=(
        "Question 3.4: If Yes, Probably Yes or No Information to 3.3: "
        "Is it likely that missingness in the outcome depended on its true value?"
    ),
    allowed_answers=[
        "Not Applicable",
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=3.4,
    is_required=True,
)

q3_o = Question(
    question=(
        "Optional Questions: What is the predicted direction of bias due to "
        "missing outcome data?"
    ),
    allowed_answers=[
        "NA",
        "Favours experimental",
        "Favours comparator",
        "Towards null",
        "Away from null",
        "Unpredictable",
    ],
    index=3.6,
    is_required=False,
)


def _compute_judgement(domain: Domain) -> str | None:
    """
    Compute the risk of bias judgement for the Domain.
    """
    q1 = (
        domain.questions[0].response.response if domain.questions[0].response else None
    )  # 3.1
    q2 = (
        domain.questions[1].response.response if domain.questions[1].response else None
    )  # 3.2
    q3 = (
        domain.questions[2].response.response if domain.questions[2].response else None
    )  # 3.3
    q4 = (
        domain.questions[3].response.response if domain.questions[3].response else None
    )  # 3.4

    # Return None if any required question is unanswered
    if None in (q1, q2, q3, q4):
        return None

    YES = {"Yes", "Probably Yes"}
    NO = {"No", "Probably No"}
    NI = {"No Information"}
    YPYNI = YES | NI  # "Yes", "Probably Yes", "No Information"

    # 3.1: Outcome data for all? (Y/PY) --> Low risk
    if q1 in YES:
        return "Low risk"

    # 3.1: Outcome data for all? (N/PN/NI) --> ask 3.2
    if q1 in NO or q1 in NI:
        # 3.2: Evidence result not biased? (Y/PY) --> Low risk
        if q2 in YES:
            return "Low risk"
        # 3.2: (N/PN) --> ask 3.3
        elif q2 in NO:
            # 3.3: Missingness could depend on
            # true value? (N/PN) --> Low risk
            if q3 in NO:
                return "Low risk"
            # 3.3: (Y/PY/NI) --> ask 3.4
            elif q3 in YPYNI:
                # 3.4: Likely that missingness depended on true value?
                if q4 in NO:
                    return "Some concerns"
                elif q4 in YPYNI:
                    return "High risk"
                else:
                    return None
            else:
                return None
        else:
            return None
    return None


domain_3_missing = Domain(
    questions=[q3_1, q3_2, q3_3, q3_4, q3_o],
    name="Missing outcome data",
    index=3,
    judgement_function=_compute_judgement,
)
