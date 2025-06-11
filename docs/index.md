# Risk of Bias

## AI Enabled Risk of Bias Assessment

Risk of bias tools are systematic frameworks primarily used in systematic reviews to evaluate potential flaws in individual studies that could lead to a systematic deviation from the true effect of an intervention. 
They aim to identify specific mechanisms through which bias might be introduced into study results, such as problems arising during the study design, conduct, or analysis.
This package provides AI and software tools to assist researchers in conducting risk of bias analyses.

### Key Features

- **Advanced AI** provides robust and independent risk of bias analysis
- **Standard Frameworks** such as RoB2 are provided out of the box
- **Batch processing** for systematic reviews and meta-analyses
- **Web interface** for single manuscript analysis with download options
- **Command line interface** for integration into research workflows
- **Latest AI models** for evidence extraction and bias assessment
- **RobVis-compatible exports** for publication-ready visualizations


## Getting Started

### Installation

You can install the program using the following pip command:

```console
pip install risk_of_bias[all]
```

### Web Interface

A simple web interface is provided to analyse a single manuscript.
To start the web interface run:

```console
risk-of-bias web
```

Then open `http://127.0.0.1:8000` and upload your manuscript. 
After processing you will see the report along with links to 
download the JSON and Markdown representations.

### Command Line Interface

The package comes with an easy to use command line interface (CLI) tool.
The CLI tool is installed along with the python package.
The CLI tool provides several handy parameters you can adjust.
Complete documentation is available in [cli](cli.md)

But to get started, you can analyse a manuscript by simply passing the path to the file:

```console
risk-of-bias analyse /path/to/manuscript.pdf
```

For systematic reviews, you can analyse entire directories and automatically generate RobVis-compatible CSV summaries:

```console
risk-of-bias analyse /path/to/manuscripts/
```


## Frameworks

The _Risk of Bias_ tool currently only supports the RoB 2 framework.
However, it is designed to be extensible, please raise an issue if there's another framework you are interested in. 
See [frameworks](frameworks.md) and [api/frameworks](api.md#framework) for additional details and context.


## Statement on the Use of AI in Research

AI does not replace human judgment in risk of bias assessment. Instead, these tools should be viewed as powerful assistants, complementing human expertise. The established gold standard, often involving two independent human reviewers and a third for adjudication, remains paramount for rigorous assessment. However, AI can augment this process; for instance, an AI could serve as an additional reviewer alongside human experts, providing a systematically derived perspective, with a human still making the final adjudication. Recognizing that both human reviewers and AI systems can have inherent biases, incorporating an AI perspective can offer a different lens through which to evaluate studies. Moreover, in situations where resource constraints make achieving the full gold standard difficult, AI tools can provide valuable support, helping to elevate the overall consistency and thoroughness of bias assessment as the field progresses towards universally ideal practices.


## References


```
Sterne JAC, Savović J, Page MJ, Elbers RG, Blencowe NS, Boutron I, Cates CJ,
Cheng H-Y,  Corbett MS, Eldridge SM, Hernán MA, Hopewell S, Hróbjartsson A,
Junqueira DR, Jüni P, Kirkham JJ, Lasserson T, Li T, McAleenan A, Reeves BC,
Shepperd S, Shrier I, Stewart LA, Tilling K, White IR, Whiting PF, Higgins JPT.
RoB 2: a revised tool for assessing risk of bias in randomised trials. 
BMJ 2019; 366: l4898.
```
