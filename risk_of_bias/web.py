from __future__ import annotations

from pathlib import Path
import tempfile
import uuid

from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.run_framework import run_framework
from risk_of_bias.types._framework_types import Framework

APP_TEMP_DIR = Path(tempfile.gettempdir()) / "risk_of_bias_web"
APP_TEMP_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Return a simple upload form."""
    return (
        "<html><body>"
        "<h1>Risk of Bias Assessment</h1>"
        "<form action='/analyze' method='post' enctype='multipart/form-data'>"
        "<input type='file' name='file' accept='application/pdf'>"
        "<input type='submit' value='Upload'>"
        "</form></body></html>"
    )


@app.post("/analyze", response_class=HTMLResponse)
def analyze(file: UploadFile = File(...)) -> str:
    """Process a PDF and return the assessment HTML."""
    file_id = uuid.uuid4().hex
    work_dir = APP_TEMP_DIR / file_id
    work_dir.mkdir(parents=True, exist_ok=True)

    filename = file.filename or "manuscript.pdf"
    pdf_path = work_dir / filename
    with pdf_path.open("wb") as f:
        f.write(file.file.read())

    framework: Framework = run_framework(
        manuscript=pdf_path,
        framework=get_rob2_framework(),
        verbose=False,
    )

    json_path = work_dir / "result.json"
    md_path = work_dir / "result.md"
    html_path = work_dir / "result.html"

    framework.save(json_path)
    framework.export_to_markdown(md_path)
    framework.export_to_html(html_path)

    html_content = html_path.read_text()
    download_links = (
        f"<p><a href='/download/{file_id}/result.json'>Download JSON</a> | "
        f"<a href='/download/{file_id}/result.md'>Download Markdown</a></p>"
    )

    return html_content.replace("<body>", f"<body>{download_links}", 1)


@app.get("/download/{file_id}/{filename}")
def download(file_id: str, filename: str) -> FileResponse:
    """Return a saved file for download."""
    file_path = APP_TEMP_DIR / file_id / filename
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)
