from __future__ import annotations

import os
from pathlib import Path
import re

from fastapi.testclient import TestClient

os.environ["OPENAI_API_KEY"] = "test"

from risk_of_bias import web
from risk_of_bias.types._framework_types import Framework


def fake_run_framework(
    manuscript: Path,
    framework,
    model: str,
    verbose: bool = False,
    temperature: float = 0.2,
) -> Framework:
    result = Framework(name="Test Framework")
    result.manuscript = Path(manuscript).name
    return result


def test_index_returns_form():
    client = TestClient(web.app)
    response = client.get("/")
    assert response.status_code == 200
    assert "<form" in response.text
    assert '<select id="model"' in response.text


def test_analyze_and_download(tmp_path, monkeypatch):
    monkeypatch.setattr(web, "run_framework", fake_run_framework)

    client = TestClient(web.app)

    pdf = tmp_path / "manuscript.pdf"
    pdf.write_bytes(b"dummy")

    with pdf.open("rb") as f:
        response = client.post(
            "/analyze",
            data={"model": "dummy-model"},
            files={"file": ("manuscript.pdf", f, "application/pdf")},
        )

    assert response.status_code == 200
    assert "Download Results" in response.text
    assert "JSON" in response.text

    match = re.search(r"/download/(\w+)/result.json", response.text)
    assert match
    file_id = match.group(1)

    download_resp = client.get(f"/download/{file_id}/result.json")
    assert download_resp.status_code == 200
    assert download_resp.headers["content-type"] == "application/json"
