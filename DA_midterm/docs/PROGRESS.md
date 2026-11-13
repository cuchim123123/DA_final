# Project Progress Log (`PROGRESS.md`)

**Project:** Telco Customer Churn Analytics (Midterm Project)  
**Target Directory:** `f:\Desktop\DA_final\DA_midterm\`  
**Last Updated:** 2026-11-10 19:08 (+07:00)

---

## Current Status Summary
- **All Phases (0 through 7) COMPLETED.**
- **Validation Status:** `ruff check src app tests` passed (`0` issues); `python -m telco_churn.cli run-all` and `python -m telco_churn.cli export-package` executed cleanly; `pytest -v` passed all **9/9** automated tests; 4 live Streamlit view screenshots verified via headless Edge CDP; `report_evidence_package/` (`58` files) and `report_evidence_package.zip` (`3,991,000` bytes) validated for internal consistency and relative-path portability.
- **Assignment Verification Note:** Raw `De KT giua ky_HK1_NH26-27(1).docx` file was not present in the workspace; requirements are verified against `TELCO_CHURN_MIDTERM_AGENT_PACK/01_OFFICIAL_REQUIREMENTS_EN.md` and student identity / team contribution fields / separate report & slides are explicitly reserved for the student and report-writing assistant.

---

## Completed Phases

### Phase 0: Requirements Analysis, Dataset Inspection & Architecture Planning — COMPLETED
- Audited pack & inspected IBM CSV schema in memory (`7,043 x 21`), created `REQUIREMENTS_TRACEABILITY.md`, `DECISIONS.md`, `ARCHITECTURE.md`, and `PROGRESS.md`.

### Phase 1: Data Source, Cryptographic Provenance & Schema Integrity — COMPLETED
- Acquired official IBM CSV (`970,457` bytes, SHA-256 `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`), persisted `data/raw/provenance.json`, audited `11` `TotalCharges` blanks (`tenure == 0`, `Churn == "No"`), `0` exact duplicates (`22` matching non-ID profiles retained), and `0` service-hierarchy errors.

### Phase 2: Descriptive & Diagnostic Analytics + 6 Chart Types — COMPLETED
- Implemented `descriptive.py`, `diagnostic.py`, `charts.py`: `26.54%` churn (`1,869 / 7,043`), `$139,130.85/mo` (`30.50%`) revenue at risk, top Cramér's $V$ (`Contract` `0.4101`, `tenure_tier` `0.3512`, `OnlineSecurity` `0.3474`, `TechSupport` `0.3429`), Mann-Whitney U (`tenure r_rb = -0.4797`), confounding reversal on `TotalCharges`, and `fig01`–`fig06` (Bar+CI, Histogram+KDE, Boxplot, Split Violin, Hexbin Scatter, Heatmaps).

### Phase 3: Predictive Modeling, Calibration & Explainability — COMPLETED
- Stratified 80/20 split (`5,634` train / `1,409` test, `26.54%` churn balanced).
- Stratified 5-fold CV benchmark: `Dummy Floor` (`ROC-AUC 0.5000`), `Logistic Regression` (`0.8458` CV / `0.8412` Test), `Random Forest` (Champion, `0.8480` CV / `0.8440` Test, `Brier 0.1361`, `Recall 74.60%` & `F1 0.6392` at CV-selected `tau = 0.33`), `HistGradientBoosting` (`0.8471` CV / `0.8461` Test, `PR-AUC 0.6610`).
- Raw-column test permutation importance & logistic log-odds + `fig07`–`fig09`.

### Phase 4: Prescriptive Analytics & Unified CLI — COMPLETED
- Held-out risk tiers (`Tier 1`: `67.27%` realized churn, capturing `49.47%` of churners), top-30% outreach capture (`65.78%` recall at `2.19x` lift), 18-point scenario sensitivity matrix, traceable `REC-1`–`REC-4`, and `fig10`.

### Phase 5: Interactive Streamlit Dashboard — COMPLETED
- Implemented 4-view light-theme Streamlit dashboard (`app/helpers.py`, `app/streamlit_app.py`, `.streamlit/config.toml`) tested with `AppTest` and captured live across all 4 views via headless Edge CDP (`outputs/dashboard_screenshots/01_overview.png`–`04_prescriptive_retention.png`).

### Phase 6 & 7: Full Quality Audit, Evidence Export & ZIP Verification — COMPLETED (Including Post-Audit Revisions)
- Implemented `src/telco_churn/reporting/guide_builders.py` and `evidence_exporter.py`.
- Resolved all findings from `TELCO_MIDTERM_EVIDENCE_AUDIT.md`:
  - **Issue 1 (`REC-2`):** Computed `descriptive_compound_segments.csv` and narrowed `REC-2` to exact intersected `Fiber optic AND (No OnlineSecurity OR No TechSupport)` (`n = 2,722`, `45.70%` churn, `1,244` churners = `66.56%` of total churn, `$108,733.60/mo` historical churned billing) while explicitly contrasting broad Fiber (`n = 3,096`), neither add-on (`n = 1,765`, `55.01%`), and both add-ons (`n = 374`, `14.17%`).
  - **Issue 2 (`REC-4` vs `REC-5`):** Split probability threshold triage (`REC-4`: `p >= 0.33`, `499 / 1,409 = 35.42%` test accounts) from capacity-constrained queue targeting (`REC-5`: Top `30%`, `423 / 1,409 = 30.02%`, `p >= 0.3918`, `65.78%` capture, `2.19x` lift), removing any ambiguous full-sample extrapolation claim on `2,113`.
  - **Issue 3 (HistGradientBoosting Threshold):** Corrected `evaluate.py` so each classifier evaluates its own CV F1-optimal threshold (`Logistic Regression = 0.325`, `Random Forest = 0.330`, `HistGradientBoosting = 0.340`) without using test data.
  - **Issue 4 & 5 (Revenue Language & Fictional Caveat):** Standardized `$139,130.85/mo` and segment amounts as historical monthly billing among churned snapshot records across UI, guides, and recommendations.
- Exported self-contained `report_evidence_package/` (`59` files including `descriptive_compound_segments.csv`) and `report_evidence_package.zip`.
