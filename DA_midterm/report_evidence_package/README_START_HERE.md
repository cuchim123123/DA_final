# Telco Customer Churn Analytics — Report Evidence Package

## Start Here (Instructions for the Academic Report & Slide Assistant)
This self-contained package contains every table, chart, statistical test result, trained model comparison, explainability ranking, prescriptive prioritization policy, and live dashboard screenshot needed to author the **nine-section midterm report** and accompanying presentation slides without inspecting source code.

## Important Provenance & Scope Disclosure
- **Dataset:** IBM public *Telco Customer Churn* sample (`Telco-Customer-Churn.csv`, `7,043` rows x `21` columns, SHA-256 `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`).
- **Source URL:** `https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv`
- **Official IBM Caveat:** IBM explicitly identifies this sample as representing a **fictional telecommunications company** cross-sectional snapshot (`Churn` = left within the last month). Do **not** describe these records as verified live carrier financial logs, prospective cohort timelines, or experimentally verified causal effects.
- **Billing Exposure Proxy Clarification:** Monetary figures labeled `monthly_revenue_at_risk_usd` (headline **`$139,130.85/month`**) represent the sum of current `MonthlyCharges` across customers labeled `Churn = Yes` in the cross-sectional snapshot. This is a **historical billing-exposure proxy**, NOT measured future lost revenue or verified retention savings.
- **Unresolved User Placeholders:** Group member names, student IDs, individual contribution percentages, and slide/report authorship must be supplied by the student for Report Section 8 (*Team Contributions*).

## Directory Navigation
- `RESULTS_AND_INTERPRETATION_GUIDE.md` — Primary authoritative narrative with exact computed statistics, denominators, interpretations, and limitations across all 4 analytical layers.
- `EVIDENCE_MANIFEST.md` — Complete file-by-file inventory with relative paths, origins, and validation status.
- `REQUIREMENTS_COVERAGE.md` — 1:1 traceability against official midterm requirements `M-01` through `M-10`.
- `00_dataset_and_quality/` — Dataset overview JSON, 21-column schema dictionary, quality audit (`11` `TotalCharges` blanks at `tenure=0`, `0` exact duplicates), SHA-256, and preprocessing decisions.
- `01_descriptive/` — Descriptive KPIs, subgroup & compound intersected cohort rates with 95% Wilson CIs, and `fig01`–`fig03`.
- `02_diagnostic/` — Chi-square/Cramer's V tests, Mann-Whitney U comparisons, confounding reversal audit, and `fig04`–`fig06`.
- `03_predictive/` — Stratified 80/20 split logs, 5-fold CV & sealed test benchmarks (`Dummy`, `Logistic Regression`, `Random Forest`, `HistGradientBoosting`) with each model's CV-selected cutoff (`0.325`/`0.330`/`0.340`), explainability tables, and `fig07`–`fig09`.
- `04_prescriptive/` — Held-out risk tiers, capacity lift table, 18-cell assumption sensitivity grid, traceable recommendations `REC-1`–`REC-5` (cleanly separating threshold cutoff vs top-30% budget queue policies), and `fig10`.
- `05_dashboard/` — Live Edge-CDP screenshots of all 4 Streamlit views (`01_overview.png`–`04_prescriptive_retention.png`) and UI walkthrough.
- `06_references_and_report_helpers/` — `chart_inventory.csv` (`10` figures across `>6` genuinely distinct chart types), `table_inventory.csv`, `key_findings.json`, verified `citations.md`, and 9-section report mapping.
