
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
│ human     Enter risk of bias results manually
 │
│ web       Launch the web interface using uvicorn.                              │
╰────────────────────────────────────────────────────────────────────────────────╯
```

The `analyse` command accepts options for model selection and the sampling
temperature. Temperature defaults to `0.2` and controls the randomness of
the OpenAI model's responses. If a negative value is supplied the
temperature setting is omitted, and the server default is used instead.

And you can analyse a manuscript by simply passing the path to the file:

```console
risk-of-bias analyse /path/to/manuscript.pdf
```

### Manual Entry

If you prefer to record answers yourself, use the `human` command:

```console
risk-of-bias human /path/to/manuscript.pdf
```

### Evaluating Research Protocols

You can run the same command on a draft protocol prior to starting a study:

```console
risk-of-bias analyse /path/to/protocol.pdf
```

Assessing protocols in advance helps verify compliance with best-practice
guidelines and reveals potential methodological problems before commencement.

## Guidance Documents

The CLI supports an optional `--guidance-document` parameter that allows you to provide domain-specific instructions or corrections to the AI assessment process. This feature is particularly valuable when:

- **Domain-specific expertise is required**: For specialized fields like pediatric studies, surgical interventions, or rare diseases where standard risk-of-bias criteria may need contextual interpretation
- **Correcting systematic AI biases**: When the AI consistently misinterprets certain methodological aspects or shows patterns of being overly lenient or conservative in specific domains
- **Journal-specific requirements**: When conducting assessments according to particular journal guidelines or institutional standards
- **Training consistency**: When multiple reviewers need to apply consistent interpretation criteria across a large systematic review

### Usage

```console
risk-of-bias analyse manuscript.pdf --guidance-document domain_guidance.pdf
```

### Creating Effective Guidance Documents

A guidance document should be a PDF containing:

1. **Specific interpretation criteria** for ambiguous scenarios
2. **Domain-specific examples** of how to classify common situations
3. **Clarifications on borderline cases** that frequently arise in your field
4. **Calibration instructions** if the AI is systematically too strict or lenient

For example, a guidance document for surgical studies might specify how to interpret blinding when complete blinding is impossible, or provide criteria for assessing outcome measurement bias in subjective surgical outcomes.

The guidance document is provided to the AI before manuscript analysis, ensuring consistent application of your specified criteria throughout the assessment process.

## Batch Analysis

You can analyse an entire directory of manuscripts for systematic reviews and meta-analyses:

```console
risk-of-bias analyse /path/to/manuscripts/
```

When processing multiple manuscripts, the tool automatically generates a RobVis-compatible CSV summary file containing domain-level risk-of-bias judgements across all studies. This CSV can be directly imported into the RobVis visualization tool or used with statistical software for further analysis.

## JSON Data Storage and Caching

The tool automatically saves complete assessment results in JSON format alongside each analyzed manuscript. This JSON storage system provides several key benefits:

### Automatic Caching and Reuse

```console
# First run - analyzes manuscript.pdf and saves manuscript.json
risk-of-bias analyse manuscript.pdf

# Second run - automatically loads from manuscript.json (no AI call needed)
risk-of-bias analyse manuscript.pdf
```

When re-running analysis on files or directories, the tool automatically detects existing JSON files and loads previous results instead of re-processing. This is particularly valuable for:

- **Large systematic reviews**: Process hundreds of papers across multiple sessions without redundant analysis
- **Iterative workflows**: Make adjustments to post-processing or visualization without re-running expensive AI analysis
- **Cost optimization**: Avoid unnecessary OpenAI API calls when refining batch processing workflows

### Forcing Reanalysis

To re-analyze previously processed files (e.g., after model updates or methodology changes):

```console
# Delete JSON files manually
rm *.json

# Or use the --force flag
risk-of-bias analyse manuscript.pdf --force
```

### Data Sharing and Reproducibility

JSON files contain the complete assessment data structure including:

- All question responses with confidence levels
- Detailed reasoning for each assessment decision  
- Specific evidence excerpts from the manuscript text
- Raw AI model responses for verification
- Metadata including model version and assessment parameters

This comprehensive data format enables:

- **Research collaboration**: Share complete assessment datasets with team members
- **Methodology verification**: Independent review of AI reasoning and evidence selection
- **Standards compliance**: Meet journal requirements for transparent bias assessment documentation
- **Meta-analysis integration**: Programmatic access to assessment data for statistical analysis

For complete details on the summary functions, data formats, and programmatic access to batch analysis features, see the [API documentation](api.md#summary-and-analysis-functions).