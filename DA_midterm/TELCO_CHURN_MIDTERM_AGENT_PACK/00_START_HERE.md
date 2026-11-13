# Telco Customer Churn Analytics: Midterm Project Agent Pack

## Purpose

Build an original, reproducible **Python** data analytics project for the university course **Data Analysis and Visualization**, using IBM's public **Telco Customer Churn** sample dataset. The project's practical question is:

> Which customer characteristics are associated with churn, how well can we identify at-risk customers, and which retention actions should a manager prioritize on the basis of measured evidence?

The finished work must be a working interactive analytics product with four connected layers: **descriptive, diagnostic, predictive and prescriptive analytics**. It must satisfy every mandatory technical requirement in the original midterm assignment. A separate assistant will later use the generated evidence to write the Word report and slides, so **do not spend project time generating the academic report or PowerPoint**.

## Read these files in order

1. `01_OFFICIAL_REQUIREMENTS_EN.md`: faithful English interpretation of the instructor's explicit requirements and completion checks.
2. `02_PROJECT_IMPLEMENTATION_SPEC.md`: project scope, functionality, reproducibility, engineering standards and phased execution.
3. `03_REPORT_EVIDENCE_EXPORT_SPEC.md`: exact evidence deliverables, validation and ZIP packaging.
4. `04_AGENT_INITIAL_PROMPT.md`: ready-to-paste master instruction for the coding agent.

## Sources and rules

- **Primary authority:** The original Vietnamese midterm assignment DOCX. If this pack and the original differ, follow the original and flag the difference.
- **Dataset:** IBM Telco Customer Churn sample, `Telco-Customer-Churn.csv`, accessible in the original IBM GitHub repository: <https://github.com/IBM/telco-customer-churn-on-icp4d> and <https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv>.
- **Reference project, inspiration only:** <https://github.com/UtkarshRai-ds/telco-churn-prediction>.
- **Important provenance caveat:** IBM identifies this as **sample data for a fictional telecommunications company**. Do not describe the records as verified real subscriber observations, real commercial impact, or a modern real-world deployment.
- **Originality:** Do not clone the reference project, paste code from it, reproduce its charts/README, reuse its trained models or copy its numerical findings. Independently design and implement your own solution using the cited dataset and the assignment. If code from any third-party source is actually incorporated, check license permissions and attribute it explicitly; prefer writing your own code.
- **No invented evidence:** Every count, proportion, metric, figure and recommendation must trace to the executing code and the selected dataset. Predictions do not establish causality or the effect of a retention intervention.
- **Separate final-term project:** This project must not reuse the Bike Sharing dataset used for the other assignment.

## What the agent must deliver

- Working Python analytics and training pipeline, documented CLI, tests, dependencies and a functioning Streamlit dashboard.
- Analyses covering the four layers, at least six **genuinely different chart types**, at least two genuinely trained models, documented train/test strategy, model explanations and evidence-based recommendations.
- A self-contained `report_evidence_package/` folder with numerical tables, plots, dashboard screenshots, interpretation, provenance, and a mapping to each official requirement.
- A validated `report_evidence_package.zip` for transfer to a separate report-writing assistant.
- A concise completion report noting checks actually run and outstanding limitations. The agent must not declare success if the environment cannot run the project.

## Suggested scope discipline

This is a course analytics project, not a banking backend or distributed system. Prefer a readable, modular Python codebase and a useful dashboard over unnecessary APIs, microservices, queues, databases, custom ML frameworks or elaborate infrastructure. Test the core research and UX workflows thoroughly.
