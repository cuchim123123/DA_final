# Telco Customer Churn Analytics — Midterm Project

Clean-room, reproducible Python analytics application covering **Descriptive, Diagnostic, Predictive, and Prescriptive Analytics** plus a four-view **Streamlit Interactive Dashboard**, built on the public IBM **Telco Customer Churn** sample dataset (`7,043` rows $\times$ `21` columns).

> **Provenance & Limitations Notice:** Per IBM's sample documentation, `Telco-Customer-Churn.csv` represents a **fictional telecommunications company** cross-sectional customer snapshot (`Churn` = left within the last month). Statistical associations (`Cramér's V`, `Mann-Whitney U`) and predictive scores (`ROC-AUC`, `Permutation Importance`) do not establish causal treatment effects or live commercial revenue outcomes.

---

## Project Architecture

```text
DA_midterm/
├── data/raw/                   # Canonical IBM CSV (SHA-256 verified) + provenance.json
├── src/telco_churn/
│   ├── config.py               # Authoritative schema, paths, seed, and feature groups
│   ├── data/                   # Acquisition, SHA-256 verification, schema & hierarchy audit
│   ├── analysis/               # Descriptive KPIs (Wilson CIs), diagnostics, & 6 chart types
│   ├── modeling/               # Stratified 80/20 split, leak-free pipelines, CV tuning & explainability
│   ├── recommendations/        # Held-out risk tiers, capacity lift, & assumption sensitivity
│   ├── reporting/              # Portable report_evidence_package/ & ZIP builder + validator
│   └── cli.py                  # Unified CLI (`run-all` and `export-package`)
├── app/
│   ├── helpers.py              # Pure testable cohort filter, threshold scorer & scenario logic
│   └── streamlit_app.py        # Four-view interactive Streamlit application
├── tests/                      # Data, analytics, leakage/recomputation, UI, & package tests
├── outputs/                    # Persisted tables (CSV), 300-DPI figures, models, & screenshots
├── docs/                       # Traceability matrix, decisions log, architecture, & progress log
├── report_evidence_package/    # Self-contained evidence folder for external report authoring
└── report_evidence_package.zip # Verified ZIP transfer archive
```

---

## Setup & Reproduction Commands

Run all commands from the `DA_midterm/` directory:

```powershell
# 1. Create and activate clean virtual environment
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install setuptools wheel
.\.venv\Scripts\python.exe -m pip install -e . --no-build-isolation --no-deps

# 2. Run complete analytical pipeline (data audit -> EDA -> diagnostics -> ML -> prescriptive)
.\.venv\Scripts\python.exe -m telco_churn.cli run-all

# 3. Export & validate self-contained report_evidence_package/ and report_evidence_package.zip
.\.venv\Scripts\python.exe -m telco_churn.cli export-package

# 4. Run linter and full automated test suite
.\.venv\Scripts\python.exe -m ruff check src app tests
.\.venv\Scripts\python.exe -m pytest -v

# 5. Launch interactive Streamlit dashboard
.\.venv\Scripts\streamlit.exe run app/streamlit_app.py
```

---

## Key Analytical Highlights (Verified Grounded Outputs)

1. **Data Quality:** `7,043` unique `customerID`s, `0` exact duplicate rows (`22` matching non-ID discrete profiles retained), and `11` blank `" "` entries in `TotalCharges` (`0.1562%`) occurring exclusively at `tenure == 0` (`Churn == "No"`), parsed cleanly and imputed inside training folds only.
2. **Descriptive & Diagnostic:** Overall churn is `26.54%` (`1,869 / 7,043`, with `$139,130.85/mo` or `30.50%` of monthly billing sitting in churned accounts as a static billing-exposure proxy). Top associations: `Contract` (`Cramér's V = 0.4101`, `42.71%` M2M vs `2.83%` 2-yr), `tenure_tier` (`V = 0.3512`, `47.68%` in 1–12 mo), `OnlineSecurity` (`V = 0.3474`), and `TechSupport` (`V = 0.3429`). Compound fiber cohort `Fiber optic` lacking `OnlineSecurity` or `TechSupport` comprises `n = 2,722` (`45.70%` churn vs `14.17%` with both). Multivariable control demonstrates confounding reversal on `TotalCharges` (`unadjusted log-odds -0.5349 -> adjusted +0.6703`).
3. **Predictive Benchmark (Sealed Hold-Out Test `n = 1,409`):** Using each model's own 5-fold CV F1-optimal cutoff: `Logistic Regression` achieves Test `ROC-AUC = 0.8412` (`PR-AUC = 0.6286`, `tau = 0.325`); `Random Forest` (selected via 5-fold CV `ROC-AUC = 0.8480`) achieves Test `ROC-AUC = 0.8440` (`PR-AUC = 0.6513`, `Brier = 0.1361`, `Recall = 74.60%` / `F1 = 0.6392` at `tau = 0.330`); `HistGradientBoosting` achieves Test `ROC-AUC = 0.8461` (`PR-AUC = 0.6610`, `tau = 0.340`).
4. **Prescriptive Prioritization:** Held-out `Tier 1 (p >= 0.50)` reaches `67.27%` realized churn (`49.47%` of all test churners in `19.52%` of accounts). Separated targeting policies: probability threshold `p >= 0.33` (`REC-4`, `499 / 1,409 = 35.42%`) vs capacity-constrained top `30%` queue (`REC-5`, `423 / 1,409 = 30.02%`, `p >= 0.3918`, `65.78%` capture, `2.19x` lift).

---

## Citations & Inspiration Disclaimer

- **Dataset Source:** IBM Sample *Telco Customer Churn* CSV (<https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv>).
- **Reference Inspiration (UX Framing Only):** `https://github.com/UtkarshRai-ds/telco-churn-prediction`. This project is an independent clean-room implementation; zero source code, serialized models, metrics, or derived datasets from that repository were reused.
