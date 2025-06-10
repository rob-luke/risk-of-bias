from pathlib import Path

from typer.testing import CliRunner

from risk_of_bias.config import settings


def test_cli_runs_with_defaults(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    from risk_of_bias import cli

    called = {}

    def fake_run_framework(
        manuscript, model: str, framework, guidance_document, verbose: bool = False
    ):
        called["manuscript"] = manuscript
        called["model"] = model
        called["framework"] = framework
        called["guidance"] = guidance_document
        called["verbose"] = verbose
        # return a minimal Framework instance so cli can call .save()
        from risk_of_bias.types._framework_types import Framework

        return Framework(name="dummy")

    monkeypatch.setattr(cli, "run_framework", fake_run_framework)

    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"dummy")

    runner = CliRunner()
    result = runner.invoke(cli.app, [str(pdf)])

    assert result.exit_code == 0
    assert called["manuscript"] == pdf
    assert called["model"] == settings.fast_ai_model
    assert called["guidance"] is None
    # the framework should be saved next to the manuscript
    assert (pdf.with_suffix(pdf.suffix + ".json")).exists()
