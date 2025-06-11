
The package comes with an easy to use command line interface (CLI) tool.
The CLI tool is installed along with the python package.

## Command Line Interface

The CLI tool provides several handy parameters you can adjust, these can be found using:

```console
> risk-of-bias --help

 Usage: risk-of-bias [OPTIONS] COMMAND [ARGS]...

 Run risk of bias assessment

╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.        │
│ --show-completion             Show completion for the current shell, to copy   │
│                               it or customise the installation.                │
│ --help                        Show this message and exit.                      │
╰────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────╮
│ analyse   Run risk of bias assessment on a manuscript or directory             │
│ web       Launch the web interface using uvicorn.                              │
╰────────────────────────────────────────────────────────────────────────────────╯
```

And you can analyse a manuscript by simply passing the path to the file:

```console
risk-of-bias analyse /path/to/manuscript.pdf
```

## Batch Analysis

You can analyse an entire directory of manuscripts for systematic reviews and meta-analyses:

```console
risk-of-bias analyse /path/to/manuscripts/
```

When processing multiple manuscripts, the tool automatically generates a RobVis-compatible CSV summary file containing domain-level risk-of-bias judgements across all studies. This CSV can be directly imported into the RobVis visualization tool or used with statistical software for further analysis.

For complete details on the summary functions, data formats, and programmatic access to batch analysis features, see the [API documentation](api.md#summary-and-analysis-functions).