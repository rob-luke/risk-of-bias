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

domain_5_selection = Domain(
    questions=[q5_1, q5_2, q5_3, q5_o],
    name="Selection of the reported result",
    index=5,
)
