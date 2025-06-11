from __future__ import annotations

from pathlib import Path
import tempfile
import uuid

from fastapi import FastAPI
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

from risk_of_bias.config import settings
from risk_of_bias.frameworks.rob2 import get_rob2_framework
from risk_of_bias.run_framework import run_framework
from risk_of_bias.types._framework_types import Framework

APP_TEMP_DIR = Path(tempfile.gettempdir()) / "risk_of_bias_web"
APP_TEMP_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Return a simple upload form."""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Risk of Bias Assessment</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50 min-h-screen flex items-center justify-center">
        <div class="max-w-md w-full space-y-8 p-8">
            <div class="text-center">
                <h1 class="text-3xl font-bold text-gray-900 mb-2">Risk of Bias Assessment</h1>
                <p class="text-gray-600 mb-8">Upload a PDF manuscript to analyze potential bias in research methodology</p>
            </div>
            
            <form id="uploadForm" action="/analyze" method="post" enctype="multipart/form-data" class="space-y-6">
                <div>
                    <label for="file" class="block text-sm font-medium text-gray-700 mb-2">
                        Select PDF Manuscript
                    </label>
                    <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-gray-400 transition-colors">
                        <div class="space-y-1 text-center">
                            <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                            </svg>
                            <div class="flex text-sm text-gray-600">
                                <label for="file" class="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
                                    <span>Upload a file</span>
                                    <input id="file" name="file" type="file" accept="application/pdf" required class="sr-only">
                                </label>
                                <p class="pl-1">or drag and drop</p>
                            </div>
                            <p class="text-xs text-gray-500">PDF up to 10MB</p>
                        </div>
                    </div>
                </div>

                <div>
                    <label for="model" class="block text-sm font-medium text-gray-700 mb-2">
                        Select AI Model
                    </label>
                    <select id="model" name="model" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                        {{MODEL_OPTIONS}}
                    </select>
                </div>
                
                <div>
                    <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors">
                        Analyze Risk of Bias
                    </button>
                </div>
            </form>
            
            <!-- Loading state (hidden by default) -->
            <div id="loadingState" class="hidden text-center space-y-4">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                <div>
                    <h3 class="text-lg font-medium text-gray-900">Processing your manuscript...</h3>
                    <p class="text-sm text-gray-600 mt-2">This may take several minutes. Please don't close this window.</p>
                </div>
            </div>
        </div>
        
        <script>
            const dropZone = document.querySelector('.border-dashed');
            const fileInput = document.getElementById('file');
            const fileLabel = document.querySelector('label[for="file"] span');
            
            // Form submission handler
            document.getElementById('uploadForm').addEventListener('submit', function() {
                // Hide the form and show loading state
                document.getElementById('uploadForm').style.display = 'none';
                document.getElementById('loadingState').classList.remove('hidden');
            });
            
            // Update file input display when file is selected
            fileInput.addEventListener('change', function(e) {
                const fileName = e.target.files[0]?.name;
                if (fileName) {
                    fileLabel.textContent = fileName;
                }
            });
            
            // Drag and drop handlers
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, preventDefaults, false);
                document.body.addEventListener(eventName, preventDefaults, false);
            });
            
            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, highlight, false);
            });
            
            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, unhighlight, false);
            });
            
            dropZone.addEventListener('drop', handleDrop, false);
            
            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            function highlight(e) {
                dropZone.classList.add('border-indigo-400', 'bg-indigo-50');
            }
            
            function unhighlight(e) {
                dropZone.classList.remove('border-indigo-400', 'bg-indigo-50');
            }
            
            function handleDrop(e) {
                const dt = e.dataTransfer;
                const files = dt.files;
                
                if (files.length > 0) {
                    const file = files[0];
                    if (file.type === 'application/pdf') {
                        fileInput.files = files;
                        fileLabel.textContent = file.name;
                    } else {
                        alert('Please select a PDF file.');
                    }
                }
            }
        </script>
    </body>
    </html>
    """

    options = (
        f'<option value="{settings.fast_ai_model}">{settings.fast_ai_model}</option>'
        f'<option value="{settings.good_ai_model}">{settings.good_ai_model}</option>'
        f'<option value="{settings.best_ai_model}">{settings.best_ai_model}</option>'
    )

    return html.replace("{{MODEL_OPTIONS}}", options)


@app.post("/analyze", response_class=HTMLResponse)
def analyze(
    file: UploadFile = File(...), model: str = Form(settings.fast_ai_model)
) -> str:
    """Process a PDF with the selected model and return the assessment HTML."""
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
        model=model,
        verbose=True,
        temperature=settings.temperature,
    )

    json_path = work_dir / "result.json"
    md_path = work_dir / "result.md"
    html_path = work_dir / "result.html"

    framework.save(json_path)
    framework.export_to_markdown(md_path)
    framework.export_to_html(html_path)

    html_content = html_path.read_text()
    download_links = (
        '<div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-6">'
        '<div class="flex">'
        '<div class="ml-3">'
        '<h3 class="text-sm font-medium text-blue-800">Download Results</h3>'
        '<div class="mt-2 text-sm text-blue-700">'
        '<p class="space-x-4">'
        f'<a href="/download/{file_id}/result.json" class="font-medium underline hover:text-blue-600">JSON </a> | '
        f'<a href="/download/{file_id}/result.md" class="font-medium underline hover:text-blue-600">Markdown </a> | '
        f'<a href="/download/{file_id}/result.html" class="font-medium underline hover:text-blue-600">HTML </a>'
        "</p>"
        "</div>"
        "</div>"
        "</div>"
        "</div>"
    )

    # Add Tailwind CSS to the results page if it doesn't already have it
    if '<script src="https://cdn.tailwindcss.com"></script>' not in html_content:
        html_content = html_content.replace(
            "<head>", '<head><script src="https://cdn.tailwindcss.com"></script>', 1
        )

    return html_content.replace("<body>", f"<body>{download_links}", 1)


@app.get("/download/{file_id}/{filename}")
def download(file_id: str, filename: str) -> FileResponse:
    """Return a saved file for download."""
    file_path = APP_TEMP_DIR / file_id / filename
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)


# Export the app for Vercel
# The FastAPI app is already ASGI compatible, so we just need to export it
# Vercel will automatically detect and use the 'app' variable


# For local development
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
