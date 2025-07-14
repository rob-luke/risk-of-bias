The API is comprised of a hierarchical set of types that mirror the structure of risk-of-bias assessment frameworks like RoB2. This design enables systematic evaluation of research manuscripts through structured questioning and evidence-based responses.

- **Frameworks** define the top-level assessment structure containing multiple evaluation domains. In the RoB2 context, a Framework represents the complete "Risk of Bias 2" tool for randomized trials, organizing five primary assessment domains and an overall judgement domain into a cohesive evaluation instrument.

- **Domains** represent specific categories of bias within a framework. Each domain focuses on a particular aspect of study methodology that could introduce bias. Domains expose a `judgement` property that computes the final risk rating from the answers provided. For RoB2, the five primary domains are: (1) bias from randomization process, (2) bias from deviations from intended interventions, (3) bias from missing outcome data, (4) bias in outcome measurement, and (5) bias in selection of reported results. An additional "Overall" domain records the final risk-of-bias judgement and predicted direction of bias.

- **Questions** are the specific signaling questions within each domain that guide the assessment process. These questions are designed to systematically evaluate potential sources of bias, with predefined allowed answers (typically "Yes", "Probably Yes", "Probably No", "No", "No Information", "Not Applicable"). But if the user requests no predefined answers (using None), then a string answer will be provided. Questions can be marked as required and are indexed for systematic processing.

- **Responses** capture the AI model's assessment for each question, structured as `ReasonedResponseWithEvidence` objects that include:
  - `evidence`: List of text excerpts from the manuscript that support the assessment
  - `reasoning`: The model's explanation of how the evidence leads to the conclusion
  - `response`: The selected answer from the allowed options, or a self selected string if None is provided for the allowed options.

This hierarchical structure ensures that bias assessments are systematic, traceable, and evidence-based, following established methodological guidelines while leveraging AI capabilities for efficient manuscript analysis.

## Type Definitions

### Framework

::: risk_of_bias.types._framework_types.Framework
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 4


#### Pre-built Frameworks

The package provides ready-to-use frameworks that implement established risk-of-bias assessment methodologies. These frameworks come pre-configured with all necessary domains, questions, and answer options, allowing you to immediately begin manuscript analysis without manual setup.

##### RoB2 Framework

::: risk_of_bias.frameworks.get_rob2_framework
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 6


### Executing a framework

::: risk_of_bias.run_framework
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 4

### Manual Entry

::: risk_of_bias.human.run_human_framework
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 4

### Domain

::: risk_of_bias.types.Domain
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 4

### Question

::: risk_of_bias.types.Question
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 4

### Response

::: risk_of_bias.types.ReasonedResponseWithEvidence
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 4

## Summary and Analysis Functions

After completing individual risk-of-bias assessments using frameworks, researchers typically need to analyze results across multiple studies for systematic reviews, meta-analyses, or research synthesis. The summary functions provide essential tools for aggregating, visualizing, and exporting assessment results in formats compatible with established research workflows.

These functions address three critical needs in evidence synthesis:

1. **Batch Processing**: Loading and processing multiple completed assessments from saved framework files
2. **Data Aggregation**: Extracting domain-level judgements across studies for comparative analysis  
3. **Standardized Export**: Creating outputs compatible with specialized visualization tools like RobVis

This workflow supports the transition from individual study assessment to systematic evidence synthesis, enabling researchers to identify patterns of bias across study collections and generate publication-ready visualizations for systematic reviews.

### Loading Multiple Assessments

::: risk_of_bias.summary.load_frameworks_from_directory
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 4

### Creating Assessment Summaries

::: risk_of_bias.summary.summarise_frameworks
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 4

### Exporting for Visualization

::: risk_of_bias.summary.export_summary
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 4

### Comparing Assessors

::: risk_of_bias.compare.compare_frameworks
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 4

### Assessor Agreement Plot

::: risk_of_bias.visualisation.plot_assessor_agreement
    handler: python
    options:
      show_root_heading: true
      show_source: false
      show_root_full_path: true
      heading_level: 4



