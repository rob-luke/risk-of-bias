# Web Interface

A simple web front end is provided using [FastAPI](https://fastapi.tiangolo.com/).
It lets you upload a PDF and view the standard RoB2 HTML report directly in your
browser.

## Running the server

Install the optional dependencies and start the server with `uvicorn`, or simply use `make web`:

```console
pip install "risk_of_bias[web]"
uvicorn risk_of_bias.web:app --reload
```

Open `http://127.0.0.1:8000` and upload your manuscript. After processing you
will see the report along with links to download the JSON and Markdown
representations.
