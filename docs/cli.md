
The package comes with an easy to use command line interface (CLI) tool.
The CLI tool is installed along with the python package.

## Command Line Usage

The CLI tool provides several handy parameters you can adjust, these can be found using:

```console
> risk-of-bias --help

 Usage: risk-of-bias [OPTIONS] COMMAND [ARGS]...

 Run risk of bias assessment

╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.        │
│ --show-completion             Show completion for the current shell, to copy   │
│                               it or customise the installation.                │
│ --help                        Show this message and exit.                       │
╰────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────╮
│ analyse   Run risk of bias assessment on a manuscript.                         │
│ web       Launch the web interface using uvicorn.                               │
╰────────────────────────────────────────────────────────────────────────────────╯
```

And you can analyse a manuscript by simply passing the path to the file:

```console
risk-of-bias analyse /path/to/manuscript.pdf
```

To start the web interface run:

```console
risk-of-bias web
```
