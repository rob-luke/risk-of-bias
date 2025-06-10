from pathlib import Path

from risk_of_bias.config import settings
from risk_of_bias.frameworks.rob2._rob2 import rob2_framework
from risk_of_bias.run_framework import run_framework


def main():
    """
    Main function to run the risk of bias analysis.
    This function is used for testing purposes.
    """

    filename = Path("/Users/rluke/Desktop/risk of bias materials/halmos.pdf")
    guidance = Path(
        "/Users/rluke/Desktop/risk of bias materials/20190822_RoB_2.0_guidance_parallel_trial.pdf"
    )

    response = run_framework(
        manuscript=filename,
        model=settings.fast_ai_model,
        framework=rob2_framework,
        guidance_document=guidance,
    )
    print(response)
    return response


if __name__ == "__main__":
    main()
