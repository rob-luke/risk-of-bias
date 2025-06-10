import risk_of_bias.frameworks.rob2.domains._domain_1_randomization as d1
from risk_of_bias.types._framework_types import Framework

rob2_framework = Framework(
    domains=[d1.domain_1_randomization],
    name="RoB2 Framework for Randomized Trials",
)
