---
title: 'Risk of Bias: Explainable, human-in-the-loop software for general risk-of-bias assessment'
tags:
  - Python
  - reviews
  - risk of bias
  - open-science
authors:
  - name: Robert Luke
    orcid: 0000-0002-4930-8351
    equal-contrib: false
    affiliation: "1"
affiliations:
 - name: Macquarie University, Macquarie University Hearing & Department of Linguistics, Australian Hearing Hub, Sydney, New South Wales, Australia
   index: 1
 - name: The University of Melbourne, Human Nutrition Group, School of Agriculture, Food and Ecosystem Sciences, Victoria, Australia
   index: 2
date: 11 June 2025
bibliography: paper.bib
---

# Summary

Assessing risk of bias (RoB) is a fundamental component of evidence synthesis, directly affecting the credibility and interpretability of systematic reviews and meta-analyses. RoB assessment clarifies to what extent findings from primary studies can be trusted, guiding both research conclusions and downstream policy or clinical recommendations [@higgins2019assessing]; [@whiting2016robis]. Despite its importance, RoB assessment remains time-intensive and demands specialized expertise. The _risk-of-bias_ Python package provides a general, framework-agnostic software assistant for risk-of-bias assessment, combining explainable AI with open, programmable infrastructure. The tool is designed to support any domain-based risk-of-bias instrument, with the widely adopted Cochrane RoB 2 tool for randomized trials [@sterne2019rob] implemented as the first example. By storing explicit evidence and reasoning for every answer, and providing both CLI and web interfaces, _risk-of-bias_ enables explainable, auditable, and efficient assessment, supporting both “living” reviews and reproducible research workflows.

# Statement of Need

Manual risk-of-bias assessment is a critical bottleneck in evidence synthesis, with typical reviews requiring 10–60 minutes of expert time per study, repeated across dozens or hundreds of manuscripts [@savovic2014evaluation]. The gold standard remains two independent human reviewers with a third for adjudication—an approach that is resource intensive and often unattainable in time- or resource-constrained projects. Commercial platforms (e.g., Covidence [@kellermeyer2018covidence], DistillerSR) offer user-friendly interfaces, while AI-driven tools like RobotReviewer [@marshall2016robotreviewer] provide partial automation for specific tasks, but few options combine openness, programmability, explainability, and affordability. The _risk-of-bias_ package addresses this gap by delivering a fully open-source, scriptable tool that provides structured, explainable output, and supports integration with both human and AI-driven workflows. The package’s transparency and extensibility support the evolving landscape of “living” systematic reviews and the continual improvement of AI models, accommodating both commercial and open models as they become available.

# Software Overview & Architecture

_Risk-of-bias_ is built around a generic, hierarchical assessment structure:

> **Framework → Domain → Question → Response**

This mirrors all major RoB instruments, enabling use beyond the Cochrane RoB 2 tool. The package offers:

- A modular core, where any framework is defined as a JSON schema capturing its domains, questions, and allowed responses.
- Data classes (via Pydantic) that explicitly store, for each answer: the response, supporting evidence (verbatim text from the manuscript), and a natural language reasoning/explanation.
- Multiple user interfaces: a command-line interface (CLI) for batch assessment and workflow integration, and a web interface for interactive analysis and report download. This enables both technical and non-technical users to use the tool effectively.
- An engine that systematically applies the framework to imported manuscripts, walking through the assessment questions and storing structured outputs.
- Export functions for RobVis-compatible CSV summaries, facilitating high-quality visualizations using the _robvis_ R package or web app [@mcguinness2021risk].

For batch analysis, the CLI allows processing of entire directories of manuscripts, automatically generating summary CSVs for cross-study visualization or meta-analysis.

# Explainable AI & Evidence-linked Reasoning

Unlike “black-box” AI tools, _risk-of-bias_ stores and surfaces both the **evidence** (exact textual excerpts) and the **reasoning** (explanation of how evidence informs the answer) for every question in every domain. This design meets the auditability requirements of leading journals and systematic review standards, supporting both transparent reporting and dispute resolution in collaborative review teams. When used alongside independent human reviewers, the software’s explicit justifications make it easy to compare and resolve discrepancies, and to understand why the software or a reviewer made a particular assessment. This explainable approach is particularly valuable as LLM-based and hybrid systems become more common in evidence synthesis, ensuring assessments remain interpretable and verifiable.

# Human-in-the-Loop Augmentation

The _risk-of-bias_ package is designed to augment, not replace expert human judgment. Its intended workflow is to serve as an additional reviewer alongside the established approach of two independent human reviewers, with a third reviewer adjudicating discrepancies. However, AI can meaningfully augment this process: for example, the software can serve as an additional reviewer alongside human experts, providing a systematically derived perspective while leaving final adjudication to a human. Incorporating an AI perspective can help reveal potential biases in both directions and offer a complementary lens for evaluating studies. In situations where resource constraints make the gold standard unachievable, AI tools can support more consistent and thorough assessments, helping raise the overall quality of risk-of-bias evaluations as the field moves toward best practice.

# Current Framework Support & Extensibility

While RoB 2 for randomized trials is implemented end-to-end (with both CLI and web UI, and export to RobVis/CSV [@mcguinness2021robvis]), the architecture is framework-agnostic by design. Additional frameworks—such as ROBINS-I [@sterne2016robins], QUADAS-2 [@whiting2011quadas], and PROBAST [@wolff2019probast]—can be registered as JSON schemas immediately, leveraging the same hierarchical logic (framework → domain → question → response), and is in the roadmap for future explicit inclusion in the software. This software is already being utilised to support study design and systematic literarure reviews.

# Acknowledgements

We acknowledge the foundational work of the _robvis_ package [@mcguinness2021robvis], the authors of RoB 2 [@sterne2019rob2], and the wider open-source and evidence synthesis community whose contributions inform both the methodology and the software ecosystem.

# References
