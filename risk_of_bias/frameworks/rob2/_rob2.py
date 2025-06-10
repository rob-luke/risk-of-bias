import risk_of_bias.frameworks.rob2.domains._domain_1_randomization as d1
import risk_of_bias.frameworks.rob2.domains._domain_2_deviations as d2
import risk_of_bias.frameworks.rob2.domains._domain_3_missing as d3
import risk_of_bias.frameworks.rob2.domains._domain_4_measurement as d4
import risk_of_bias.frameworks.rob2.domains._domain_5_selection as d5
from risk_of_bias.types._framework_types import Framework


def get_rob2_framework() -> Framework:
    """
    Get the complete RoB2 (Risk of Bias 2) Framework for Randomized Trials.

    This function returns a fully configured RoB2 framework that implements the
    Cochrane Risk of Bias tool version 2.0 guidelines for systematic evaluation
    of bias in randomized controlled trials.

    The RoB2 framework is the gold standard for assessing risk of bias in
    randomized trials and is widely used in systematic reviews and meta-analyses.
    It provides a structured approach to evaluate five key domains where bias
    commonly occurs in clinical research.

    Framework Structure
    -------------------
    The framework contains five assessment domains, each with specific signaling
    questions designed to systematically evaluate potential sources of bias:

    **Domain 1: Bias arising from the randomization process**
        Evaluates the adequacy of the randomization sequence generation and
        allocation concealment mechanisms.

    **Domain 2: Bias due to deviations from intended interventions**
        Assesses whether there were deviations from intended interventions
        and whether the analysis was appropriate.

    **Domain 3: Bias due to missing outcome data**
        Examines whether outcome data was available for all participants
        and whether missingness could depend on the true value.

    **Domain 4: Bias in measurement of the outcome**
        Evaluates whether the outcome measurement was appropriate and
        whether measurement differed between intervention groups.

    **Domain 5: Bias in selection of the reported result**
        Assesses whether the reported result was selected from multiple
        measurements or analyses of the data.

    Returns
    -------
    Framework
        A configured Framework instance containing all five RoB2 domains
        with their respective signaling questions and answer options.
        The framework is ready for immediate use with `run_framework()`.

    Examples
    --------
    >>> from risk_of_bias.frameworks.rob2 import get_rob2_framework
    >>> from risk_of_bias import run_framework
    >>> from pathlib import Path
    >>>
    >>> # Get the pre-configured framework
    >>> framework = get_rob2_framework()
    >>> print(f"Framework: {framework.name}")
    >>> print(f"Number of domains: {len(framework.domains)}")
    >>>
    >>> # Use with manuscript analysis
    >>> manuscript = Path("manuscript.pdf")
    >>> results = run_framework(manuscript=manuscript, framework=framework)

    Notes
    -----
    This framework follows the official RoB2 guidance and includes all
    standard signaling questions with the appropriate answer options:
    "Yes", "Probably Yes", "Probably No", "No", "No Information",
    "Not Applicable".

    The framework structure mirrors the official RoB2 tool to ensure
    consistency with established assessment practices in systematic
    review methodology.

    References
    ----------
    Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for
    assessing risk of bias in randomised trials. BMJ 2019; 366: l4898.
    """
    return Framework(
        domains=[
            d1.domain_1_randomization,
            d2.domain_2_deviations,
            d3.domain_3_missing,
            d4.domain_4_measurement,
            d5.domain_5_selection,
        ],
        name="RoB2 Framework for Randomized Trials",
    )
