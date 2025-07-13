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

domain_2_deviations = Domain(
    questions=[q2_1, q2_2, q2_3, q2_4, q2_5, q2_6, q2_7, q2_o],
    name="Deviations from intended interventions",
    index=2,
)
