# Interactive Streamlit Dashboard Walkthrough (`05_dashboard/`)

- **Application Entrypoint:** `app/streamlit_app.py` (supported by pure helper module `app/helpers.py`).
- **Launch Command (from `DA_midterm/` root):**
  ```powershell
  .\.venv\Scripts\streamlit.exe run app/streamlit_app.py
  ```
- **Four Tested Views (Verified via `AppTest` and Headless Edge CDP Screenshots):**
  1. `01_overview.png` (**Executive Overview**): KPI metrics (including historical churned monthly billing proxy), data-quality audit table (`TotalCharges` 11 blanks, `0` exact duplicates), and `fig01` contract/payment risk chart.
  2. `02_explore_diagnose.png` (**Explore & Diagnose**): Interactive cohort filters dynamically update KPIs and charts; tabs expose numeric distributions, Chi-square/Cramer's V tests, and `TotalCharges` confounding reversal.
  3. `03_predictive_models.png` (**Predictive Models & Explainability**): Compares 5-Fold CV vs sealed held-out Test benchmarks (`n=1,409`), interactive cutoff slider (`tau`), raw-column permutation importance, and an *Educational Single-Profile Scorer* enforcing service-hierarchy logic via `champion_pipeline.joblib`.
  4. `04_prescriptive_retention.png` (**Prescriptive Prioritization**): Held-out risk tiers, capacity capture lift (`fig10`), interactive assumption-labeled budget/save simulator, and traceable `REC-1`–`REC-5` action matrix.
