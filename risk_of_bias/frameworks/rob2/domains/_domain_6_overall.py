from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._question_types import Question

q6_r = Question(
    question="Risk-of-bias judgement",
    allowed_answers=["Low", "High", "Some Concerns"],
    index=6.1,
    is_required=True,
)

q6_o = Question(
    question="What is the overall predicted direction of bias for this outcome?",
    allowed_answers=[
        "NA",
        "Favours experimental",
        "Favours comparator",
        "Towards null",
        "Away from null",
        "Unpredictable",
    ],
    index=6.2,
    is_required=False,
)

overall_domain = Domain(
    questions=[q6_r, q6_o],
    name="Overall",
    index=6,
)
