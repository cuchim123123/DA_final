# Midterm Assignment: Authoritative Requirements in English

**Course:** Data Analysis and Visualization, Semester 1, Academic Year 2026–2027.

**Source:** `De KT giua ky_HK1_NH26-27(1).docx` supplied by the student. This document reproduces the official general instructions in English. It distinguishes *explicit instructor requirements* from the project design choices, which appear in the next document.

## A. Mandatory submission products

The original assignment requires:

1. **Word report** containing **nine sections**: Introduction; Dataset; four layers of analysis; Conclusion; Team Contributions; References.
2. **Presentation slides.**
3. **Runnable source code or notebook** (`.ipynb` or `.py`), with comments explaining each step.
4. **At least one interactive dashboard**, implemented in Power BI, Tableau or Python.

The report/slides will be prepared later by the student and another assistant. The coding agent **must still prepare all supporting evidence** required for these deliverables. It must implement and demonstrate the interactive dashboard.

## B. Mandatory technical standards

- **At least six different chart types** across the report. Repeated charts of one kind do not count as different types.
- **Each chart must have:** a title, axis labels, a legend when multiple groups are displayed, and **one or two accompanying sentences of interpretation**.
- **Predictive modeling must compare at least two algorithms:** one simple baseline and one more advanced model.
- **Explain the train/test split:** including why random or time-based splitting was used.
- **Include at least one model explainability technique:** feature importance, regression coefficients, SHAP, etc.
- **Prescriptive analytics recommendations must cite specific numbers/findings from each of the three preceding analytical layers.** Generic recommendations are insufficient.

These points come directly from page 1 of the original assignment. The suggested topics listed on the remaining pages are **suggestions**, not the exclusive allowable choices. The student has explicitly chosen Telco Customer Churn instead.

## C. Report sections and the four analytical layers

The original document explicitly calls for 'four layers of analysis' and a nine-section report, but does not prescribe a particular library, dashboard layout, algorithm family, or exact column names. The standard and appropriate mapping used for this project is:

1. Introduction
2. Dataset
3. Descriptive Analytics: **What patterns are observed?**
4. Diagnostic Analytics: **Which variables are associated with churn?**
5. Predictive Analytics: **Which customers are predicted to be at risk, with what uncertainty and error rates?**
6. Prescriptive Analytics: **What should a retention team prioritize, supported by measurable evidence and qualified assumptions?**
7. Conclusion
8. Team Contributions
9. References

This mapping is a **project design interpretation** of the four layers, not a verbatim official enumeration in the file. Ask the student if an instructor provides a different definition.

## D. Dataset and choice of project

**Chosen dataset:** IBM Telco Customer Churn sample. The commonly used file contains **7,043 rows and 21 original columns** (including the customer identifier and target). These are dataset facts to verify locally, not assumptions to hardcode into analyses.

**Important:** IBM describes its sample as a *fictional telecommunications company*. This is an established public educational dataset, not a longitudinal dataset of verified live business transactions. Represent scope and limitations accurately. The original midterm instructions do not impose a separate requirement that the data must come from actual commercial operations.

**Reference repository:** `UtkarshRai-ds/telco-churn-prediction`. This is not a sanctioned submission template. It is an optional inspiration source. The published README describes a known fresh-environment feature-engineering issue; therefore, its existence does not prove that its implementation is production-ready.

## E. Traceability checklist for agent acceptance

| ID | Requirement | Required evidence |
|---|---|---|
| M-01 | Word-report-ready evidence for nine sections | Clear results, interpretations and sources; do not generate the Word report |
| M-02 | Presentation-ready evidence | Legible figures, concise factual key findings and dashboard screenshots |
| M-03 | Runnable and explained Python code | Clean setup; reproducible CLI/notebook; correct and useful comments |
| M-04 | At least one interactive dashboard | Actual local functional tests; filters/reactions; instructions to run |
| M-05 | Six *different* chart types | Chart-type inventory identifying figure files, variables, titles, labels and one-to-two-sentence interpretation each |
| M-06 | Two or more predictive algorithms | Simple baseline and advanced model fit on comparable data; metrics saved |
| M-07 | Explain split selection | Stratified or time-aware selection documented with justification and validation |
| M-08 | Model explainability | Correct model-specific coefficients/importance/SHAP, graphs and limitations |
| M-09 | Prescriptive proposals backed by preceding three layers | For every recommendation: at least one concrete finding from descriptive, diagnostic and predictive analyses (collectively), with source file references and reasonable assumptions |
| M-10 | Clear data provenance and non-duplicate topic | Original dataset source, citation, checksum and distinction from Bike Sharing |

**Additional engineering checks in the other documents are project quality safeguards, not extra instructor-imposed rubric points.**
