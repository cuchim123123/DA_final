# Initial Prompt for AI Coding Agent

You are responsible for independently building and validating an end-to-end **Python** project for my university **Data Analysis and Visualization** midterm assignment.

## What to read first

Read the following project documents completely, in order:

1. `00_START_HERE.md`
2. `01_OFFICIAL_REQUIREMENTS_EN.md`
3. `02_PROJECT_IMPLEMENTATION_SPEC.md`
4. `03_REPORT_EVIDENCE_EXPORT_SPEC.md`

Also read the **original Vietnamese midterm assignment DOCX**, if it is available in the workspace. The original is the authoritative statement of assignment requirements.

## Project choice

Build **Telco Customer Churn Analytics**, using the original public IBM `Telco-Customer-Churn.csv` sample data. The listed topics in the instructor's assignment are suggestions; this chosen Telco topic is intentional.

Use the following public project ONLY as an optional example of the type of analytics product and UX that can be built:

https://github.com/UtkarshRai-ds/telco-churn-prediction

**Do not clone, fork, copy, paraphrase its source code, import its models, reuse its derived artifacts, or report its metrics as ours.** Independently design and write the code. Cite relevant third-party inspiration and data sources. Build against the original IBM dataset instead. The reference project has documented reproducibility problems, so do not inherit its implementation decisions without evaluating them.

## Success criteria

Produce a clean, maintainable, reproducible Python codebase that **actually solves** the churn analytics problem, not just a dashboard mockup or a set of academic explanations.

The project must cover:

- **Descriptive analytics** with reliable numeric findings.
- **Diagnostic analytics** with meaningful, carefully qualified associations.
- **Predictive analytics** comparing at least two properly trained algorithms (baseline and advanced), a justified train/test split, robust evaluation and model interpretability.
- **Prescriptive analytics** with concrete recommendations citing numerical findings from all three previous layers and clearly labeling any business assumptions.
- **An interactive Streamlit dashboard** that exposes the analysis, model comparisons and prioritized recommendations.
- **At least six different chart types**, each with a title, axis labels, legend when relevant and one or two accurate sentences of interpretation.
- Python source/notebooks that run from a clean environment and meaningful automated tests.

**Dataset limitation:** IBM says its Telco data describe a fictional sample telecommunications company. You must explicitly disclose this, and must not claim the findings represent verified real operations or that recommendations have measured causal business impact.

## Engineering expectations

Use your own judgment to select a suitably simple, modular architecture. Prioritize correct analysis, clean code, low coupling, consistent model preprocessing, robust validation, readable figures and testable functionality. Avoid excessive hardcoding, a monolithic UI script, duplicated business calculations, fabricated results, and unnecessary infrastructure.

Do not deliberately degrade a baseline to make an advanced model look better. The baseline and advanced candidates must be trained and compared fairly. Do not optimize on the final test set or leak target information into predictors.

Do not blindly reproduce numbers shown in the reference repository. Only computed and verified local results belong in this project.

## Workflow and checkpoints

Start at **Phase 0** in `02_PROJECT_IMPLEMENTATION_SPEC.md`. Inspect the workspace, dataset and assignment, then create `docs/REQUIREMENTS_TRACEABILITY.md`, `docs/DECISIONS.md` and `docs/PROGRESS.md`. Work phase by phase and execute tests after each meaningful stage.

Continue from analysis through actual implementation, dashboard testing, final verification, and evidence-package export. Do not stop at a plan or project skeleton.

Update `docs/PROGRESS.md` after each completed phase with concrete work performed, commands/tests run, observed results, unresolved issues and the next step. If this session is interrupted, the next agent should be able to resume from that file.

**Ask me before deciding only when a decision is truly material or would violate the assignment, originality constraint, data integrity or project scope.** Otherwise, make defensible decisions, document the rationale and continue.

## Final output package

**Critical:** At the end, generate both:

- `report_evidence_package/`
- `report_evidence_package.zip`

They must contain all factual analysis and visual evidence necessary for a **separate AI assistant** to write the midterm Word report and PowerPoint: data audit, descriptive/diagnostic findings, model comparisons, evaluation and explanation, retention recommendations, screenshot evidence, figure inventory, sources, reproducibility information, and a requirement-to-file manifest.

The package must be accurate and self-contained. Re-run the complete pipeline and verify internal consistency before export. The Word-report assistant should not need to request more outputs because files were omitted.

**Do not generate or modify the Word report, PowerPoint, or video in this task.** I will handle those separately.

## Final response to me

Report:

- Work implemented and why it meets the business objective.
- The status of every official requirement, with evidence paths.
- The actual commands and tests executed (including any failures).
- The exact paths to `report_evidence_package/` and `report_evidence_package.zip`.
- Known limitations and anything still requiring my decision or action.

Never claim completion if a core requirement remains unimplemented, the app has not run, the analyses were not regenerated, or the evidence ZIP was not opened and validated.

**Begin Phase 0 now.**
