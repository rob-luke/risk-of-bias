from typing import Callable, Optional

from pydantic import BaseModel, Field

from risk_of_bias.types._question_types import Question


class Domain(BaseModel):
    """
    A thematic grouping of related bias assessment questions within a framework.

    Domains represent the conceptual organization of bias assessment, where each
    domain focuses on a specific methodological aspect that could introduce bias
    into research findings. This organizational structure reflects how bias
    assessment experts think about and categorize different types of threats
    to study validity.

    Conceptual Foundation
    ---------------------
    The domain concept stems from decades of methodological research showing that
    bias in research studies tends to cluster around specific aspects of study
    design and conduct. Rather than having an unstructured list of questions,
    domains provide logical groupings that:

    - **Guide Systematic Thinking**: Help assessors consider all major categories
      of potential bias systematically
    - **Enable Targeted Assessment**: Allow focus on specific methodological
      concerns relevant to different study types
    - **Support Hierarchical Analysis**: Enable both domain-level and overall
      framework-level bias judgments
    - **Facilitate Communication**: Provide a shared vocabulary for discussing
      specific types of bias concerns

    Assessment Workflow
    -------------------
    During assessment, domains are typically evaluated sequentially, with each
    domain's questions answered before moving to the next. This approach:

    - Maintains focus on one type of bias at a time
    - Allows for domain-specific reasoning and evidence gathering
    - Enables partial assessments when time or information is limited
    - Supports quality control by domain-expert reviewers

    Attributes
    ----------
    questions : list[Question]
        The signaling questions that comprise this domain's assessment. Questions
        are typically ordered from fundamental to more detailed aspects of the
        bias type being evaluated.
    name : str
        A descriptive name for the domain that clearly indicates the type of bias
        being assessed (e.g., "Bias arising from the randomization process").
    index : int
        The sequential position of this domain within the overall framework.
        Used for organizing assessment workflow and reporting results in a
        consistent order.
    """

    questions: list[Question] = []
    name: str = ""
    index: int = 0
    judgement_function: Optional[Callable[["Domain"], str | None]] = Field(
        default=None, exclude=True
    )

    @property
    def judgement(self) -> str | None:
        """Return the risk-of-bias judgement for this domain."""
        if self.judgement_function is None:
            return None
        return self.judgement_function(self)
