from pathlib import Path
import sys
import types

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
    result = runner.invoke(cli.app, ["analyse", str(pdf)])

    assert result.exit_code == 0
    assert called["manuscript"] == pdf
    assert called["model"] == settings.fast_ai_model
    assert called["guidance"] is None
    # the framework should be saved next to the manuscript
    assert (pdf.with_suffix(pdf.suffix + ".json")).exists()


def test_cli_sets_manuscript_filename(tmp_path, monkeypatch):
    """Test that the CLI properly sets the manuscript filename in the framework."""
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    from risk_of_bias import cli

    stored_framework = None

    def fake_run_framework(
        manuscript, model: str, framework, guidance_document, verbose: bool = False
    ):
        # Return a framework with manuscript name set (simulating run_framework behavior)
        from risk_of_bias.types._framework_types import Framework

        result_framework = Framework(name="dummy")
        result_framework.manuscript = manuscript.name
        nonlocal stored_framework
        stored_framework = result_framework
        return result_framework

    monkeypatch.setattr(cli, "run_framework", fake_run_framework)

    pdf = tmp_path / "my_research_paper.pdf"
    pdf.write_bytes(b"dummy")

    runner = CliRunner()
    result = runner.invoke(cli.app, ["analyse", str(pdf)])

    assert result.exit_code == 0
    assert stored_framework is not None
    assert stored_framework.manuscript == "my_research_paper.pdf"

    # Check that the saved JSON file contains the manuscript filename
    saved_json = pdf.with_suffix(pdf.suffix + ".json")
    assert saved_json.exists()

    # Load the saved framework and verify manuscript filename is preserved
    from risk_of_bias.types._framework_types import Framework

    loaded_framework = Framework.load(saved_json)
    assert loaded_framework.manuscript == "my_research_paper.pdf"


def test_cli_backward_compatibility_manuscript_filename(tmp_path, monkeypatch):
    """Test that CLI sets manuscript filename for existing frameworks without it."""
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    from risk_of_bias import cli
    from risk_of_bias.types._framework_types import Framework

    # Create a framework without manuscript filename (old format)
    old_framework = Framework(name="old_framework")
    pdf = tmp_path / "backward_compat_test.pdf"
    pdf.write_bytes(b"dummy")

    # Save the old framework
    json_path = pdf.with_suffix(pdf.suffix + ".json")
    old_framework.save(json_path)

    # Verify the saved framework doesn't have manuscript field set
    loaded_old = Framework.load(json_path)
    assert loaded_old.manuscript is None

    # Mock run_framework to ensure it's not called since JSON exists
    run_framework_called = False

    def fake_run_framework(*args, **kwargs):
        nonlocal run_framework_called
        run_framework_called = True
        return Framework(name="should_not_be_called")

    monkeypatch.setattr(cli, "run_framework", fake_run_framework)

    runner = CliRunner()
    result = runner.invoke(cli.app, ["analyse", str(pdf)])

    assert result.exit_code == 0
    assert not run_framework_called  # Should use existing JSON

    # Load the framework again and verify manuscript filename was added
    updated_framework = Framework.load(json_path)
    assert updated_framework.manuscript == "backward_compat_test.pdf"


def test_cli_exports_include_manuscript_name(tmp_path, monkeypatch):
    """Test that CLI exports (MD/HTML) include manuscript name."""
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    from risk_of_bias import cli
    from risk_of_bias.types._framework_types import Framework

    def fake_run_framework(
        manuscript, model: str, framework, guidance_document, verbose: bool = False
    ):
        result_framework = Framework(name="Test Framework")
        result_framework.manuscript = manuscript.name
        return result_framework

    monkeypatch.setattr(cli, "run_framework", fake_run_framework)

    pdf = tmp_path / "integration_test.pdf"
    pdf.write_bytes(b"dummy")

    runner = CliRunner()
    result = runner.invoke(cli.app, ["analyse", str(pdf)])

    assert result.exit_code == 0

    # Check that the exported files contain manuscript name
    md_path = pdf.with_suffix(pdf.suffix + ".md")
    html_path = pdf.with_suffix(pdf.suffix + ".html")

    assert md_path.exists()
    assert html_path.exists()

    md_content = md_path.read_text()
    html_content = html_path.read_text()

    assert "**Manuscript:** integration_test.pdf" in md_content
    assert "<strong>Manuscript: </strong>integration_test.pdf" in html_content


def test_cli_web_command(monkeypatch):
    calls = {}
    monkeypatch.setitem(
        sys.modules,
        "uvicorn",
        types.SimpleNamespace(
            run=lambda *args, **kwargs: calls.update({"args": args, **kwargs})
        ),
    )

    from risk_of_bias import cli

    runner = CliRunner()
    result = runner.invoke(
        cli.app, ["web", "--reload", "--host", "0.0.0.0", "--port", "1234"]
    )

    assert result.exit_code == 0
    assert calls["args"][0] == "risk_of_bias.web:app"
    assert calls["host"] == "0.0.0.0"
    assert calls["port"] == 1234
    assert calls["reload"] is True


def test_cli_analyse_directory_processes_all_pdfs(tmp_path, monkeypatch):
    """The directory command should analyse each PDF in the given folder."""
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    from risk_of_bias import cli

    processed = []

    def fake_run_framework(
        manuscript, model: str, framework, guidance_document, verbose: bool = False
    ):
        processed.append(manuscript)
        from risk_of_bias.types._framework_types import Framework

        result = Framework(name="dummy")
        result.manuscript = Path(manuscript).name
        return result

    monkeypatch.setattr(cli, "run_framework", fake_run_framework)

    pdf1 = tmp_path / "file1.pdf"
    pdf2 = tmp_path / "file2.pdf"
    pdf1.write_bytes(b"dummy")
    pdf2.write_bytes(b"dummy")

    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "ignored.pdf").write_bytes(b"dummy")

    runner = CliRunner()
    result = runner.invoke(cli.app, ["analyse", str(tmp_path)])

    assert result.exit_code == 0
    assert set(processed) == {pdf1, pdf2}

    for pdf in [pdf1, pdf2]:
        assert (pdf.with_suffix(pdf.suffix + ".json")).exists()
        assert (pdf.with_suffix(pdf.suffix + ".md")).exists()
        assert (pdf.with_suffix(pdf.suffix + ".html")).exists()
