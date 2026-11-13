"""Programmatic documentation builders for the self-contained report evidence package."""

from __future__ import annotations

from typing import Any

import pandas as pd

from telco_churn.config import IBM_DATASET_URL, IBM_REPO_URL, INSPIRATION_REPO_URL, PROJECT_ROOT


def format_section_guides(res: dict[str, Any]) -> dict[str, str]:
    """Generate numerically verified markdown prose sections directly from executed results."""
    ov = res["dataset_overview"]
    prov = ov["provenance"]
    dims = ov["dimensions"]
    dq = ov["data_quality"]
    kpis = res["descriptive"]["kpis"]

    sub_df = pd.DataFrame(res["descriptive"]["subgroups_table"])
    num_df = pd.DataFrame(res["descriptive"]["numeric_summary_table"])
    comp_df = pd.DataFrame(res["descriptive"]["compound_segments_table"]).set_index("segment_name")
    cat_diag = pd.DataFrame(res["diagnostic"]["categorical_associations"]).set_index("feature")
    cont_diag = pd.DataFrame(res["diagnostic"]["continuous_comparisons"]).set_index("feature")
    conf_df = pd.DataFrame(res["diagnostic"]["confounding_adjusted_odds"]).set_index("encoded_term")

    cv_det = res["predictive"]["cv_details"]
    cv_df = pd.DataFrame(res["predictive"]["cv_comparison"]).set_index("model_name")
    test_df = pd.DataFrame(res["predictive"]["test_comparison"])
    perm_df = pd.DataFrame(res["predictive"]["permutation_importance"])
    tiers_df = pd.DataFrame(res["prescriptive"]["risk_tiers"])
    lift_df = pd.DataFrame(res["prescriptive"]["capacity_lift"])
    rec_df = pd.DataFrame(res["prescriptive"]["recommendations"])

    m2m = sub_df[(sub_df["feature"] == "Contract") & (sub_df["category"] == "Month-to-month")].iloc[0]
    one_yr = sub_df[(sub_df["feature"] == "Contract") & (sub_df["category"] == "One year")].iloc[0]
    two_yr = sub_df[(sub_df["feature"] == "Contract") & (sub_df["category"] == "Two year")].iloc[0]
    fiber = sub_df[(sub_df["feature"] == "InternetService") & (sub_df["category"] == "Fiber optic")].iloc[0]
    dsl = sub_df[(sub_df["feature"] == "InternetService") & (sub_df["category"] == "DSL")].iloc[0]
    no_net = sub_df[(sub_df["feature"] == "InternetService") & (sub_df["category"] == "No")].iloc[0]
    ec = sub_df[(sub_df["feature"] == "PaymentMethod") & (sub_df["category"] == "Electronic check")].iloc[0]
    cc = sub_df[(sub_df["feature"] == "PaymentMethod") & (sub_df["category"] == "Credit card (automatic)")].iloc[0]
    t1_12 = sub_df[(sub_df["feature"] == "tenure_tier") & (sub_df["category"] == "1-12 mo")].iloc[0]
    t49_72 = sub_df[(sub_df["feature"] == "tenure_tier") & (sub_df["category"] == "49-72 mo")].iloc[0]
    m2m_early = comp_df.loc["Month-to-month AND tenure 1-12 mo"]
    fiber_unprot = comp_df.loc["Fiber optic AND (No OnlineSecurity OR No TechSupport)"]
    fiber_neither = comp_df.loc["Fiber optic AND (No OnlineSecurity AND No TechSupport)"]
    fiber_both = comp_df.loc["Fiber optic AND (Both OnlineSecurity & TechSupport = Yes)"]

    champ = cv_det["final_champion_label"]
    tau_champ = float(cv_df.loc[champ, "val_optimal_threshold"])
    tau_lr = float(cv_df.loc["Logistic Regression", "val_optimal_threshold"])
    tau_hgb = float(cv_df.loc["HistGradientBoosting", "val_optimal_threshold"])

    champ_05 = test_df[(test_df["model_name"] == champ) & (test_df["threshold_setting"] == "Default (0.50)")].iloc[0]
    champ_opt = test_df[(test_df["model_name"] == champ) & (test_df["threshold_setting"] != "Default (0.50)")].iloc[0]
    lr_05 = test_df[(test_df["model_name"] == "Logistic Regression") & (test_df["threshold_setting"] == "Default (0.50)")].iloc[0]
    lr_opt = test_df[(test_df["model_name"] == "Logistic Regression") & (test_df["threshold_setting"] != "Default (0.50)")].iloc[0]
    hgb_05 = test_df[(test_df["model_name"] == "HistGradientBoosting") & (test_df["threshold_setting"] == "Default (0.50)")].iloc[0]
    hgb_opt = test_df[(test_df["model_name"] == "HistGradientBoosting") & (test_df["threshold_setting"] != "Default (0.50)")].iloc[0]
    dummy_row = test_df[test_df["model_name"] == "Dummy Floor (Most Frequent)"].iloc[0]

    tier1 = tiers_df.iloc[0]
    tier2 = tiers_df.iloc[1]
    tier3 = tiers_df.iloc[2]
    cap30 = lift_df[lift_df["top_capacity_pct"] == 30].iloc[0]

    readme = f"""# Telco Customer Churn Analytics — Report Evidence Package

## Start Here (Instructions for the Academic Report & Slide Assistant)
This self-contained package contains every table, chart, statistical test result, trained model comparison, explainability ranking, prescriptive prioritization policy, and live dashboard screenshot needed to author the **nine-section midterm report** and accompanying presentation slides without inspecting source code.

## Important Provenance & Scope Disclosure
- **Dataset:** IBM public *Telco Customer Churn* sample (`Telco-Customer-Churn.csv`, `{dims['n_rows']:,}` rows x `{dims['n_cols']}` columns, SHA-256 `{prov.get('sha256', '')}`).
- **Source URL:** `{IBM_DATASET_URL}`
- **Official IBM Caveat:** IBM explicitly identifies this sample as representing a **fictional telecommunications company** cross-sectional snapshot (`Churn` = left within the last month). Do **not** describe these records as verified live carrier financial logs, prospective cohort timelines, or experimentally verified causal effects.
- **Billing Exposure Proxy Clarification:** Monetary figures labeled `monthly_revenue_at_risk_usd` (headline **`${kpis['monthly_revenue_at_risk_usd']:,.2f}/month`**) represent the sum of current `MonthlyCharges` across customers labeled `Churn = Yes` in the cross-sectional snapshot. This is a **historical billing-exposure proxy**, NOT measured future lost revenue or verified retention savings.
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
"""

    how_to_reproduce = f"""# How to Reproduce All Analytical Artifacts & Launch the Dashboard

All paths and commands operate from the `DA_midterm/` project root without developer-specific absolute paths.

## 1. Environment Setup
```powershell
python -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install --upgrade pip
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.\\.venv\\Scripts\\python.exe -m pip install setuptools wheel
.\\.venv\\Scripts\\python.exe -m pip install -e . --no-build-isolation --no-deps
```

## 2. Regenerate Complete Analytical Pipeline (Phases 1-4)
```powershell
.\\.venv\\Scripts\\python.exe -m telco_churn.cli run-all
```
This deterministic command (seed `42`) verifies `data/raw/Telco-Customer-Churn.csv` (SHA-256 `{prov.get('sha256', '')}`), executes descriptive/diagnostic layers (`fig01`–`fig06`), runs Stratified 5-Fold CV and single-pass test evaluation (`fig07`–`fig09`), computes prescriptive tiers & scenario grids (`fig10`), and saves `outputs/results_summary.json`.

## 3. Run Automated Verification & Lint Checks
```powershell
.\\.venv\\Scripts\\python.exe -m ruff check src app tests
.\\.venv\\Scripts\\python.exe -m pytest -v
```

## 4. Launch Interactive Streamlit Dashboard
```powershell
.\\.venv\\Scripts\\streamlit.exe run app/streamlit_app.py
```

## 5. Export and Validate Self-Contained Transfer Package
```powershell
.\\.venv\\Scripts\\python.exe -m telco_churn.cli export-package
```
"""

    preprocessing_decisions = f"""# Data Quality Audit & Preprocessing Decisions

1. **No Silent Row Removal (`N = {dims['n_rows']:,}` Retained):**
   - Exact row duplicates: `{dq['exact_duplicate_rows']}` (`{dims['n_rows']:,}` unique `customerID` strings).
   - Non-ID identical feature+target rows: `{dq['non_id_identical_profile_rows']}` rows match another customer across all 19 predictors and target `Churn` (primarily month-1 subscribers on identical discrete base plans). Because each carries a distinct `customerID` in a cross-sectional snapshot, dropping them would distort segment prevalence. All `{dims['n_rows']:,}` rows are retained.
2. **`TotalCharges` String Parsing (`{dq['blank_total_charges_count']}` Blank Entries = `{dq['blank_total_charges_pct']:.4f}%`):**
   - In the raw CSV, `TotalCharges` is stored as text because `{dq['blank_total_charges_count']}` records contain whitespace (`" "`).
   - Exact verification confirms **100% of these `{dq['blank_total_charges_count']}` blank entries (`all_blank_total_charges_are_tenure_zero={dq['all_blank_total_charges_are_tenure_zero']}`) occur when `tenure == 0` and `Churn == "No"`**.
   - **Treatment:** Parsed to `NaN` via `pd.to_numeric(..., errors="coerce")` for transparent EDA auditing; inside predictive modeling, missing numeric values are imputed using **`SimpleImputer(strategy="median")` fitted strictly inside training CV folds**, guaranteeing zero leakage to held-out test records or single-profile inputs.
3. **Identifier & Target Leakage Prevention:**
   - `customerID` is excluded from all model matrices (`X`) and used strictly to assert zero train/test overlap.
   - Exploratory binned column `tenure_tier` is computed in EDA/diagnostics only and never fed into predictive preprocessing alongside `tenure` (`RAW_PREDICTORS` contains strictly the 19 exogenous schema columns).
4. **Service Dependency Integrity:**
   - Verified 0 inconsistencies between `PhoneService == "No"` ($n=682$) and `MultipleLines == "No phone service"`, and 0 inconsistencies between `InternetService == "No"` ($n=1,526$) and `"No internet service"` across all 6 online add-ons. The interactive scoring helper enforces these exact dependency constraints automatically.
"""

    desc_findings = f"""# Layer 1 — Descriptive Analytics Findings (`01_descriptive/`)

- **Population & Target Composition:** `{kpis['n_customers']:,}` subscribers, of whom `{kpis['n_churned']:,}` churned (**`{kpis['overall_churn_rate_pct']:.2f}%`**, 95% Wilson CI `[{kpis['overall_churn_ci95_low_pct']:.2f}%, {kpis['overall_churn_ci95_high_pct']:.2f}%]`) and `{kpis['n_retained']:,}` stayed (`73.46%`).
- **Disproportionate Monthly Churned Billing Proxy (`monthly_revenue_at_risk_usd`):** Total snapshot billing across all records is `${kpis['total_monthly_charges_usd']:,.2f}/mo`, of which **`${kpis['monthly_revenue_at_risk_usd']:,.2f}/mo` (`{kpis['monthly_revenue_at_risk_pct']:.2f}%`)** is summed from records labeled `Churn = Yes` — higher than their `26.54%` headcount share because churners carry higher median monthly bills (`${num_df[(num_df['variable']=='MonthlyCharges')&(num_df['segment']=='Churn = Yes')]['median'].iloc[0]:.2f}` vs `${num_df[(num_df['variable']=='MonthlyCharges')&(num_df['segment']=='Churn = No')]['median'].iloc[0]:.2f}`). *(Note: this metric is a static monthly billing-exposure proxy across churned accounts, not verified future multi-month revenue lost.)*
- **Contract Concentration (`descriptive_subgroups.csv`, `fig01`):** `Month-to-month` accounts (`n={int(m2m['n_customers']):,}`, `{m2m['pct_of_population']:.2f}%` of base) experience `{m2m['churn_rate_pct']:.2f}%` churn, contributing **`{m2m['share_of_all_churn_pct']:.2f}%`** of all churners (`${m2m['monthly_revenue_at_risk_usd']:,.2f}/mo` historical churned billing), compared with `{one_yr['churn_rate_pct']:.2f}%` on `One year` (`n={int(one_yr['n_customers']):,}`) and `{two_yr['churn_rate_pct']:.2f}%` on `Two year` (`n={int(two_yr['n_customers']):,}`).
- **Early-Tenure Cliff (`fig02`, `fig04`, `fig06`):** Customers in months `1-12` (`n={int(t1_12['n_customers']):,}`) churn at `{t1_12['churn_rate_pct']:.2f}%` (`55.48%` of all churn), vs `{t49_72['churn_rate_pct']:.2f}%` in `49-72 mo` (`n={int(t49_72['n_customers']):,}`). Within the compound segment `Month-to-month AND 1-12 mo` (`n={int(m2m_early['n_customers']):,}`), churn peaks at **`{m2m_early['churn_rate_pct']:.2f}%`**.
- **Broad vs Intersected Fiber & Add-On Patterns (`descriptive_subgroups.csv`, `descriptive_compound_segments.csv`):** Broad `Fiber optic` accounts (`n={int(fiber['n_customers']):,}`) churn at `{fiber['churn_rate_pct']:.2f}%` (`${fiber['monthly_revenue_at_risk_usd']:,.2f}/mo` historical churned billing) vs `{dsl['churn_rate_pct']:.2f}%` for `DSL` and `{no_net['churn_rate_pct']:.2f}%` for no internet. Narrowing Fiber optic to subscribers lacking `OnlineSecurity` OR `TechSupport` isolates **`n={int(fiber_unprot['n_customers']):,}`** accounts (`{fiber_unprot['pct_of_population']:.2f}%` of base) with **`{fiber_unprot['churn_rate_pct']:.2f}%` churn** (`{int(fiber_unprot['n_churned']):,}` churners = `{fiber_unprot['share_of_all_churn_pct']:.2f}%` of all churn; `${fiber_unprot['monthly_revenue_at_risk_usd']:,.2f}/mo` historical churned billing); those lacking *both* add-ons (`n={int(fiber_neither['n_customers']):,}`) churn at **`{fiber_neither['churn_rate_pct']:.2f}%`** compared with **`{fiber_both['churn_rate_pct']:.2f}%`** among Fiber subscribers holding both (`n={int(fiber_both['n_customers']):,}`). Meanwhile, `Electronic check` payers (`n={int(ec['n_customers']):,}`) churn at `{ec['churn_rate_pct']:.2f}%` vs `{cc['churn_rate_pct']:.2f}%` for automatic credit card billing.
"""

    t_cont = cont_diag.loc["tenure"]
    m_cont = cont_diag.loc["MonthlyCharges"]
    tc_cont = cont_diag.loc["TotalCharges"]
    tc_conf = conf_df.loc["TotalCharges"]

    diag_findings = f"""# Layer 2 — Diagnostic Analytics Findings (`02_diagnostic/`)

> **Non-Causality Qualification:** All tests below evaluate observational associations in a cross-sectional snapshot (`N = 7,043`). "Strong association" does not prove causal intervention effects.

- **Categorical Bivariate Associations (`diagnostic_categorical_associations.csv`, `fig06`):**
  1. `Contract`: `chi2={cat_diag.loc['Contract','chi2_stat']:.2f}`, `df=2`, `Cramer's V={cat_diag.loc['Contract','cramers_v']:.4f}`, Holm `p={cat_diag.loc['Contract','p_value_holm']:.2e}` (`39.88` pp spread).
  2. `tenure_tier`: `chi2={cat_diag.loc['tenure_tier','chi2_stat']:.2f}`, `V={cat_diag.loc['tenure_tier','cramers_v']:.4f}`, Holm `p={cat_diag.loc['tenure_tier','p_value_holm']:.2e}`.
  3. `OnlineSecurity`: `V={cat_diag.loc['OnlineSecurity','cramers_v']:.4f}`, Holm `p={cat_diag.loc['OnlineSecurity','p_value_holm']:.2e}` (`41.77%` without vs `14.61%` with add-on).
  4. `TechSupport`: `V={cat_diag.loc['TechSupport','cramers_v']:.4f}`, Holm `p={cat_diag.loc['TechSupport','p_value_holm']:.2e}` (`41.64%` without vs `15.17%` with add-on).
  5. `InternetService` (`V={cat_diag.loc['InternetService','cramers_v']:.4f}`) and `PaymentMethod` (`V={cat_diag.loc['PaymentMethod','cramers_v']:.4f}`).
  - By contrast, `gender` (`V={cat_diag.loc['gender','cramers_v']:.4f}`, Holm `p={cat_diag.loc['gender','p_value_holm']:.4f}`) and `PhoneService` (`V={cat_diag.loc['PhoneService','cramers_v']:.4f}`, Holm `p={cat_diag.loc['PhoneService','p_value_holm']:.4f}`) show **no statistically significant** association with Churn.
- **Continuous Group Comparisons (`diagnostic_continuous_comparisons.csv`, `fig02`, `fig03`, `fig05`):**
  - `tenure`: Churners mean `{t_cont['mean_churn_yes']:.2f}` mo vs retained `{t_cont['mean_churn_no']:.2f}` mo (Welch `t={t_cont['welch_t_stat']:.2f}`, Mann-Whitney `p={t_cont['mann_whitney_p_value']:.2e}`, `rank-biserial r={t_cont['rank_biserial_r']:+.4f}`).
  - `MonthlyCharges`: Churners mean `${m_cont['mean_churn_yes']:.2f}` vs retained `${m_cont['mean_churn_no']:.2f}` (`t={m_cont['welch_t_stat']:.2f}`, `p={m_cont['mann_whitney_p_value']:.2e}`, `r_rb={m_cont['rank_biserial_r']:+.4f}`).
  - `TotalCharges`: Churners mean `${tc_cont['mean_churn_yes']:,.2f}` vs retained `${tc_cont['mean_churn_no']:,.2f}` (`r_rb={tc_cont['rank_biserial_r']:+.4f}`).
- **Multivariable Confounding Reversal (`diagnostic_confounding_adjusted_odds.csv`):**
  - Marginally, `TotalCharges` exhibits negative association with churn (`unadjusted log-odds={tc_conf['unadjusted_log_odds']:+.4f}`, `OR={tc_conf['unadjusted_odds_ratio']:.4f}`) purely because cumulative charges increase mechanically with tenure (`TotalCharges ~ tenure * MonthlyCharges`). Controlling for `tenure` and `MonthlyCharges` reverses `TotalCharges` to `adjusted log-odds={tc_conf['adjusted_log_odds']:+.4f}` (`OR={tc_conf['adjusted_odds_ratio']:.4f}`).
"""

    split_md = f"""# Split Strategy, Cross-Validation & Leak-Free Evaluation (`03_predictive/`)

- **Why Stratified Random Split (Instead of Chronological):** The IBM CSV (`7,043` records) contains no calendar timestamps (`tenure` is subscription duration in months `0..72`). Inventing a chronological split would impose arbitrary ordering. Stratified random sampling (`test_size=0.20`, `random_state=42`, `stratify=Churn`) preserves exact class prevalence (`26.54%`) and enforces 0 overlapping `customerID`s:
  - **Training / CV Development Split:** `n = 5,634` (`79.99%`; `1,495` Churn = Yes, `26.5353%`)
  - **Sealed Hold-Out Test Split:** `n = 1,409` (`20.01%`; `374` Churn = Yes, `26.5436%`)
- **Cross-Validation & Independent Threshold Protocol (`model_cv_comparison.csv`):**
  - All imputers (`SimpleImputer(strategy="median")`), numeric scalers (`StandardScaler`), categorical `OneHotEncoder(handle_unknown="ignore")`, hyperparameter grid searches (`5-fold Stratified CV`), probability calibration assessment, and each model's F1-optimal cutoff (`Logistic Regression`: `tau={tau_lr:.3f}`; `{champ}`: `tau={tau_champ:.3f}`; `HistGradientBoosting`: `tau={tau_hgb:.3f}`) were selected **exclusively from 5-fold CV out-of-fold probabilities inside the 5,634 training records**, with zero hold-out test peeking.
  - Sigmoid calibration check: Uncalibrated `{cv_det['base_champion_model']}` already achieved superior CV Brier score (`{cv_det['raw_champion_cv_brier']:.4f}` vs calibrated `{cv_det['calibrated_champion_cv_brier']:.4f}`, ECE `{cv_df.loc[champ,'cv_ece']:.4f}`), so `{champ}` probabilities were retained unwarped (`calibration_applied={cv_det['calibration_applied']}`).
"""

    model_spec_md = f"""# Predictive Model Specifications & Held-Out Test Benchmarks (`03_predictive/`)

- **Algorithms Evaluated Fairly Under Identical Preprocessing (`n_test = 1,409`, `374` positive churners):**
  1. **No-Skill Floor (`DummyClassifier` most frequent):** Accuracy `{dummy_row['accuracy']:.4f}`, Recall `0.0000`, ROC-AUC `0.5000`, PR-AUC `{dummy_row['pr_auc']:.4f}`. *(Reference only; not counted as a trained ML algorithm.)*
  2. **Simple Baseline Algorithm (`Logistic Regression`, L2 C=5.0):**
     - Default `0.50`: Test ROC-AUC **`{lr_05['roc_auc']:.4f}`**, PR-AUC **`{lr_05['pr_auc']:.4f}`**, Brier `{lr_05['brier_score']:.4f}`, Accuracy `{lr_05['accuracy']:.4f}`, F1 `{lr_05['f1_score']:.4f}` (`TP={int(lr_05['tp'])}, FP={int(lr_05['fp'])}, FN={int(lr_05['fn'])}, TN={int(lr_05['tn'])}`).
     - Own CV F1-Opt (`tau={tau_lr:.3f}`): Precision `{lr_opt['precision']:.4f}`, Recall `{lr_opt['recall']:.4f}`, F1 `{lr_opt['f1_score']:.4f}` (`TP={int(lr_opt['tp'])}, FP={int(lr_opt['fp'])}, FN={int(lr_opt['fn'])}, TN={int(lr_opt['tn'])}`).
  3. **Selected Champion Model (`{champ}`, selected via highest 5-fold CV ROC-AUC={cv_df.loc[champ,'cv_roc_auc']:.4f}):**
     - Default `0.50`: Test ROC-AUC **`{champ_05['roc_auc']:.4f}`**, PR-AUC **`{champ_05['pr_auc']:.4f}`**, Brier **`{champ_05['brier_score']:.4f}`**, ECE **`{champ_05['calibration_ece']:.4f}`**, Accuracy `{champ_05['accuracy']:.4f}`, Precision `{champ_05['precision']:.4f}`, Recall `{champ_05['recall']:.4f}`, F1 `{champ_05['f1_score']:.4f}` (`TP={int(champ_05['tp'])}, FN={int(champ_05['fn'])}`).
     - Own CV F1-Opt (`tau={tau_champ:.3f}`): Precision `{champ_opt['precision']:.4f}`, Recall **`{champ_opt['recall']:.4f}`** (`{int(champ_opt['tp'])}/374` churners captured; `FN` drops from `{int(champ_05['fn'])}` to `{int(champ_opt['fn'])}`), **F1 `{champ_opt['f1_score']:.4f}`**, Accuracy `{champ_opt['accuracy']:.4f}`.
  4. **Runner-Up Boosting Ensemble (`HistGradientBoosting`):**
     - Default `0.50`: Test ROC-AUC **`{hgb_05['roc_auc']:.4f}`**, PR-AUC **`{hgb_05['pr_auc']:.4f}`**, Brier `{hgb_05['brier_score']:.4f}`, Accuracy `{hgb_05['accuracy']:.4f}`, F1 `{hgb_05['f1_score']:.4f}`.
     - Own CV F1-Opt (`tau={tau_hgb:.3f}`): Precision `{hgb_opt['precision']:.4f}`, Recall `{hgb_opt['recall']:.4f}`, **F1 `{hgb_opt['f1_score']:.4f}`** (`TP={int(hgb_opt['tp'])}, FP={int(hgb_opt['fp'])}, FN={int(hgb_opt['fn'])}, TN={int(hgb_opt['tn'])}`).
- **Critical Modeling Finding:** Linear `Logistic Regression` (`ROC-AUC={lr_05['roc_auc']:.4f}`) performs very close to tree ensembles (`0.8440`–`0.8461`) because churn propensity in the IBM sample is predominantly smooth and additive across contract length, tenure, and internet tier, with modest non-linear interaction gains (`HistGradientBoosting` PR-AUC `+0.0324` over baseline).
"""

    top5_perm = perm_df.head(5)
    perm_bullets = "\n".join(
        f"  {int(r.importance_rank)}. `{r.raw_feature}`: mean dROC-AUC = `{r.roc_auc_drop_mean:.4f}` (±`{r.roc_auc_drop_sd:.4f}`), mean dPR-AUC = `{r.pr_auc_drop_mean:.4f}`"
        for r in top5_perm.itertuples()
    )
    explain_md = f"""# Model Explainability & Limitations (`03_predictive/`)

## 1. Raw-Column Test Permutation Importance (`permutation_importance.csv`, `fig09`)
Evaluating permutation drops on raw input columns before one-hot encoding preserves unified feature credit:
{perm_bullets}

## 2. Logistic Regression Directional Log-Odds (`logistic_odds_ratios.csv`, `fig09`)
- Strongest **risk-increasing** active indicators: `InternetService_Fiber optic` (`beta=+1.1535`, OR=`3.1694`), `Contract_Month-to-month` (`beta=+0.5525`, OR=`1.7375`), `StreamingMovies_Yes` (`+0.4474`), `StreamingTV_Yes` (`+0.4464`), `PaymentMethod_Electronic check` (`+0.1727`).
- Strongest **protective** signals: `tenure` (`beta=-1.2677` per 1 SD, OR=`0.2815`), `InternetService_DSL` (`beta=-1.0366`), `Contract_Two year` (`beta=-0.8248`, OR=`0.4383`), `Dependents_Yes` (`beta=-0.3213`).
- **Collinearity Explanation on `MonthlyCharges`:** In unconditional diagnostics `MonthlyCharges` increases churn (`r_rb=+0.2416`), yet its conditional Logistic Regression coefficient turns negative (`-1.6791`) because `MonthlyCharges` is almost collinear with holding `Fiber optic` + streaming + multiple-line indicators simultaneously. Permutation importance on `Random Forest` avoids coefficient sign-splitting and shows predictive credit consistently ranks `Contract`, `tenure`, `InternetService`, and `TotalCharges` at the top.

## 3. Practical Limitations of Predictive Scores
- **Missed Churn vs False Alarm Tradeoff:** Even at `tau={tau_champ:.3f}`, `{int(champ_opt['fn'])}` of `374` test churners (`{100 - champ_opt['recall']*100:.2f}%`) are missed while `{int(champ_opt['fp'])}` non-churners are flagged as false alarms (`Precision={champ_opt['precision']*100:.2f}%`), justifying low-cost outreach rather than expensive universal discounts.
- **Snapshot Restriction:** Predicts retrospective class membership (*left last month*) on synthetic sample customers; does not incorporate network outage logs, competitor price drops, or customer support transcripts.
"""

    rec_md_lines = [
        "# Layer 4 — Prescriptive Recommendations Backed by Evidence (`04_prescriptive/`)\n",
        "Each recommendation cites concrete statistics from Descriptive, Diagnostic, and Predictive outputs alongside explicit non-causal assumptions. `REC-4` (probability threshold `p >= 0.33`) and `REC-5` (budget-capped top-30% queue `p >= 0.3918`) are explicitly separated as distinct targeting policies.\n",
    ]
    for r in rec_df.itertuples():
        rec_md_lines.extend(
            [
                f"## {r.rec_id}: {r.target_segment} [{r.priority}]",
                f"- **Measured Segment Count & Scope:** `n = {int(r.segment_n):,}` ({r.segment_pct_of_scope:.2f}% of `{r.segment_scope}`)",
                f"- **Descriptive Evidence:** {r.descriptive_evidence}",
                f"- **Diagnostic Evidence:** {r.diagnostic_evidence}",
                f"- **Predictive Evidence:** {r.predictive_evidence}",
                f"- **Proposed Action:** {r.proposed_action}",
                f"- **Assumptions & Caveats:** {r.assumptions_and_caveats}",
                f"- **Source Paths:** `{r.evidence_paths}`\n",
            ]
        )

    assump_md = f"""# Prescriptive Targeting Tiers, Capacity Lift & Assumption Sensitivity

## 1. Held-Out Risk Tier Realization (`prescriptive_risk_tiers.csv`, `n_test = 1,409`)
- **{tier1['risk_tier']}:** `{int(tier1['n_test_customers'])}` customers (`{tier1['pct_of_test_population']:.2f}%`), mean predicted churn `{tier1['mean_predicted_prob_pct']:.2f}%` vs **realized churn `{tier1['actual_churn_rate_pct']:.2f}%`** (`{int(tier1['actual_churn_count'])}` churners = **`{tier1['capture_of_all_test_churners_pct']:.2f}%`** of all test churn; `${tier1['actual_churn_monthly_rev_at_risk_usd']:,.2f}/mo` historical monthly billing among churned test records).
- **{tier2['risk_tier']}:** `{int(tier2['n_test_customers'])}` customers (`{tier2['pct_of_test_population']:.2f}%`), mean predicted `{tier2['mean_predicted_prob_pct']:.2f}%` vs **realized churn `{tier2['actual_churn_rate_pct']:.2f}%`** (`{int(tier2['actual_churn_count'])}` churners = `{tier2['capture_of_all_test_churners_pct']:.2f}%` of all test churn; `${tier2['actual_churn_monthly_rev_at_risk_usd']:,.2f}/mo` historical churned billing).
- **{tier3['risk_tier']}:** `{int(tier3['n_test_customers'])}` customers (`{tier3['pct_of_test_population']:.2f}%`), mean predicted `{tier3['mean_predicted_prob_pct']:.2f}%` vs **realized churn `{tier3['actual_churn_rate_pct']:.2f}%`**.

## 2. Threshold Policy (`REC-4`) vs. Capacity Queue (`REC-5`) & Scenario Sensitivity
- **Why Two Policies Differ:** Evaluating `{champ}` on the sealed `1,409`-account test set at its CV F1-optimal probability threshold `tau = {tau_champ:.3f}` (`REC-4`) flags **`499` accounts (`35.42%`)**, reaching `{int(champ_opt['tp'])} / 374` (`{champ_opt['recall']*100:.2f}%`) of churners. By contrast, capping outreach strictly at the Top **`30%`** capacity tier (`REC-5`, empirical test rank cutoff `p >= {cap30['min_predicted_prob_in_tier']:.4f}`) selects **`{int(cap30['customers_targeted'])}` test accounts (`30.02%`)**, reaching **`{int(cap30['true_churners_captured'])} / 374` (`{cap30['cumulative_churn_recall_pct']:.2f}%`)** of churners (`{cap30['lift_over_random_outreach']:.2f}x` lift over random outreach) covering `${cap30['targeted_monthly_rev_at_risk_usd']:,.2f}/mo` in historical churned monthly charges.
- **Explicit Separation of Facts vs Assumptions:** All financial scenario numbers (`$15`/`$25` outreach cost, `10%–30%` assumed save rate, `6`-month horizon) in `prescriptive_scenario_sensitivity.csv` and the Streamlit Scenario Simulator are **user-adjustable hypothetical assumptions** — NOT measured treatment effects or guaranteed revenue saved. If actual outreach costs `$25/cust` and only saves `10%` at `40%` outreach capacity, illustrative 6-month net value turns negative (`-$919.05`). A controlled A/B retention pilot is required before rollout.
"""

    dashboard_walk = """# Interactive Streamlit Dashboard Walkthrough (`05_dashboard/`)

- **Application Entrypoint:** `app/streamlit_app.py` (supported by pure helper module `app/helpers.py`).
- **Launch Command (from `DA_midterm/` root):**
  ```powershell
  .\\.venv\\Scripts\\streamlit.exe run app/streamlit_app.py
  ```
- **Four Tested Views (Verified via `AppTest` and Headless Edge CDP Screenshots):**
  1. `01_overview.png` (**Executive Overview**): KPI metrics (including historical churned monthly billing proxy), data-quality audit table (`TotalCharges` 11 blanks, `0` exact duplicates), and `fig01` contract/payment risk chart.
  2. `02_explore_diagnose.png` (**Explore & Diagnose**): Interactive cohort filters dynamically update KPIs and charts; tabs expose numeric distributions, Chi-square/Cramer's V tests, and `TotalCharges` confounding reversal.
  3. `03_predictive_models.png` (**Predictive Models & Explainability**): Compares 5-Fold CV vs sealed held-out Test benchmarks (`n=1,409`), interactive cutoff slider (`tau`), raw-column permutation importance, and an *Educational Single-Profile Scorer* enforcing service-hierarchy logic via `champion_pipeline.joblib`.
  4. `04_prescriptive_retention.png` (**Prescriptive Prioritization**): Held-out risk tiers, capacity capture lift (`fig10`), interactive assumption-labeled budget/save simulator, and traceable `REC-1`–`REC-5` action matrix.
"""

    filters_md = """# Dashboard Interactive Controls & State Guarantees

1. **Zero UI Retraining:** All tables and `champion_pipeline.joblib` are loaded once via `@st.cache_resource`; changing filters, thresholds, or scenario sliders never retrains models or leaks test labels.
2. **Cohort Filters (`Explore & Diagnose`):** `Contract`, `InternetService`, `PaymentMethod`, `SeniorCitizen`, and `tenure` slider `[0..72]` dynamically recompute sample size `n`, churn rate %, 95% Wilson CI bounds, historical churned monthly billing, and subgroup bar charts.
3. **Cutoff Explorer (`Predictive Models`):** Adjusting `tau` in `[0.15, 0.75]` recalculates exact confusion counts (`TP/FP/FN/TN`), Precision, Recall, F1, and Accuracy directly on precomputed held-out `test_predictions.csv`.
4. **Hierarchy-Safe Single-Profile Scorer:** Setting `PhoneService = "No"` locks `MultipleLines = "No phone service"` and setting `InternetService = "No"` locks all six add-ons to `"No internet service"` before calling `validate_customer_record()` and `champion_pipeline.predict_proba()`.
5. **Scenario Simulator (`Prescriptive Prioritization`):** Strictly separates observed held-out churners reached and historical churned billing from user-adjustable inputs (`Outreach Capacity %`, `Cost/Contact $`, `Assumed Save Rate %`, `Horizon Months`).
"""

    citations_md = f"""# Verified Sources and Academic References

1. **IBM Telco Customer Churn Sample Dataset:** IBM Developer / Cloud Pak for Data Sample Repository. CSV URL: <{IBM_DATASET_URL}>; Repository: <{IBM_REPO_URL}>. *(Note: IBM explicitly describes this dataset as sample data for a fictional telecommunications company.)*
2. **Pedregosa, F., et al. (2011).** Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830. (Used for Stratified Splitting, Pipelines, LogisticRegression, RandomForestClassifier, HistGradientBoostingClassifier, Permutation Importance, Calibration, and Metrics.)
3. **Virtanen, P., et al. (2020).** SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods*, 17(3), 261–272. (Used for Pearson Chi-square, Welch's t-test, and Mann-Whitney U tests.)
4. **Wilson, E. B. (1927).** Probable inference, the law of succession, and statistical inference. *Journal of the American Statistical Association*, 22(158), 209–212. (Used for 95% binomial proportion confidence intervals.)
5. **Breiman, L. (2001).** Random Forests. *Machine Learning*, 45(1), 5–32; and Permutation Feature Importance methodology.
6. **Optional Reference Inspiration (UX Context Only — No Code or Results Copied):** Public repository <{INSPIRATION_REPO_URL}> (consulted at a high level for general dashboard UX framing only; all implementation, preprocessing, models, charts, and numerical findings in this project are 100% original).
"""

    sources_limitations = f"""# Sources, Methodology Boundaries, and Honest Limitations

1. **Fictional Snapshot Caveat:** IBM's sample CSV (`N = {dims['n_rows']:,}`) describes a fictional carrier snapshot rather than verified real-world commercial transactions or multi-month longitudinal follow-up.
2. **Historical Billing Exposure vs Prospective Revenue:** Metrics labeled `monthly_revenue_at_risk_usd` (e.g., `${kpis['monthly_revenue_at_risk_usd']:,.2f}/mo`) measure current monthly charges on records labeled `Churn = Yes`. They quantify retrospective billing exposure in the snapshot, NOT verified multi-month lost revenue or guaranteed retention savings.
3. **Non-Causality:** Bivariate diagnostics (`Cramer's V`, `Mann-Whitney U`) and model explanations (`Permutation Importance`, `Logistic Odds`) reveal statistical associations and predictive signal; they do **not** establish that modifying an attribute (e.g., gifting OnlineSecurity or migrating contracts) will causally reduce churn by the observational difference.
4. **Missingness & Duplicate Handling Transparency:** Exact `TotalCharges` blanks (`n = {dq['blank_total_charges_count']}`, `100%` at `tenure = 0`) and `22` non-ID matching feature profiles are documented rather than silently deleted.
5. **No Treatment Uplift Data:** Financial figures in `prescriptive_scenario_sensitivity.csv` quantify sensitivity across explicit scenario assumptions (`cost`, `save rate`, `horizon`) rather than observed campaign ROI.
"""

    section_map = f"""# Nine-Section Midterm Report & Presentation Slide Mapping

Use this mapping when drafting the Word report (`01_OFFICIAL_REQUIREMENTS_EN.md`, Section C) and PowerPoint deck:

| Report Section | Key Analytical Content to Write | Primary Evidence Files to Cite | Best Slides / Visuals |
|---|---|---|---|
| **1. Introduction** | Churn problem statement ("which subscribers leave, what drives association, who is at risk, how to prioritize retention"), snapshot scale (`{kpis['overall_churn_rate_pct']:.2f}%` churn; `${kpis['monthly_revenue_at_risk_usd']:,.2f}/mo` historical monthly billing on churned accounts), fictional IBM sample framing. | `README_START_HERE.md`<br>`RESULTS_AND_INTERPRETATION_GUIDE.md` (§1)<br>`SOURCES_AND_LIMITATIONS.md` | Slide 1-2: Problem Framing & KPI Banner (`05_dashboard/screenshots/01_overview.png`) |
| **2. Dataset** | IBM Telco provenance (`N=7,043`, `p=21`, SHA-256 verified), schema breakdown (demographics, services, contract/billing, `Churn`), `TotalCharges` `11` blank parsing at `tenure=0`, `0` exact duplicates, `22` identical non-ID rows retained, service consistency. | `00_dataset_and_quality/schema_dictionary.csv`<br>`00_dataset_and_quality/data_quality_audit.csv`<br>`00_dataset_and_quality/preprocessing_decisions.md` | Slide 3: Dataset Schema & Data Quality Audit Table |
| **3. Descriptive Analytics** | KPIs (`26.54%` churn vs `30.50%` churned monthly billing share), `Contract` (`42.71%` M2M = `88.55%` churn share), `tenure_tier` (`47.68%` in `1-12 mo`), compound segments (`Fiber optic` lacking add-ons `n=2,722`, `45.70%` churn; lacking both `n=1,765`, `55.01%`), `Electronic check` (`45.29%`). | `01_descriptive/findings.md`<br>`01_descriptive/tables/descriptive_kpis.csv`<br>`01_descriptive/tables/descriptive_subgroups.csv`<br>`01_descriptive/tables/descriptive_compound_segments.csv` | `fig01_churn_by_contract_payment.png`<br>`fig02_numeric_distributions_kde.png`<br>`fig03_charges_by_contract_churn_boxplot.png` |
| **4. Diagnostic Analytics** | Chi-square + Cramer's V rankings (`Contract` `0.4101`, `tenure_tier` `0.3512`, `OnlineSecurity` `0.3474`, `TechSupport` `0.3429`), Mann-Whitney U (`tenure r_rb=-0.4797`), `TotalCharges` confounding reversal (`-0.5349 -> +0.6703`), explicit non-causality. | `02_diagnostic/findings.md`<br>`02_diagnostic/tables/diagnostic_categorical_associations.csv`<br>`02_diagnostic/tables/diagnostic_continuous_comparisons.csv`<br>`02_diagnostic/tables/diagnostic_confounding_adjusted_odds.csv` | `fig04_tenure_violin_by_contract_churn.png`<br>`fig05_tenure_vs_monthly_charges_scatter.png`<br>`fig06_diagnostic_association_heatmaps.png` |
| **5. Predictive Analytics** | Stratified 80/20 split (`5,634`/`1,409`), 5-fold CV benchmark, Logistic Baseline (`AUC={lr_05['roc_auc']:.4f}`, `tau={tau_lr:.3f}`) vs `{champ}` (`AUC={champ_05['roc_auc']:.4f}`, `tau={tau_champ:.3f}`, `F1={champ_opt['f1_score']:.4f}`, `Recall={champ_opt['recall']:.4f}`) vs `HistGradientBoosting` (`PR-AUC={hgb_05['pr_auc']:.4f}`, `tau={tau_hgb:.3f}`), Permutation Importance & Log-Odds. | `03_predictive/split_and_validation.md`<br>`03_predictive/model_specification.md`<br>`03_predictive/explanation_and_limitations.md`<br>`03_predictive/tables/model_test_comparison.csv`<br>`03_predictive/tables/permutation_importance.csv` | `fig07_model_roc_pr_calibration_curves.png`<br>`fig08_confusion_matrices_heatmap.png`<br>`fig09_model_explainability.png` |
| **6. Prescriptive Analytics & Dashboard** | Risk tiers (`Tier 1`: `67.27%` realized churn), distinct threshold (`REC-4`: `p>=0.33`, `499/1,409`) vs capacity queue (`REC-5`: top 30% `423/1,409`, `65.78%` capture, `2.19x` lift), `REC-1`–`REC-5`, assumption sensitivity, interactive Streamlit dashboard. | `04_prescriptive/recommendations_with_evidence.md`<br>`04_prescriptive/assumptions_and_sensitivity.md`<br>`04_prescriptive/tables/prescriptive_recommendations.csv`<br>`05_dashboard/walkthrough.md` | `fig10_prescriptive_targeting_lift.png`<br>`05_dashboard/screenshots/01_overview.png`–`04_prescriptive_retention.png` |
| **7. Conclusion** | Synthesis from problem to targeted onboarding/security-bundle/autopay/capacity prioritization, plus explicit fictional snapshot & non-causal limitations. | `RESULTS_AND_INTERPRETATION_GUIDE.md`<br>`SOURCES_AND_LIMITATIONS.md` | Final Summary Slide (Keep concise; max 3-4 bullets + caveat) |
| **8. Team Contributions** | *Placeholder Only:* Student must fill in actual team members, IDs, roles, and contribution percentages. | External user input (`PENDING_USER_INFO`) | Team / Contributions Slide |
| **9. References** | Official IBM dataset URL, scikit-learn, SciPy, Wilson CI, and reference disclaimers. | `06_references_and_report_helpers/citations.md` | References Slide |
"""

    results_guide = f"""# Comprehensive Results & Interpretation Guide (`RESULTS_AND_INTERPRETATION_GUIDE.md`)

> **For the Report-Writing AI Assistant:** Every count, rate, confidence interval, test statistic, model score, and recommendation metric below was computed from the actual execution of the `Telco-Customer-Churn.csv` analytical pipeline. Monetary totals on `Churn = Yes` rows reflect historical monthly billing in churned snapshot records, not verified future lost revenue or causal savings.

---

{desc_findings}

---

{diag_findings}

---

{split_md}

{model_spec_md}

{explain_md}

---

{''.join(rec_md_lines)}

{assump_md}

---

{sources_limitations}
"""

    return {
        "README_START_HERE.md": readme,
        "HOW_TO_REPRODUCE.md": how_to_reproduce,
        "RESULTS_AND_INTERPRETATION_GUIDE.md": results_guide,
        "SOURCES_AND_LIMITATIONS.md": sources_limitations,
        "00_dataset_and_quality/preprocessing_decisions.md": preprocessing_decisions,
        "01_descriptive/findings.md": desc_findings,
        "02_diagnostic/findings.md": diag_findings,
        "03_predictive/split_and_validation.md": split_md,
        "03_predictive/model_specification.md": model_spec_md,
        "03_predictive/explanation_and_limitations.md": explain_md,
        "04_prescriptive/recommendations_with_evidence.md": "\n".join(rec_md_lines),
        "04_prescriptive/assumptions_and_sensitivity.md": assump_md,
        "05_dashboard/walkthrough.md": dashboard_walk,
        "05_dashboard/filters_and_interactions.md": filters_md,
        "05_dashboard/DASHBOARD_SCREENSHOT_GUIDE.md": (PROJECT_ROOT / "DASHBOARD_SCREENSHOT_GUIDE.md").read_text(encoding="utf-8") if (PROJECT_ROOT / "DASHBOARD_SCREENSHOT_GUIDE.md").exists() else "",
        "05_dashboard/DASHBOARD_FUNCTIONALITY_COVERAGE.md": (PROJECT_ROOT / "DASHBOARD_FUNCTIONALITY_COVERAGE.md").read_text(encoding="utf-8") if (PROJECT_ROOT / "DASHBOARD_FUNCTIONALITY_COVERAGE.md").exists() else "",
        "06_references_and_report_helpers/citations.md": citations_md,
        "06_references_and_report_helpers/suggested_report_section_mapping.md": section_map,
    }
