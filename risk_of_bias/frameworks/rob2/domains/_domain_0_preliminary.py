from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._question_types import Question

q0_1 = Question(
    question="What was the study design?",
    allowed_answers=[
        "Individually-randomized parallel-group trial",
        "Cluster-randomized parallel-group trial",
        "Individually randomized cross-over (or other matched) trial",
    ],
    index=0.1,
    is_required=True,
)

q0_2 = Question(
    question=(
        "For the purposes of this assessment, the Experimental "
        "interventions being compared is defined as?"
    ),
    allowed_answers=None,
    index=0.2,
    is_required=True,
)

q0_3 = Question(
    question=(
        "For the purposes of this assessment, the Comparator "
        "interventions being compared is defined as?"
    ),
    allowed_answers=None,
    index=0.3,
    is_required=True,
)

domain_0_preliminary = Domain(
    questions=[q0_1, q0_2, q0_3],
    name="Preliminary",
    index=0,
)
