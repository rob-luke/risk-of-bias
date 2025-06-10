import risk_of_bias.frameworks.rob2.domains._domain_1_randomization as d1
import risk_of_bias.frameworks.rob2.domains._domain_2_deviations as d2
import risk_of_bias.frameworks.rob2.domains._domain_3_missing as d3
import risk_of_bias.frameworks.rob2.domains._domain_4_measurement as d4
import risk_of_bias.frameworks.rob2.domains._domain_5_selection as d5
from risk_of_bias.types._framework_types import Framework

"""
RoB2 (Risk of Bias 2) Framework for Randomized Trials.

This module defines the complete RoB2 framework by combining all five assessment domains
for evaluating risk of bias in randomized controlled trials. The framework follows the
Cochrane Risk of Bias tool version 2.0 guidelines.

The framework includes the following domains:
- Domain 1: Bias arising from the randomization process
- Domain 2: Bias due to deviations from intended interventions
- Domain 3: Bias due to missing outcome data
- Domain 4: Bias in measurement of the outcome
- Domain 5: Bias in selection of the reported result

Each domain contains specific signaling questions and algorithms to determine
the overall risk of bias rating (Low, Some concerns, High).

Returns:
    Framework: A configured RoB2 framework instance containing all five domains
    with the name "RoB2 Framework for Randomized Trials".
"""
rob2_framework = Framework(
    domains=[
        d1.domain_1_randomization,
        d2.domain_2_deviations,
        d3.domain_3_missing,
        d4.domain_4_measurement,
        d5.domain_5_selection,
    ],
    name="RoB2 Framework for Randomized Trials",
)
