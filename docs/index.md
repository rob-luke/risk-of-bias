# Risk of Bias

AI and software for assesing risk of bias.

Risk of bias tools are systematic frameworks primarily used in systematic reviews to evaluate potential flaws in individual studies that could lead to a systematic deviation from the true effect of an intervention. 
They aim to identify specific mechanisms through which bias might be introduced into study results, such as problems arising during the study design, conduct, or analysis.
This package provides AI and software tools to assist researchers in conducting risk of bias analyses.


## Getting Started

### Installation

You can install the program using the following pip command:

```console
pip install risk_of_bias[all]
```

### Command Line Usage

The package comes with an easy to use command line interface (CLI) tool.
The CLI tool is installed along with the python package.
The CLI tool provides several handy parameters you can adjust.
Complete documentation is available in [cli](cli.md)

But to get started, you can analyse a manuscript by simply passing the path to the file:

```console
risk-of-bias analyse /path/to/manuscript.pdf
```

To start the web interface run:

```console
risk-of-bias web
```


## Frameworks

The _Risk of Bias_ tool currently only supports the RoB 2 framework.
However, it is designed to be extensible, please raise an issue if there's another framework you are interested in. 
See [frameworks](frameworks.md) and [api/frameworks](api.md#framework) for additional details and context.


## References


```
Sterne JAC, Savović J, Page MJ, Elbers RG, Blencowe NS, Boutron I, Cates CJ,
Cheng H-Y,  Corbett MS, Eldridge SM, Hernán MA, Hopewell S, Hróbjartsson A,
Junqueira DR, Jüni P, Kirkham JJ, Lasserson T, Li T, McAleenan A, Reeves BC,
Shepperd S, Shrier I, Stewart LA, Tilling K, White IR, Whiting PF, Higgins JPT.
RoB 2: a revised tool for assessing risk of bias in randomised trials. 
BMJ 2019; 366: l4898.
```
