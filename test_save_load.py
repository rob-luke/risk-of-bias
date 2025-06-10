#!/usr/bin/env python3
"""
Test script to verify framework save/load functionality works correctly.
"""

from pathlib import Path

from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.types._response_types import ReasonedResponseWithEvidenceAndRawData


def test_save_load():
    """Test that framework can be saved and loaded correctly."""

    # Create a framework with some mock responses
    framework = get_rob2_framework()

    # Add a mock response to the first question
    if framework.domains and framework.domains[0].questions:
        first_question = framework.domains[0].questions[0]
        first_question.response = ReasonedResponseWithEvidenceAndRawData(
            evidence=["Test evidence from manuscript"],
            reasoning="Test reasoning for the assessment",
            response="Yes",
        )

    # Save to a temp file
    temp_path = Path("/tmp/test_framework.json")
    framework.save(temp_path)
    print(f"Framework saved to {temp_path}")

    # Load it back
    loaded_framework = framework.load(temp_path)
    print("Framework loaded successfully!")

    # Verify the response was preserved
    if loaded_framework.domains and loaded_framework.domains[0].questions:
        loaded_response = loaded_framework.domains[0].questions[0].response
        if loaded_response:
            print(f"Loaded response: {loaded_response.response}")
            print(f"Loaded reasoning: {loaded_response.reasoning}")
            print(f"Loaded evidence: {loaded_response.evidence}")
            print(f"Raw data: {loaded_response.raw_data}")  # Should be None
        else:
            print("No response found")

    # Clean up
    temp_path.unlink()
    print("Test completed successfully!")


if __name__ == "__main__":
    test_save_load()
