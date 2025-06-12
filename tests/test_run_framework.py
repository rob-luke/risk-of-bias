from pathlib import Path
import types

from risk_of_bias.frameworks.rob2 import get_rob2_framework
import risk_of_bias.run_framework as rf


def test_run_framework_omits_temperature(tmp_path, monkeypatch):
    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"dummy")

    captured = {}

    class FakeResponses:
        def parse(self, **kwargs):
            captured.update(kwargs)
            return types.SimpleNamespace(output_parsed=None, output_text="x")

    class FakeClient:
        def __init__(self, api_key=None):
            self.responses = FakeResponses()

    monkeypatch.setattr(rf, "OpenAI", lambda api_key=None: FakeClient())
    monkeypatch.setattr(rf, "pdf_to_base64", lambda p: "data")
    monkeypatch.setattr(rf, "create_domain_response_class", lambda d: object)

    framework = get_rob2_framework()
    framework.domains = framework.domains[:1]

    rf.run_framework(manuscript=pdf, framework=framework, temperature=None)
    assert "temperature" not in captured

    captured.clear()
    rf.run_framework(manuscript=pdf, framework=framework, temperature=0.7)
    assert captured.get("temperature") == 0.7
