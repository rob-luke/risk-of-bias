from types import SimpleNamespace

from risk_of_bias import run_framework
from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._framework_types import Framework
from risk_of_bias.types._question_types import Question


def test_run_framework_omits_negative_temperature(tmp_path, monkeypatch):
    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"dummy")

    parse_kwargs = {}

    class DummyResponses:
        def parse(self, **kwargs):
            parse_kwargs.update(kwargs)
            return SimpleNamespace(output_parsed=None, output_text="")

    class DummyClient:
        def __init__(self, *args, **kwargs):
            self.responses = DummyResponses()

    monkeypatch.setattr(run_framework, "OpenAI", lambda api_key=None: DummyClient())
    monkeypatch.setattr(run_framework, "pdf_to_base64", lambda path: "encoded")
    monkeypatch.setattr(
        run_framework, "create_openai_message", lambda *args, **kwargs: {}
    )
    monkeypatch.setattr(
        run_framework, "create_domain_response_class", lambda domain: object
    )

    framework = Framework(
        name="Test Framework",
        domains=[Domain(name="D1", index=1, questions=[Question(question="Q1")])],
    )

    run_framework.run_framework(
        manuscript=pdf,
        framework=framework,
        temperature=-1.0,
    )

    assert "temperature" not in parse_kwargs
