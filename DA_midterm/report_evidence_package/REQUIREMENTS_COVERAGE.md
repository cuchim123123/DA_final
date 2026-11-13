# Official Midterm Requirements Coverage (`M-01` to `M-10`)

**Source Authority Note:** Evaluated against `TELCO_CHURN_MIDTERM_AGENT_PACK/01_OFFICIAL_REQUIREMENTS_EN.md`. Note that the raw binary Vietnamese handout `.docx` was absent from the workspace and is flagged for user confirmation alongside student identity/team contribution placeholders.

| ID | Official Requirement | Package Evidence Paths | Validation Status |
|---|---|---|---|
| **M-01** | Word-report-ready evidence for all 9 sections (without generating `.docx`) | `RESULTS_AND_INTERPRETATION_GUIDE.md`<br>`06_references_and_report_helpers/suggested_report_section_mapping.md` | **COVERED (Sections 1-7, 9); Sec 8 Placeholder for User Team Roster** |
| **M-02** | Presentation-ready visual evidence and dashboard screenshots (without `.pptx`) | `01_descriptive/figures/` through `04_prescriptive/figures/`<br>`05_dashboard/screenshots/01_overview.png`–`04_prescriptive_retention.png` | **VERIFIED** (10 figures + 4 live screenshots) |
| **M-03** | Runnable and explained Python code (`src/`, `app/`, CLI, tests) | `HOW_TO_REPRODUCE.md` | **VERIFIED** (`python -m telco_churn.cli run-all`, `pytest`, `ruff`) |
| **M-04** | At least one working interactive dashboard (tested live) | `05_dashboard/walkthrough.md`<br>`05_dashboard/filters_and_interactions.md`<br>`05_dashboard/screenshots/*.png` | **VERIFIED** (`AppTest` + 4 live Edge CDP screenshots) |
| **M-05** | At least 6 genuinely different chart types with title, axes, legend & 1-2 interpretation sentences | `06_references_and_report_helpers/chart_inventory.csv` (**10 distinct chart types**) | **VERIFIED** |
| **M-06** | Compare >= 2 predictive algorithms (baseline vs advanced) | `03_predictive/tables/model_cv_comparison.csv`<br>`03_predictive/tables/model_test_comparison.csv` | **VERIFIED** (Logistic Regression baseline vs Random Forest & HistGradientBoosting + Dummy floor) |
| **M-07** | Justified train/test split strategy | `03_predictive/split_and_validation.md`<br>`03_predictive/tables/split_class_balance.csv` | **VERIFIED** (Stratified 80/20 cross-sectional split, seed=42) |
| **M-08** | Model explainability technique | `03_predictive/explanation_and_limitations.md`<br>`03_predictive/tables/permutation_importance.csv`<br>`03_predictive/tables/logistic_odds_ratios.csv`<br>`03_predictive/figures/fig09_model_explainability.png` | **VERIFIED** (Champion `Random Forest` permutation + Log-Odds) |
| **M-09** | Prescriptive recommendations citing concrete numbers from all 3 prior layers | `04_prescriptive/recommendations_with_evidence.md`<br>`04_prescriptive/tables/prescriptive_recommendations.csv`<br>`04_prescriptive/assumptions_and_sensitivity.md` | **VERIFIED** (`REC-1`–`REC-5` + sensitivity grid) |
| **M-10** | Clear provenance, data audit, non-duplication from DA_final & verified ZIP | `00_dataset_and_quality/*` (`SHA-256` & caveat)<br>`EVIDENCE_MANIFEST.md` | **VERIFIED** |
