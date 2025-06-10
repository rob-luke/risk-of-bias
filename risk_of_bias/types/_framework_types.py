from pydantic import BaseModel

from risk_of_bias.types._domain_types import Domain


class Framework(BaseModel):
    domains: list[Domain] = []
    name: str = ""

    def __str__(self) -> str:
        """Custom string representation of the Framework."""
        if not self.domains:
            return "Framework: No domains defined"

        lines = [f"Framework: {self.name}"]
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
