from pathlib import Path

from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.types._framework_types import Framework


def test_framework_save_and_load(tmp_path: Path) -> None:
    framework = get_rob2_framework()
    save_path = tmp_path / "rob2.json"
    framework.save(save_path)

    loaded = Framework.load(save_path)
    assert isinstance(loaded, Framework)
    assert loaded.name == framework.name
    assert len(loaded.domains) == len(framework.domains)
