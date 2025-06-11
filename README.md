# Risk of Bias

## AI Enabled Risk of Bias Assessment

Risk of bias tools are systematic frameworks primarily used in systematic reviews to evaluate potential flaws in individual studies that could lead to a systematic deviation from the true effect of an intervention. 
They aim to identify specific mechanisms through which bias might be introduced into study results, such as problems arising during the study design, conduct, or analysis.
This package provides AI and software tools to assist researchers in conducting risk of bias analyses.


## Getting Started

### Installation

You can install the program using the following pip command:

```console
pip install risk_of_bias[all]
```


### Command Line Interface

The package comes with an easy to use command line interface (CLI) tool.
The CLI tool is installed along with the python package.
The CLI tool provides several handy parameters you can adjust.
Complete [documentation](https://rob-luke.github.io/risk-of-bias/) is available in the cli section.

But to get started, you can analyse a manuscript by simply passing the path to the file:

```console
risk-of-bias analyse /path/to/manuscript.pdf
```

The results will be saved next to the pdf as a json, html, and markdown file.
The output will look something like:

```text
Domain 1: Bias arising from the randomization process.

  Question 1.1: Question 1.1: Was the allocation sequence random? (['Yes', 'Probably Yes', 'Probably No', 'No', 'No Information', 'Not Applicable'])
    Response: AllowedResponses.Yes
      Reasoning: The methods section describes the study as a 'randomized crossover study' and states that 'Pairs were then randomized to receive the almond or no-almond (control) interventions.' This indicates that a random allocation sequence was used to assign participants to the initial intervention group. However, the specific method of random sequence generation (e.g., computer-generated random numbers, random number tables) is not described in the provided text.
        Evidence: A 14-week, randomized crossover study was conducted from January 2014 to May 2014. ... Pairs were then randomized to receive the almond or no-almond (control) interventions and asked to complete daily and weekly questionnaires as well as 3 nonconsecutive, unannounced 24-hour dietary recalls throughout the 3-week intervention.



  Question 1.2: Question 1.2: Was the allocation sequence concealed until participants were enrolled and assigned to interventions? (['Yes', 'Probably Yes', 'Probably No', 'No', 'No Information', 'Not Applicable'])
    Response: AllowedResponses.No_Information
      Reasoning: There is no explicit information in the provided text about how the allocation sequence was concealed from those enrolling participants. The methods do not mention any procedures such as sealed envelopes, central randomization, or other mechanisms to ensure allocation concealment.
        Evidence: No information is provided in the methods section regarding allocation concealment procedures.



  Question 1.3: Question 1.3: Did baseline differences between intervention groups suggest a problem with the randomization process? (['Yes', 'Probably Yes', 'Probably No', 'No', 'No Information', 'Not Applicable'])
    Response: AllowedResponses.No
      Reasoning: The baseline characteristics table (Table 1) shows demographic and anthropometric data for both parents and children, but since this is a crossover study, each participant serves as their own control, and baseline differences between groups are less relevant. There is no mention of significant baseline imbalances or problems with randomization in the text.
        Evidence: Table 1 – Characteristics of 29 child and parent pairs participating in a study examining the effects of almond consumption on dietary quality, gastrointestinal function, inflammation, and immunity ... Most of the parents were non-Hispanic white women, and most children attended a school or daycare outside the home (Table 1).

...
```


Or you can analyse an entire directory using:

```console
risk-of-bias analyse /path/to/manuscripts/
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


## Frameworks

The _Risk of Bias_ tool currently only supports the RoB 2 framework.
However, it is designed to be extensible, please raise an issue if there's another framework you are interested in. 
See [documentation](https://rob-luke.github.io/risk-of-bias/) of frameworks and api/frameworks for additional details and context.


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