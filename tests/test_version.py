"""Test version consistency between package and pyproject.toml."""

from pathlib import Path
import tomllib

import risk_of_bias


def test_version_consistency():
    """Test that the version is a valid semantic version"""
    # Get the package version from pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomllib.load(f)
    package_version = pyproject_data["project"]["version"]

    # Validate the version format
    assert isinstance(package_version, str), "Package version should be a string"
    assert package_version.count(".") == 2, "Package version should have two dots"
    major, minor, patch = package_version.split(".")
    assert major.isdigit(), "Major version should be a number"
    assert minor.isdigit(), "Minor version should be a number"
    assert patch.isdigit(), "Patch version should be a number"
