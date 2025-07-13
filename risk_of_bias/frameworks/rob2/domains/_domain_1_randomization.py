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

domain_1_randomization = Domain(
    questions=[q1_1, q1_2, q1_3, q_o],
    name="Bias arising from the randomization process.",
    index=1,
)
