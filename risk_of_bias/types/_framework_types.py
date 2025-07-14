from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from risk_of_bias.types._domain_types import Domain


class Framework(BaseModel):
    """
    The top-level container for risk-of-bias assessment frameworks.

    A Framework represents a complete methodological assessment tool (e.g., RoB2)
    that systematically evaluates potential sources of bias in research studies.
    Frameworks organize the assessment process through a hierarchical structure:

    Framework → Domains → Questions → Responses

    The Framework serves as both a template (defining the assessment structure)
    and a container for results (storing responses after manuscript analysis).
    When a manuscript is analyzed, the AI model works through each question
    in sequence, populating the response fields with evidence-based assessments.

    Attributes
    ----------
    domains : list[Domain]
        The assessment domains that comprise this framework. Each domain
        focuses on a specific category of potential bias.
    name : str
        A descriptive name for the framework (e.g., "RoB2 Framework for
        Randomized Trials").
    manuscript : str, optional
        The filename (without path) of the manuscript being assessed.
    assessor : str | None
        The name or identifier of the person or system performing the assessment.
        This can be useful for tracking who completed the assessment, especially
        in collaborative environments.
    """

    domains: list[Domain] = []
    name: str = ""
    manuscript: Optional[str] = None
    assessor: Optional[str] = None

    @property
    def judgement(self) -> str | None:
        """Return the overall risk-of-bias judgement for this framework.

        The overall judgement is derived from the judgements of all domains
        except the ``Overall`` domain. If any domain judgement is ``None``
        the overall judgement is also ``None``.

        Returns
        -------
        str | None
            One of ``"Low"``, ``"Some concerns"`` or ``"High```, or ``None`` if
            any domain does not yet have a judgement.
        """

        ranking = {"low": 0, "some concerns": 1, "high": 2}
        worst = -1
        for domain in self.domains:
            if domain.name.lower() == "overall":
                continue
            judgement = domain.judgement
            if judgement is None:
                return None
            score = ranking.get(judgement.lower(), -1)
            if score > worst:
                worst = score

        if worst == -1:
            return None

        inverse = {0: "Low", 1: "Some concerns", 2: "High"}
        return inverse[worst]

    def __str__(self) -> str:
        """
        Provide a comprehensive human-readable representation of the Framework.

        This method creates a structured text representation that displays the complete
        assessment framework hierarchy, making it easy to review the framework structure
        and any completed assessments. The output format is designed for readability
        and debugging purposes.

        The string representation includes:
        - Framework name and overview
        - Each domain with its index and name
        - All questions within each domain with their indices and text
        - Allowed answer options for each question (if defined)
        - Response details for answered questions, including:
          - The selected response
          - The reasoning behind the assessment
          - Supporting evidence excerpts from the manuscript
        - Clear indication of unanswered questions

        Returns
        -------
        str
            A multi-line string representation of the framework showing:
            - Framework structure (domains and questions)
            - Assessment progress (which questions have been answered)
            - Complete response details for answered questions

        Examples
        --------
        >>> framework = Framework(name="RoB2 Framework")
        >>> print(framework)
        Framework: RoB2 Framework
        Domain 1: Randomization Process
          Question 1.1: Was the allocation sequence random? (['Yes', 'Probably Yes',
          ...])
            Response: Yes
              Reasoning: The study clearly describes using computer-generated
              randomization
                Evidence: "Participants were randomized using a computer-generated
                sequence"

        Notes
        -----
        This method is particularly useful for:

        - Reviewing framework structure during development
        - Debugging assessment workflows
        - Generating human-readable reports of completed assessments
        - Understanding the hierarchical organization of bias assessment questions
        """
        if not self.domains:
            return "Framework: No domains defined"

        lines = [f"Framework: {self.name}"]
        if self.manuscript:
            lines.append(f"Manuscript: {self.manuscript}")
        for domain in self.domains:
            lines.append(f"\nDomain {domain.index}: {domain.name}")

            if not domain.questions:
                lines.append("  No questions defined")
                continue

            for question in domain.questions:
                question_line = f"  Question {question.index}: {question.question}"
                if question.allowed_answers:
                    question_line += f" ({question.allowed_answers})"
                lines.append(question_line)

                if question.response:
                    lines.append(f"    Response: {question.response.response}")
                    if question.response.reasoning:
                        lines.append(f"      Reasoning: {question.response.reasoning}")
                    if question.response.evidence:
                        for evidence in question.response.evidence:
                            lines.append(f"        Evidence: {evidence}")
                else:
                    lines.append("    Response: Not answered")
                lines.append("")

        return "\n".join(lines)

    def export_to_markdown(self, path: Path) -> None:
        """Export the framework as a Markdown document.

        This method creates a structured Markdown representation of the framework
        and its assessment results, suitable for documentation, reporting, or
        sharing with stakeholders.

        The generated Markdown includes:
        - Framework name as the main heading
        - Each domain as a section with its index and name
        - Questions within each domain with their indices and text
        - Allowed answer options for each question
        - Response details for answered questions, including:
          - The selected response
          - The reasoning behind the assessment
          - Supporting evidence excerpts from the manuscript

        Parameters
        ----------
        path : Path
            Destination file for the Markdown representation.

        Examples
        --------
        >>> framework = Framework(name="RoB2 Framework")
        >>> framework.export_to_markdown(Path("assessment_report.md"))
        """
        from risk_of_bias.export import export_framework_as_markdown

        export_framework_as_markdown(self, path)

    def export_to_html(self, path: Path) -> None:
        """Export the framework as an HTML document.

        Parameters
        ----------
        path : Path
            Destination file for the HTML representation.
        """
        from risk_of_bias.export import export_framework_as_html

        export_framework_as_html(self, path)

    def save(self, path: Path) -> None:
        """Save the framework as formatted JSON to ``path``.

        This method excludes raw_data fields from the JSON output to keep
        the saved files clean and focused on assessment results.

        Parameters
        ----------
        path : Path
            Location to write the JSON representation.
        """
        # Convert to JSON with indentation, excluding raw_data for cleaner files
        import json

        data = self.model_dump(
            exclude={
                "domains": {
                    "__all__": {"questions": {"__all__": {"response": {"raw_data"}}}}
                }
            }
        )
        path.write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path: Path) -> "Framework":
        """Load a framework from a JSON file at ``path``.

        Parameters
        ----------
        path : Path
            The file to read from.

        Returns
        -------
        Framework
            An instance populated with the data from the file.
        """
        return cls.model_validate_json(path.read_text())
