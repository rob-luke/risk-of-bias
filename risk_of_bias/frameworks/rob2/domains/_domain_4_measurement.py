from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._question_types import Question

q4_1 = Question(
    question=("Question 4.1: Was the method of measuring the outcome inappropriate?"),
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=4.1,
    is_required=True,
)

q4_2 = Question(
    question=(
        "Question 4.2: Could measurement or ascertainment of the outcome "
        "have differed between intervention groups?"
    ),
    allowed_answers=[
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=4.2,
    is_required=True,
)

q4_3 = Question(
    question=(
        "Question 4.3: If No, Probably No or No Information to 4.1 and 4.2: "
        "Were outcome assessors aware of the intervention received by participants?"
    ),
    allowed_answers=[
        "Not Applicable",
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=4.3,
    is_required=True,
)

q4_4 = Question(
    question=(
        "Question 4.4: If Yes, Probably Yes or No Information to 4.3: "
        "Could assessment of the outcome have been influenced "
        "by knowledge of intervention received?"
    ),
    allowed_answers=[
        "Not Applicable",
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=4.4,
    is_required=True,
)

q4_5 = Question(
    question=(
        "Question 4.5: If Yes, Probably Yes or No Information to 4.4: "
        "Is it likely that assessment of the outcome was influenced "
        "by knowledge of intervention received?"
    ),
    allowed_answers=[
        "Not Applicable",
        "Yes",
        "Probably Yes",
        "Probably No",
        "No",
        "No Information",
    ],
    index=4.5,
    is_required=True,
)

q4_o = Question(
    question=(
        "Optional Questions: What is the predicted direction "
        "of bias in measurement of the outcome?"
    ),
    allowed_answers=[
        "NA",
        "Favours experimental",
        "Favours comparator",
        "Towards null",
        "Away from null",
        "Unpredictable",
    ],
    index=4.7,
    is_required=False,
)

domain_4_measurement = Domain(
    questions=[q4_1, q4_2, q4_3, q4_4, q4_5, q4_o],
    name="Measurement of the outcome",
    index=4,
)
