# Architecture & Analysis Blueprint (`ARCHITECTURE.md`)

## 1. Directory Layout (`f:\Desktop\DA_final\DA_midterm\`)

```text
DA_midterm/
├── pyproject.toml
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── raw/
│       ├── Telco-Customer-Churn.csv          # Untouched IBM canonical dataset (SHA-256 verified)
│       └── provenance.json                   # Download URL, access timestamp, SHA-256, schema hash
├── src/
│   └── telco_churn/
│       ├── __init__.py
│       ├── config.py                         # Authoritative paths, random seeds, schema definitions, column groups
│       ├── data/
│       │   ├── __init__.py
│       │   ├── ingest.py                     # Download/load IBM CSV, verify SHA-256, write provenance
│       │   └── validate.py                   # Schema, missingness, TotalCharges parsing, duplicate & service hierarchy audit
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── descriptive.py                # KPIs, numeric quantiles, subgroup counts/rates + 95% Wilson CIs
│       │   ├── diagnostic.py                 # Chi-square, Cramer's V, Mann-Whitney U, Welch t, multivariable confounding check
│       │   └── charts.py                     # Descriptive & diagnostic 300-DPI figures (Bar, Hist+KDE, Boxplot, Violin, Scatter, Heatmap)
│       ├── modeling/
│       │   ├── __init__.py
│       │   ├── split.py                      # Stratified 80/20 split with overlap & balance assertions
│       │   ├── pipeline.py                   # Leak-free ColumnTransformer (Median imputer, Scaler, OneHotEncoder) + input validator
│       │   ├── train.py                      # Dummy floor + CV-tuned LogisticRegression, RandomForest, HistGradientBoosting + Calibration check
│       │   ├── evaluate.py                   # Validation threshold selection + single-use test metrics + confusion matrices + ROC/PR plots
│       │   └── explain.py                    # Raw-column permutation importance + Logistic odds ratios + explanation figures
│       ├── recommendations/
│       │   ├── __init__.py
│       │   └── prescriptive.py               # Risk-tier bucketing, capacity lift curve, evidence-linked recommendations & sensitivity grid
│       ├── reporting/
│       │   ├── __init__.py
│       │   └── evidence_exporter.py          # Repeatable report_evidence_package/ + ZIP exporter + internal consistency validator
│       └── cli.py                            # End-to-end CLI entrypoint (`python -m telco_churn.cli run-all`)
├── app/
│   ├── __init__.py
│   ├── helpers.py                            # Pure testable UI data loaders, filter helpers, scenario calculator, single-customer validation
│   └── streamlit_app.py                      # 4-view interactive Streamlit application (Overview, Explore & Diagnose, Models & Explainability, Prescriptive Prioritization)
├── tests/
│   ├── test_data_integrity.py
│   ├── test_analysis_layers.py
│   ├── test_modeling_and_leakage.py
│   ├── test_prescriptive_and_app_helpers.py
│   └── test_evidence_package.py
├── outputs/
│   ├── dataset_overview.json
│   ├── results_summary.json
│   ├── tables/
│   ├── figures/
│   ├── models/
│   └── dashboard_screenshots/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DECISIONS.md
│   ├── PROGRESS.md
│   └── REQUIREMENTS_TRACEABILITY.md
├── report_evidence_package/
└── report_evidence_package.zip
```

## 2. Analytical Pipeline Data Flow

1. **Ingest & Audit (`Phase 1`):** Download/load `data/raw/Telco-Customer-Churn.csv`, verify SHA-256, validate all 21 columns, parse `TotalCharges` cleanly (`11` blank entries mapped to `NaN` in EDA audit, imputed strictly on training folds in ML), verify service hierarchy and `22` non-ID identical feature rows, export `outputs/dataset_overview.json` & `outputs/tables/data_quality_audit.csv`.
2. **Descriptive & Diagnostic Layers (`Phase 2`):** Compute segment counts/rates with 95% Wilson CIs, distributional quantiles, Chi-square / Cramér's $V$, Mann-Whitney $U$ / rank-biserial correlations, adjusted vs. unadjusted odds ratios (confounding demonstration), and Figures `fig01`–`fig06`.
3. **Predictive Layer (`Phase 3`):** Stratified 80/20 split (`seed = 42`, `5,634` train / `1,409` test). Run Stratified 5-Fold CV for `LogisticRegression`, `RandomForestClassifier`, and `HistGradientBoostingClassifier` (plus `DummyClassifier` floor). Select champion model and decision threshold strictly on training out-of-fold validation predictions; evaluate calibration and fit reliability; run a single final evaluation on `X_test, y_test`; save `champion_pipeline.joblib`, `test_predictions.csv`, metrics tables, Figures `fig07`–`fig09`.
4. **Prescriptive Layer (`Phase 4`):** Score and tier segments using calibrated test probabilities; compute capacity-constrained cumulative capture/lift table; generate evidence-linked strategic recommendations citing exact Descriptive, Diagnostic, and Predictive statistics; compute scenario assumptions & sensitivity matrix + `fig10`.
5. **Interactive Streamlit Dashboard (`Phase 5`):** Build modular 4-section Streamlit app reading directly from precomputed tables + fitted `champion_pipeline.joblib` (zero retraining on filter change; enforces service-hierarchy rules in hypothetical scoring form; separates observed statistics from labeled scenario assumptions). Test via `AppTest` / helper unit tests and headless Edge/Chrome screenshot verification.
6. **Full Audit (`Phase 6`):** Execute clean `python -m telco_churn.cli run-all`, `pytest`, `ruff check`, inspect screenshots and plots visually via `read_file`, verify all requirement checks (`M-01`–`M-10`).
7. **Evidence Export & Validation (`Phase 7`):** Populate `report_evidence_package/`, generate comprehensive `RESULTS_AND_INTERPRETATION_GUIDE.md`, `EVIDENCE_MANIFEST.md`, `REQUIREMENTS_COVERAGE.md`, `chart_inventory.csv`, and `report_evidence_package.zip`; run full standalone ZIP and number-consistency audit.
