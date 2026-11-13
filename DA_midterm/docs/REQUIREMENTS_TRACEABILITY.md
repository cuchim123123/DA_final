# Requirements Traceability Matrix (`REQUIREMENTS_TRACEABILITY.md`)

## 1. Assignment Authority & Eligibility Audit

- **Primary Authority:** Official Midterm Assignment (`De KT giua ky_HK1_NH26-27(1).docx`), reproduced in English in [`TELCO_CHURN_MIDTERM_AGENT_PACK/01_OFFICIAL_REQUIREMENTS_EN.md`](../TELCO_CHURN_MIDTERM_AGENT_PACK/01_OFFICIAL_REQUIREMENTS_EN.md).
  - *Audit Note:* The raw `.docx` binary is not present in `DA_midterm/`. This traceability matrix verifies compliance against `01_OFFICIAL_REQUIREMENTS_EN.md` and preserves Section 8 (*Team Contributions*) and final Word/slide authoring for the student and report assistant.
- **Topic & Dataset Selection:** **Telco Customer Churn Analytics**, IBM sample `Telco-Customer-Churn.csv` (`7,043` rows $\times$ `21` columns, SHA-256 `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`).
- **Topic Non-Overlap:** Completely distinct from `DA_final` (UCI Bike Sharing `day.csv`).
- **Originality Policy:** 100% clean-room Python implementation; zero code, pre-trained models, charts, or metrics copied from `UtkarshRai-ds/telco-churn-prediction`.
- **Provenance Caveat:** Sample data represents a **fictional telecommunications company** snapshot (`Churn` = left within last month); observational patterns and predictive probabilities do not establish causality.

---

## 2. Official Requirements Verification Matrix (`M-01` to `M-10`)

| Req ID | Official Requirement | Implementing Module(s) | Exported Evidence & Artifacts | Verification Method | Status |
|---|---|---|---|---|---|
| **M-01** | Word-report-ready evidence for 9 sections *(without generating `.docx`)* | `src/telco_churn/reporting/guide_builders.py`<br>`src/telco_churn/reporting/evidence_exporter.py` | `report_evidence_package/RESULTS_AND_INTERPRETATION_GUIDE.md`<br>`report_evidence_package/06_references_and_report_helpers/suggested_report_section_mapping.md` | Cross-check of statistics against CSV/JSON sources (`tests/test_evidence_package.py`) | **VERIFIED** *(Sec. 8 team roster reserved for user)* |
| **M-02** | Presentation-ready visual evidence *(without generating `.pptx`)* | `src/telco_churn/analysis/charts.py`<br>`src/telco_churn/modeling/evaluate.py`<br>`src/telco_churn/modeling/explain.py` | `outputs/figures/fig01`–`fig10` (300 DPI)<br>`outputs/dashboard_screenshots/01`–`04.png` | `PIL.Image.verify()`, resolution audit, visual review | **VERIFIED** |
| **M-03** | Runnable and explained Python code | `pyproject.toml`, `requirements.txt`<br>`src/telco_churn/cli.py`<br>`README.md` | `python -m telco_churn.cli run-all`<br>`python -m telco_churn.cli export-package` | Full clean reproduction, `ruff check`, `pytest -v` | **VERIFIED** |
| **M-04** | Interactive Streamlit dashboard | `app/helpers.py`<br>`app/streamlit_app.py`<br>`.streamlit/config.toml` | 4 views (`Overview`, `Explore & Diagnose`, `Predictive`, `Prescriptive`) + screenshots | `tests/test_prescriptive_and_app_helpers.py` (`AppTest`) + live Edge CDP capture | **VERIFIED** |
| **M-05** | At least 6 different chart types with titles, axes, legends & 1-2 interpretation sentences | `analysis/charts.py`, `modeling/evaluate.py`, `modeling/explain.py`, `recommendations/prescriptive.py` | `chart_inventory.csv` (10 charts across >6 distinct chart types: Bar+CI, Hist+KDE, Boxplot, Split Violin, Hexbin Scatter, Heatmaps, ROC/PR/Calibration Curves, Error/Diverging Bars, Cumulative Gain Curve) | Automated check in `validate_evidence_package()` + `test_evidence_package.py` | **VERIFIED** |
| **M-06** | Compare $\ge 2$ predictive algorithms (simple baseline vs advanced) | `src/telco_churn/modeling/train.py`<br>`src/telco_churn/modeling/evaluate.py` | `model_cv_comparison.csv`, `model_test_comparison.csv`, `test_predictions.csv`, `champion_pipeline.joblib` | Fair Stratified 5-Fold CV + test metric recomputation from `test_predictions.csv` | **VERIFIED** |
| **M-07** | Justify train/test split strategy | `src/telco_churn/modeling/split.py` | `split_class_balance.csv`, `split_and_validation.md` | `test_split_isolation_and_no_leakage` (0 ID overlap, `26.54%` stratified balance) | **VERIFIED** |
| **M-08** | Model explainability technique | `src/telco_churn/modeling/explain.py` | `permutation_importance.csv`, `logistic_odds_ratios.csv`, `fig09_model_explainability.png`, `explanation_and_limitations.md` | Raw-column 30-repeat test permutation across all 19 features + Logistic log-odds | **VERIFIED** |
| **M-09** | Prescriptive recommendations citing concrete numbers from all 3 prior layers | `src/telco_churn/recommendations/prescriptive.py` | `prescriptive_recommendations.csv` (`REC-1`–`REC-5`), `descriptive_compound_segments.csv`, `prescriptive_risk_tiers.csv`, `prescriptive_capacity_lift.csv`, `prescriptive_scenario_sensitivity.csv`, `fig10` | `test_dashboard_helpers_filtering_scoring_and_scenarios` (`REC-2` n=2,722; `REC-4` n=499; `REC-5` n=423) | **VERIFIED** |
| **M-10** | Clear provenance, data quality audit & verified ZIP package | `src/telco_churn/data/ingest.py`, `validate.py`, `reporting/evidence_exporter.py` | `report_evidence_package/` (`59` files), `report_evidence_package.zip` | `test_acquire_and_checksum`, `test_schema_dimensions_and_quality_audit`, `test_evidence_package.py` | **VERIFIED** |
