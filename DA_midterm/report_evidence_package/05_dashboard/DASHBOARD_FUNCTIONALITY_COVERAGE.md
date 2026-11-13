# Dashboard Functionality Coverage Matrix
**Project:** Telco Customer Churn Analytics (Decision Support Dashboard)  
**Location:** `DA_midterm/app/streamlit_app.py`  
**Base URL:** `http://localhost:8501`  
**Execution Context:** Sealed Test Set ($N = 1,409$), Stratified 80/20 Dev/Test Split, IBM Telco Sample Dataset ($N = 7,043$).

---

## 1. Overview & Verification Summary

This document provides a 100% complete traceability matrix mapping every user-facing interactive component, filter control, prediction interface, statistical diagnostic panel, and prescriptive tool in the running Streamlit dashboard to its corresponding high-resolution demonstration screenshot in `dashboard_demonstration_package/`.

Every screenshot has been captured from the live, unmocked Streamlit application rendered at high resolution ($1440 \times 1100$ or $1440 \times 1450$).

---

## 2. Interactive Feature-to-Screenshot Coverage Matrix

| # | Dashboard View | Component / Feature Description | Interactive Trigger / Parameter State | Target Output / Observed Behavior | Captured Screenshot Path |
|---|---|---|---|---|---|
| **1** | **1. Executive Overview** | Executive KPI metric cards & analytical narrative callout | `?view=overview` (Default landing state) | Displays $N=7,043$ subscribers, $26.54\%$ churn rate (Wilson 95% CI $[25.52\%, 27.58\%]$), 1,869 churners, and $\$139,131$ monthly billing exposure ($30.5\%$ of revenue). | `01_executive_overview/01_executive_kpis_and_narrative.png` |
| **2** | **1. Executive Overview** | Core segmentation bar charts & Provenance Audit Table | `?view=overview` (Scroll $y = 420\text{px}$) | Dual Matplotlib bar charts (Contract & Payment churn rates) and 9-row dataset audit table verifying 11 whitespace string fixes, 0 true missing, 0 duplicates. | `01_executive_overview/02_contract_payment_churn_and_data_audit.png` |
| **3** | **1. Executive Overview** | Panoramic executive overview (full page) | `?view=overview` (Extended viewport $1440 \times 1450\text{px}$) | Uninterrupted panoramic capture showing KPIs, executive narrative, bivariate bar charts, and data provenance audit table in a single unified view. | `01_executive_overview/03_overview_panoramic_full_view.png` |
| **4** | **2. Explore & Diagnose** | Multi-dimensional cohort filtering (Baseline state) | `?view=explore` (All filters reset) | Controls: Multi-select Contract (All 3), Internet (All 3), Payment (All 4), Senior Citizen (All), Tenure Slider $[0, 72]$. Dynamic KPI card confirms baseline $N=7,043$. | `02_explore_and_diagnose/01_cohort_filters_baseline.png` |
| **5** | **2. Explore & Diagnose** | Dynamic cohort filtering (Month-to-month early tenure) | `?view=explore&contract=month-to-month&tenure_max=12` | Sub-cohort isolated: $N=2,058$ ($29.2\%$ of base), churn rate jumps to $51.35\%$ (CI $[49.19\%, 53.51\%]$), 1,057 churners, $\$70,724$ monthly billing exposure ($50.8\%$ of total churn revenue!). | `02_explore_and_diagnose/02_cohort_filters_month_to_month_early_tenure.png` |
| **6** | **2. Explore & Diagnose** | Dynamic subgroup breakdown chart & statistical table | `?view=explore` (Dropdown: `Contract`) | Matplotlib subgroup bar chart with Wilson 95% error bars and $(n=\dots)$ sample size annotations, paired with complete statistical summary table. | `02_explore_and_diagnose/03_dynamic_subgroup_barchart_and_table.png` |
| **7** | **2. Explore & Diagnose** | Tab 1: Numeric Distributions & Hexbin | `?view=explore` $\rightarrow$ Click Tab 0 | KDE density plots for tenure, MonthlyCharges, TotalCharges stratified by churn; boxplots by contract term; violin plots; tenure vs charges hexbin. | `02_explore_and_diagnose/04_numeric_distributions_and_boxplots.png` |
| **8** | **2. Explore & Diagnose** | Tab 2: Bivariate Diagnostic Tests | `?view=explore` $\rightarrow$ Click Tab 1 | Heatmap of Cramér's V and Pearson Chi-square associations with Holm-Bonferroni correction; Mann-Whitney U test results; explicit observational disclaimer. | `02_explore_and_diagnose/05_bivariate_diagnostic_associations.png` |
| **9** | **2. Explore & Diagnose** | Tab 3: Confounding Audit & Simpson's Paradox | `?view=explore` $\rightarrow$ Click Tab 2 | Simpson's paradox demonstration: unadjusted log-odds for `TotalCharges` ($-0.5349$) reverses to $+0.6703$ when controlling for tenure and monthly charges; 16-variable confounding table. | `02_explore_and_diagnose/06_confounding_audit_simpsons_paradox.png` |
| **10** | **3. Predictive Models** | Tab 0: Model Benchmark (CV & Test Tables) | `?view=predictive` $\rightarrow$ Tab 0 (Top) | Stratified 80/20 protocol info banner; 5-Fold Cross-Validation Summary table (dev $n=5,634$); Sealed Held-Out Test Benchmark table ($n=1,409$). | `03_predictive_models/01_model_benchmark_cv_and_test.png` |
| **11** | **3. Predictive Models** | Tab 0: Confusion Matrices & Diagnostic Curves | `?view=predictive` $\rightarrow$ Tab 0 (Scroll $y = 750\text{px}$) | ROC Curves (AUC 0.842 vs 0.838 vs 0.841), Precision-Recall curves, Calibration curves, and 3-panel confusion matrix heatmaps evaluated at optimal cutoff ($\tau=0.33$). | `03_predictive_models/02_confusion_matrices_benchmark.png` |
| **12** | **3. Predictive Models** | Tab 1: Cutoff Explorer (Default Cutoff $\tau = 0.50$) | `?view=predictive&tau=0.50` $\rightarrow$ Click Tab 1 | Model: Random Forest; Cutoff slider at 0.50. Metrics: Flagged Accounts = 296 (21.0%), Precision = 0.6858, Recall = 0.5428, F1 = 0.6060. Counts: TP=203, FN=171, FP=93, TN=942. | `03_predictive_models/03_threshold_explorer_default_tau_050.png` |
| **13** | **3. Predictive Models** | Tab 1: Cutoff Explorer (Optimal Cutoff $\tau = 0.33$) | `?view=predictive&tau=0.33` $\rightarrow$ Click Tab 1 | Model: Random Forest; Cutoff slider at 0.33. Metrics: Flagged Accounts = 482 (34.2%), Precision = 0.5788, Recall = 0.7460, F1 = 0.6519. Counts: TP=279, FN=95, FP=203, TN=832 (+76 churners caught!). | `03_predictive_models/04_threshold_explorer_optimal_tau_033.png` |
| **14** | **3. Predictive Models** | Tab 2: Model Explainability & Permutation Importance | `?view=predictive` $\rightarrow$ Click Tab 2 | Permutation feature importance horizontal chart (19 predictors), Logistic Regression odds ratios chart, and detailed side-by-side importance rankings table. | `03_predictive_models/05_permutation_importance_and_weights.png` |
| **15** | **3. Predictive Models** | Tab 3: Single Customer Scorer (High-Risk Profile) | `?view=predictive&profile=high_risk` $\rightarrow$ Tab 3 | Month-to-month, tenure 4 mo, fiber optic, no tech support, elec check. Scored Churn Probability: `79.43%` | Tier: `Tier 1: High Risk (p >= 0.50)` displayed in banner. | `03_predictive_models/06_single_customer_scorer_high_risk.png` |
| **16** | **3. Predictive Models** | Tab 3: Single Customer Scorer (Low-Risk Profile) | `?view=predictive&profile=low_risk` $\rightarrow$ Tab 3 | Two-year contract, tenure 60 mo, DSL, tech support, credit card. Scored Churn Probability: `2.14%` | Tier: `Tier 3: Low Risk (p < 0.33)` displayed in banner. | `03_predictive_models/07_single_customer_scorer_low_risk.png` |
| **17** | **3. Predictive Models** | Tab 3: Service Hierarchy Defensive Validation | `?view=predictive&profile=no_service` $\rightarrow$ Tab 3 | PhoneService="No", InternetService="No". Warning banners displayed: MultipleLines locked to "No phone service"; Internet add-ons locked to "No internet service". Dropdowns disabled. | `03_predictive_models/08_service_hierarchy_validation.png` |
| **18** | **4. Prescriptive** | Risk Tier Calibration & Cumulative Capacity Tables | `?view=prescriptive` (Top section) | Calibration table for Tiers 1-4 (Tier 1: 75.52% churn, Tier 4: 3.81% churn; monotonic separation); Capacity-ranked cumulative lift table from 10% to 100%. | `04_prescriptive_prioritization/01_risk_tiers_and_capacity_lift_tables.png` |
| **19** | **4. Prescriptive** | Prescriptive Targeting Lift & Gain Curves | `?view=prescriptive` (Scroll $y = 440\text{px}$) | Matplotlib cumulative gain & lift curves (`fig10_prescriptive_targeting_lift.png`) showing Top 30% reaches 73.0% of all churners ($2.43\times$ random lift). | `04_prescriptive_prioritization/02_prescriptive_targeting_lift_curve.png` |
| **20** | **4. Prescriptive** | Retention Simulator (Baseline 30% Policy) | `?view=prescriptive&cap=30&cost=15&save=20&horizon=6` | Sliders: Cap=30%, Cost=\$15, Save=20%, Horizon=6 mo. Metrics: Observed Churners Reached: `273 / 374` (73.0%), Contacted: `423`, Cost: `$6,345`, Net Value: `$19,531.08`. | `04_prescriptive_prioritization/03_retention_simulator_baseline_capacity_30pct.png` |
| **21** | **4. Prescriptive** | Retention Simulator (Aggressive 50% Expansion) | `?view=prescriptive&cap=50&cost=20&save=25&horizon=9` | Sliders: Cap=50%, Cost=\$20, Save=25%, Horizon=9 mo. Metrics: Observed Churners Reached: `331 / 374` (88.5%), Contacted: `705`, Cost: `$14,100`, Net Value: `$39,693.45`. | `04_prescriptive_prioritization/04_retention_simulator_aggressive_capacity_50pct.png` |
| **22** | **4. Prescriptive** | Traceable Retention Action Plan (REC-1 to REC-5) | `?view=prescriptive` (Scroll $y = 1150\text{px}$) | Comprehensive action plan table mapping REC-1 through REC-5 with target populations ($n=2,058$, $n=2,722$, $n=2,365$, $n=423$, $n=241$), intervention rationale, and governance. | `04_prescriptive_prioritization/05_traceable_recommendations_action_plan.png` |

---

## 3. Coverage Completeness Audit

- **Total Distinct Application Views:** 4 of 4 covered ($100\%$).
- **Total Interactive Tabs:** 7 of 7 covered ($100\%$).
- **Total User-Facing Sliders / Inputs Demonstrated:**
  - Contract, Internet, Payment, Senior, Tenure filters: Demonstrated.
  - Decision Cutoff ($\tau$) Explorer: Demonstrated ($\tau=0.50$ vs $\tau=0.33$).
  - Single Customer Scorer: High-risk, Low-risk, and Hierarchy-constrained demonstrated.
  - Retention Simulator: 30% Capacity baseline vs 50% Capacity expansion demonstrated.
- **Defensive & Quality Features:**
  - Service hierarchy validation banner: Demonstrated.
  - Simpson's paradox confounding audit: Demonstrated.
  - Explicit observational causality disclaimers: Demonstrated.
  - Wilson score confidence intervals: Demonstrated.
  - Assumption labeling on financial simulations: Demonstrated.
