from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._question_types import Question

q2_1 = Question(
    question=(
        "Question 2.1: Were participants aware of "
        "their assigned intervention during the trial?"
    ),
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
        "Not Applicable",
    ],
    index=2.1,
    is_required=True,
)

q2_2 = Question(
    question=(
        "Question 2.2: Were carers and people delivering the interventions "
        "aware of participants' assigned intervention during the trial?"
    ),
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
        "Not Applicable",
    ],
    index=2.2,
    is_required=True,
)

q2_3 = Question(
    question=(
        "Question 2.3: If Yes, Probably Yes or No Information to 2.1 or 2.2: "
        "Were there deviations from the intended intervention "
        "that arose because of the trial context?"
    ),
    allowed_answers=[
        "Not Applicable",
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=2.3,
    is_required=True,
)

q2_4 = Question(
    question=(
        "Question 2.4: If Yes or Probably Yes to 2.3: Were these deviations "
        "likely to have affected the outcome?"
    ),
    allowed_answers=[
        "Not Applicable",
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=2.4,
    is_required=True,
)

q2_5 = Question(
    question=(
        "Question 2.5: If Yes, Probably Yes or No Information to 2.4: "
        "Were these deviations from intended intervention balanced between groups?"
    ),
    allowed_answers=[
        "Not Applicable",
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=2.5,
    is_required=True,
)

q2_6 = Question(
    question=(
        "Question 2.6: Was an appropriate analysis used to estimate the effect "
        "of assignment to intervention?"
    ),
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
        "Not Applicable",
    ],
    index=2.6,
    is_required=True,
)

q2_7 = Question(
    question=(
        "Question 2.7: If No, Probably No or No Information to 2.6: "
        "Was there potential for a substantial impact on the result "
        "of the failure to analyse participants in "
        "the group to which they were randomized?"
    ),
    allowed_answers=[
        "Not Applicable",
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=2.7,
    is_required=True,
)

q2_o = Question(
    question=(
        "Optional Questions: What is the predicted direction of bias due to deviations "
        "from intended interventions?"
    ),
    allowed_answers=[
        "NA",
        "Favours experimental",
        "Favours comparator",
        "Towards null",
        "Away from null",
        "Unpredictable",
    ],
    index=2.9,
    is_required=False,
)


def _compute_judgement(domain: Domain) -> str | None:
    """
    Compute the risk of bias judgement for the Domain using the algorithm
    from the RoB 2.0 deviations domain flowchart.
    """

    # Answers for each question
    q1 = (
        domain.questions[0].response.response if domain.questions[0].response else None
    )  # 2.1
    q2 = (
        domain.questions[1].response.response if domain.questions[1].response else None
    )  # 2.2
    q3 = (
        domain.questions[2].response.response if domain.questions[2].response else None
    )  # 2.3
    q4 = (
        domain.questions[3].response.response if domain.questions[3].response else None
    )  # 2.4
    q5 = (
        domain.questions[4].response.response if domain.questions[4].response else None
    )  # 2.5
    q6 = (
        domain.questions[5].response.response if domain.questions[5].response else None
    )  # 2.6
    q7 = (
        domain.questions[6].response.response if domain.questions[6].response else None
    )  # 2.7

    YES = {"Yes", "Probably Yes"}
    NO = {"No", "Probably No"}
    NI = {"No Information"}

    # Part 1
    if q1 in NO and q2 in NO:
        part1 = "Low"
    else:
        if q3 in NO:
            part1 = "Low"
        elif q3 in NI:
            part1 = "Some concerns"
        else:  # q3 in YES
            if q4 in NO:
                part1 = "Some concerns"
            else:
                if q5 in YES:
                    part1 = "Some concerns"
                else:
                    part1 = "High"

    # Part 2
    if q6 in YES:
        part2 = "Low"
    else:
        if q7 in NO:
            part2 = "Some concerns"
        else:
            part2 = "High"

    if part1 == "Low" and part2 == "Low":
        return "Low"
    elif part1 == "High" or part2 == "High":
        return "High"
    else:
        return "Some concerns"


domain_2_deviations = Domain(
    questions=[q2_1, q2_2, q2_3, q2_4, q2_5, q2_6, q2_7, q2_o],
    name="Deviations from intended interventions",
    index=2,
    judgement_function=_compute_judgement,
)
