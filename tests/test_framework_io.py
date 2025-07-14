from pathlib import Path

from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.types._domain_types import Domain
from risk_of_bias.types._framework_types import Framework


def test_framework_save_and_load(tmp_path: Path) -> None:
    framework = get_rob2_framework()
    save_path = tmp_path / "rob2.json"
    framework.save(save_path)

    loaded = Framework.load(save_path)
    assert isinstance(loaded, Framework)
    assert loaded.name == framework.name
    assert len(loaded.domains) == len(framework.domains)


def test_framework_with_manuscript_filename(tmp_path: Path) -> None:
    """Test that the framework can store and retrieve manuscript filename."""
    framework = get_rob2_framework()
    manuscript_filename = "test_paper.pdf"
    framework.manuscript = manuscript_filename

    save_path = tmp_path / "rob2_with_manuscript.json"
    framework.save(save_path)

    loaded = Framework.load(save_path)
    assert isinstance(loaded, Framework)
    assert loaded.manuscript == manuscript_filename
    assert loaded.name == framework.name
    assert len(loaded.domains) == len(framework.domains)


def test_framework_manuscript_optional() -> None:
    """Test that manuscript field is optional and defaults to None."""
    framework = get_rob2_framework()
    assert framework.manuscript is None

    # Should be able to set it
    framework.manuscript = "another_paper.pdf"
    assert framework.manuscript == "another_paper.pdf"


def test_framework_str_includes_manuscript() -> None:
    """Test that the string representation includes manuscript filename when set."""
    framework = get_rob2_framework()

    # Without manuscript
    str_repr = str(framework)
    assert "Manuscript:" not in str_repr

    # With manuscript
    framework.manuscript = "test_study.pdf"
    str_repr = str(framework)
    assert "Manuscript: test_study.pdf" in str_repr


def test_framework_judgement_property() -> None:
    domain1 = Domain(index=1, name="Random", judgement_function=lambda d: "Low")
    domain2 = Domain(index=2, name="Deviation", judgement_function=lambda d: "High")
    framework = Framework(name="T", domains=[domain1, domain2])

    assert framework.judgement == "High"

    domain2.judgement_function = None
    assert framework.judgement is None

    domain_overall = Domain(
        index=3, name="Overall", judgement_function=lambda d: "High"
    )
    framework.domains.append(domain_overall)
    domain1.judgement_function = lambda d: "Low"
    domain2.judgement_function = lambda d: "Low"
    assert framework.judgement == "Low"
