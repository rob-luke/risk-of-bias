
The package comes with an easy to use command line interface (CLI) tool.
The CLI tool is installed along with the python package.

## Command Line Usage

The CLI tool provides several handy parameters you can adjust, these can be found using:

```console
> risk-of-bias --help

 Usage: risk-of-bias [OPTIONS] MANUSCRIPT

 Run risk of bias assessment on a manuscript.

 Processes a manuscript PDF file using the specified AI model and optional guidance document to perform risk of bias evaluation
 using the ROB2 framework.

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    manuscript      TEXT  Path to the manuscript PDF [default: None] [required]                                                │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --model                                 TEXT  OpenAI model name [default: gpt-4.1-nano]                                         │
│ --guidance-document                     TEXT  Optional guidance document [default: None]                                        │
│ --verbose               --no-verbose          Enable verbose output for debugging [default: verbose]                            │
│ --install-completion                          Install completion for the current shell.                                         │
│ --show-completion                             Show completion for the current shell, to copy it or customize the installation.  │
│ --help                                        Show this message and exit.                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

And you can analyse a manuscript by simply passing the path to the file:

```console
risk-of-bias /path/to/manuscript.pdf
```
