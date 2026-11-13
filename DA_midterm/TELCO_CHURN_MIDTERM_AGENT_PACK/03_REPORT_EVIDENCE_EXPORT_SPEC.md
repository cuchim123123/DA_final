# Specification: Self-Contained Midterm Report Evidence Package

## Objective

At the end of the Telco Churn project, produce **one portable folder and one ZIP** that another AI assistant can use to write an academically accurate **nine-section midterm report** and PowerPoint without asking the coding agent for additional analysis outputs.

Required paths at project root:

```
report_evidence_package/
report_evidence_package.zip
```

The ZIP must contain the same directory tree. **Do not write the report or create slides in this task.** This is a transfer package of computed evidence, graphs, methods, interpretations and screenshots.

## Required logical structure

The directory names below are suggested and can be adjusted for clarity, but every information category is mandatory:

```
report_evidence_package/
  README_START_HERE.md
  EVIDENCE_MANIFEST.md
  REQUIREMENTS_COVERAGE.md
  RESULTS_AND_INTERPRETATION_GUIDE.md
  HOW_TO_REPRODUCE.md
  SOURCES_AND_LIMITATIONS.md
  00_dataset_and_quality/
    dataset_overview.json
    schema_dictionary.csv
    data_quality_audit.csv
    preprocessing_decisions.md
    raw_dataset_source.txt
    dataset_sha256.txt
  01_descriptive/
    tables/
    figures/
    findings.md
  02_diagnostic/
    tables/
    figures/
    findings.md
  03_predictive/
    tables/
    figures/
    split_and_validation.md
    model_specification.md
    explanation_and_limitations.md
  04_prescriptive/
    tables/
    figures/
    recommendations_with_evidence.md
    assumptions_and_sensitivity.md
  05_dashboard/
    screenshots/
    walkthrough.md
    filters_and_interactions.md
  06_references_and_report_helpers/
    chart_inventory.csv
    table_inventory.csv
    key_findings.json
    citations.md
    suggested_report_section_mapping.md
```

If the same figure is relevant to more than one section, store a single canonical file and reference it by a relative path from the manifest. Avoid unnecessary duplicate image files.

## 1. Cover and navigation files

### `README_START_HERE.md`

Briefly explain the project, data provenance, four analytical layers, how to interpret the package, where to find tables/figures and what is not claimed. State clearly that IBM's Telco data are from a **fictional sample company**, rather than verified operational churn records.

### `EVIDENCE_MANIFEST.md`

For every output, include: relative path, originating analysis step, purpose, associated requirement, validation status and any important caveat. Every referenced file must actually exist in the ZIP.

### `REQUIREMENTS_COVERAGE.md`

Map each official midterm requirement to output artifacts and validation, including:

- 9 report sections (content evidence only)
- runnable Python project (point to project-level commands and verification)
- interactive dashboard (screenshots, run guide, tested interactions)
- 6 different chart types (name all six and link their images)
- chart titles/axes/legends/one-to-two-sentence interpretations
- at least 2 predictive algorithms (train/test metrics, protocol)
- train/test split rationale
- interpretability result
- prescriptive recommendations with **specific numerical evidence from descriptive, diagnostic and predictive layers**

Explicitly mark any item incomplete or blocked; do not claim 100% if anything is missing.

### `RESULTS_AND_INTERPRETATION_GUIDE.md`

This is the **main source for the report-writing AI**. It must have substantive, coherent prose, not a notebook dump. For each analytical layer, provide:

- research questions and business relevance
- methods actually implemented and why they were chosen
- major computed results, with units, denominators and appropriate precision
- exact references to supporting CSV/JSON tables and figure filenames
- statistical interpretation and potential alternative explanations
- limits, assumptions and distinctions between evidence and conjecture
- suggested cross-references for the nine report sections

No hardcoded claims that could diverge from current calculated results. Generate or validate quantitative statements from the fresh execution outputs; manually authored prose must be numerically checked.

## 2. Data and audit evidence

Export original dataset identification, SHA-256, source URL, access date, full schema, inferred/declared types, definition of target, rows, duplicates, missing/invalid values and cleaning treatment. List exclusions and justify them. If a dataset copy is bundled, retain its provenance and license; original code and dashboard must still work without proprietary data access.

If the project uses a cleaned copy, identify precisely which changes were applied to original rows. The report assistant should not need to inspect source code to explain those changes.

## 3. Descriptive analytics evidence

Export headline KPIs, group counts and churn rates, subgroup tables and charts that show the population composition and observed patterns. Provide exact descriptive findings (including subgroup denominators) and avoid mixing raw rates with model-predicted probabilities.

## 4. Diagnostic analytics evidence

Export cross-tabulation or statistical association tables, selected effect sizes and appropriate comparisons. Include method notes and limitations. The report assistant must be able to explain why certain characteristics are *associated with* churn without claiming experimentally established causation.

## 5. Predictive analytics evidence

At minimum, export:

- raw class distribution and split sizes, seed, holdout strategy and why this split was selected
- training-only model selection and cross-validation settings/results
- comparable baseline versus advanced model metrics on held-out data: accuracy, precision, recall, F1, ROC-AUC, and PR-AUC if used
- model confusion matrices with actual counts and orientation labels
- ROC and PR figure(s), calibration plots if probabilities are shown
- chosen threshold and documented validation-only selection method
- model coefficients/feature importance/SHAP and definitions of each encoded feature
- test-set predictions/labels/probabilities **only as necessary to independently verify metrics**, with fictional IDs avoided or anonymized
- honest assessment of what the trained model can and cannot predict

Do not reuse metrics from another GitHub repository. Do not relabel training performance as test performance. If outputs indicate performance is poor, report it accurately.

## 6. Prescriptive evidence

Provide a traceable recommendations table with, for each proposed action:

- eligible segment and estimated segment size
- specific descriptive evidence (count/rate)
- specific diagnostic evidence (comparison/association)
- specific predictive evidence (risk score distribution, precision, recall, model uncertainty or capacity metric)
- proposed action and operational cost/effort assumptions
- uncertainty or reason the action may not work
- corresponding exact evidence paths

There must be at least one defensible overall recommendation and enough information for the report writer to refer concretely to the previous three layers. More recommendations are not necessarily better.

If modeling budget, intervention uplift or ROI, keep inputs labeled as user-adjustable **scenario assumptions**, not outcomes observed in the dataset. Include sensitivity results and avoid fictional savings presented as empirical facts.

## 7. Dashboard evidence

Provide full-resolution screenshots of the actual running app (not mocked illustrations) that show:

- Overview/KPIs
- diagnostic exploration and working filters
- test-set model comparison and interpretability
- retention-prioritization panel and relevant assumptions

Document the local launch command, dashboard pages, filter behavior, model loading behavior, and any control that changes the interpretation of results. No personal identifiers should appear unnecessarily in screenshots.

## 8. Chart inventory

Maintain `chart_inventory.csv` with one row per figure and at least these columns:

`figure_id,relative_path,chart_type,section,variables,title,axis_labels,legend_applicable,interpretation_1,interpretation_2,source_table,verification_status`

Identify at least **six distinct chart types**. If a chart is purely supplementary, label it as such. In the report guide, include one or two *accurate* explanatory sentences per chart, as the instructor explicitly requires.

## 9. References and report mapping

`citations.md` should provide source links for the IBM dataset and relevant statistical/ML libraries or methodological references. Cite the inspiration repo only as an external project consulted at a high level, if consulted. Do not claim its results are yours.

`suggested_report_section_mapping.md` should map evidence to:

1. Introduction
2. Dataset
3. Descriptive Analytics
4. Diagnostic Analytics
5. Predictive Analytics
6. Prescriptive Analytics
7. Conclusion
8. Team Contributions (placeholder only; real members supplied by user)
9. References

Provide concise guidance on how to select the clearest figures for slides and avoid overcrowding. **Do not draft the actual report, assign invented group members, or create slides.**

## 10. Artifact validation and export tests

Implement a repeatable exporter and run it only after all analyses have been regenerated. Validate at least:

1. Every path in the manifest is relative and exists in the package.
2. All required CSV and JSON outputs parse and contain expected schema and non-empty content where applicable.
3. All PNG/SVG figures open and have readable titles/labels at report and slide size.
4. Every quantitative conclusion in the guide agrees with its cited data table, including units and denominators.
5. Model metrics recomputed from exported test predictions match the exported metrics within justified tolerance.
6. The chart inventory contains six genuine chart types and matches the actual figures.
7. Every prescribed action cites real values from preceding analytics and labels assumptions clearly.
8. The dashboard screenshots were captured from the functional app, not recreated or copied from another repo.
9. The ZIP file opens, reproduces the same directory tree, and does not contain broken links, virtual environments, caches, developer-local absolute paths or unrelated artifacts.
10. A fresh reader can understand and write the report **without browsing the original source code**.

**Output acceptance:** `report_evidence_package/` and `report_evidence_package.zip` must exist and pass the automated validation. The agent should report exact export paths, number of tables and plots, dashboard test results, and any unresolved discrepancies. Do not mark completion until the ZIP has been opened and checked.
