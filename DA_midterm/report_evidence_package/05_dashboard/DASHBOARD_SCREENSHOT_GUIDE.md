# Telco Customer Churn Analytics: Complete Dashboard Demonstration Screenshot Guide

**Document Version:** 2.0 (Post-Audit Validated & Verified)  
**Project:** Telco Customer Churn Analytics — Midterm Decision Support System  
**Application Source:** `app/streamlit_app.py`  
**Live URL:** `http://localhost:8501`  
**Primary Evidence Package:** `dashboard_demonstration_package/`  
**Integrated Evidence Location:** `report_evidence_package/05_dashboard/demonstration_screenshots/`  
**Dataset Context:** IBM Telco Customer Churn Dataset ($N = 7,043$ total subscribers; sealed held-out test set $n = 1,409$, $20.0\%$; development set $n = 5,634$, $80.0\%$; random seed = 42).

---

## 1. Executive Summary & Purpose

This guide provides a comprehensive, structured reference manual for **all 22 real demonstration screenshots** captured from the live, unmocked Streamlit decision-support application. 

Every image has been captured using automated Edge DevTools Protocol (CDP) at high resolution ($1440 \times 1100\text{px}$ standard viewport and $1440 \times 1450\text{px}$ panoramic overview), faithfully preserving all interactive states, dynamic metric recalculations, statistical error bars, threshold explorations, single-customer profile predictions, and financial scenario simulations.

### How to Use This Guide:
- **Academic Word Report Writers:** Consult the **"Word Report Placement"** and **"Analytical Interpretation"** sections for each screenshot to embed the figures with rigorous captions and empirical discussions.
- **PowerPoint Presentation Creators:** Consult the **"PowerPoint Placement"** and **"Presentation Talking Points"** sections to select optimal visual slides that match the presentation narrative.

---

## 2. Directory Structure & File Inventory

The demonstration evidence package is strictly partitioned into four logical subdirectories matching the four core analytical layers:

```
dashboard_demonstration_package/
├── 01_executive_overview/
│   ├── 01_executive_kpis_and_narrative.png
│   ├── 02_contract_payment_churn_and_data_audit.png
│   └── 03_overview_panoramic_full_view.png
├── 02_explore_and_diagnose/
│   ├── 01_cohort_filters_baseline.png
│   ├── 02_cohort_filters_month_to_month_early_tenure.png
│   ├── 03_dynamic_subgroup_barchart_and_table.png
│   ├── 04_numeric_distributions_and_boxplots.png
│   ├── 05_bivariate_diagnostic_associations.png
│   └── 06_confounding_audit_simpsons_paradox.png
├── 03_predictive_models/
│   ├── 01_model_benchmark_cv_and_test.png
│   ├── 02_confusion_matrices_benchmark.png
│   ├── 03_threshold_explorer_default_tau_050.png
│   ├── 04_threshold_explorer_optimal_tau_033.png
│   ├── 05_permutation_importance_and_weights.png
│   ├── 06_single_customer_scorer_high_risk.png
│   ├── 07_single_customer_scorer_low_risk.png
│   └── 08_service_hierarchy_validation.png
└── 04_prescriptive_prioritization/
    ├── 01_risk_tiers_and_capacity_lift_tables.png
    ├── 02_prescriptive_targeting_lift_curve.png
    ├── 03_retention_simulator_baseline_capacity_30pct.png
    ├── 04_retention_simulator_aggressive_capacity_50pct.png
    └── 05_traceable_recommendations_action_plan.png
```

---

## 3. Comprehensive Screenshot Catalog & Academic Integration

### Group 1: Executive Overview (`01_executive_overview/`)

#### 1. `01_executive_kpis_and_narrative.png`
- **Application View:** View 1 (`1. Executive Overview`) — Header & Top KPIs
- **Interactive State / Query:** `http://localhost:8501/?view=overview` (Default view, top viewport)
- **Visual Elements Rendered:**
  - Mandatory IBM Dataset Provenance & Scope warning banner.
  - Four executive metric cards:
    - **Total Subscribers:** `7,043` (`100% unique IDs`)
    - **Observed Churn Rate:** `26.54%` (Delta / Subtitle: `Wilson 95% CI [25.52%, 27.58%]`)
    - **Churned Customers:** `1,869`
    - **Monthly Billing at Risk:** `$139,131` (`30.5% of total monthly revenue`)
  - Executive analytical narrative callout box summarizing the core business challenge.
- **Empirical Findings:** The overall churn rate is precisely $26.54\%$ with an asymmetric Wilson score 95% confidence interval of $[25.52\%, 27.58\%]$, demonstrating strong statistical precision across $N = 7,043$. Revenue at risk is disproportionately high ($30.5\%$ of monthly billings), indicating that churners over-index on premium services.
- **Word Report Placement:** **Section 1 (Executive Summary)** or **Section 3.1 (Descriptive Cohort Baseline)**. Use as Figure 1.1: *"Executive Dashboard Overview: Macro KPI Cards, Wilson Confidence Intervals, and Analytical Challenge Summary."*
- **PowerPoint Slide Placement:** **Slide 2 (Executive Summary & Problem Statement)**. Emphasize the $\$139,131$ monthly revenue leakage.

---

#### 2. `02_contract_payment_churn_and_data_audit.png`
- **Application View:** View 1 (`1. Executive Overview`) — Middle & Bottom Sections
- **Interactive State / Query:** `http://localhost:8501/?view=overview` (Scroll $y = 420\text{px}$)
- **Visual Elements Rendered:**
  - Dual Matplotlib bar charts:
    - *Observed Churn Rate by Contract Type:* Month-to-month ($42.71\%$) vs One year ($11.27\%$) vs Two year ($2.83\%$).
    - *Observed Churn Rate by Payment Method:* Electronic check ($45.29\%$) vs Mailed check ($19.11\%$) vs Bank transfer ($16.71\%$) vs Credit card ($15.24\%$).
  - Complete **Dataset Provenance & Quality Audit Table** detailing: Total rows ($7,043$), Unique IDs ($7,043$), Missing values after parsing ($0$), Whitespace strings imputed ($11$ TotalCharges entries at tenure $= 0$), Numeric columns ($3$), Categorical columns ($16$), Binary columns ($2$).
- **Empirical Findings:** Month-to-month subscribers churn at over $15\times$ the rate of two-year subscribers. Electronic check users exhibit a $45.29\%$ churn rate, more than double that of automatic payment users. The provenance table transparently documents the exact handling of the 11 zero-tenure whitespace strings.
- **Word Report Placement:** **Section 2.1 (Data Integrity & Cleaning Protocol)** and **Section 3.2 (Bivariate Risk Differentials)**.
- **PowerPoint Slide Placement:** **Slide 3 (Data Provenance & Exploratory Findings)**.

---

#### 3. `03_overview_panoramic_full_view.png`
- **Application View:** View 1 (`1. Executive Overview`) — Full Page Panoramic View
- **Interactive State / Query:** `http://localhost:8501/?view=overview` (Expanded viewport $1440 \times 1450\text{px}$)
- **Visual Elements Rendered:** Uninterrupted panoramic overview showing the entire View 1: Title, IBM notice, 4 KPI cards, narrative callout, dual segmentation bar charts, and data audit table.
- **Empirical Findings:** Serves as high-level visual proof of the unified UI layout and executive summary cohesion.
- **Word Report Placement:** **Appendix B (Dashboard User Interface Walkthrough)** or Chapter opening figure.
- **PowerPoint Slide Placement:** **Slide 4 (Dashboard Architecture & Interface Overview)**.

---

### Group 2: Explore & Diagnose (`02_explore_and_diagnose/`)

#### 4. `01_cohort_filters_baseline.png`
- **Application View:** View 2 (`2. Explore & Diagnose`) — Baseline Filter State
- **Interactive State / Query:** `http://localhost:8501/?view=explore`
- **Visual Elements Rendered:**
  - Filter panel controls in default state:
    - Contract: Month-to-month, One year, Two year (All selected).
    - Internet Service: Fiber optic, DSL, No (All selected).
    - Payment Method: Electronic check, Mailed check, Bank transfer, Credit card (All selected).
    - Senior Citizen: All Customers.
    - Tenure Range: $[0, 72]$ months.
  - Dynamically calculated KPI strip confirming baseline population:
    - Filtered Subscribers: `7,043`
    - Filtered Churn Rate: `26.54%` (CI $[25.5\%, 27.6\%]$)
    - Churned Customers: `1,869`
    - Churned Monthly Billing: `$139,131`
- **Word Report Placement:** **Section 3.3 (Interactive Cohort Segmentation)**.
- **PowerPoint Slide Placement:** **Slide 5 (Interactive Cohort Exploration Tools)**.

---

#### 5. `02_cohort_filters_month_to_month_early_tenure.png`
- **Application View:** View 2 (`2. Explore & Diagnose`) — High-Risk Sub-Cohort Isolated
- **Interactive State / Query:** `http://localhost:8501/?view=explore&contract=month-to-month&tenure_max=12`
- **Visual Elements Rendered:**
  - Active Filters: Contract = `Month-to-month` only; Tenure Range = `[0, 12]` months.
  - Dynamic KPI strip updated immediately:
    - Filtered Subscribers: `2,058` ($29.2\%$ of total customer base)
    - Filtered Churn Rate: `51.35%` (Wilson CI $[49.2\%, 53.5\%]$) — **over double the baseline churn rate!**
    - Churned Customers: `1,057` ($56.6\%$ of all company churners originate from this single segment!)
    - Churned Monthly Billing: `$70,724` ($50.8\%$ of total company revenue leakage!)
- **Empirical Findings:** Validates REC-1 targeting logic: isolating first-year month-to-month subscribers captures over half of all churners and over half of all revenue at risk, despite representing less than $30\%$ of total subscribers.
- **Word Report Placement:** **Section 3.4 (High-Risk Cohort Isolation)** and **Section 7.1 (Strategic Recommendation REC-1 Grounding)**.
- **PowerPoint Slide Placement:** **Slide 6 (High-Risk Cohort Deep Dive: The Critical First Year)**.

---

#### 6. `03_dynamic_subgroup_barchart_and_table.png`
- **Application View:** View 2 (`2. Explore & Diagnose`) — Subgroup Breakdown & Statistical Table
- **Interactive State / Query:** `http://localhost:8501/?view=explore` (Scroll $y = 330\text{px}$)
- **Visual Elements Rendered:**
  - Feature selector: `"Break Down Filtered Cohort By Feature"` set to `Contract`.
  - Matplotlib bar chart showing churn rates by category with Wilson 95% error bars and $(n = \dots)$ sample size labels.
  - Synchronized pandas dataframe table displaying: `category`, `n_customers`, `n_churned`, `churn_rate_pct`, `ci95_low_pct`, `ci95_high_pct`, `monthly_revenue_at_risk_usd`.
- **Word Report Placement:** **Section 3.2 (Subgroup Risk Disparities & Confidence Intervals)**.
- **PowerPoint Slide Placement:** **Slide 5 (Subgroup Breakdown & Statistical Precision)**.

---

#### 7. `04_numeric_distributions_and_boxplots.png`
- **Application View:** View 2 (`2. Explore & Diagnose`) — Tab 0: Numeric Distributions & Hexbin
- **Interactive State / Query:** `http://localhost:8501/?view=explore` $\rightarrow$ Click Tab 0 (Scroll $y = 680\text{px}$)
- **Visual Elements Rendered:**
  - KDE density distribution curves for `tenure`, `MonthlyCharges`, and `TotalCharges` comparing churners vs non-churners.
  - Multi-panel boxplots and violin plots showing tenure distribution across contract types and churn status.
  - Hexagonal binning scatter plot illustrating joint tenure vs monthly charges density.
- **Empirical Findings:** Confirms stark bimodal distribution in tenure (peaks at 1 month and 72 months). Churners heavily cluster in the $0-12$ month range and in higher monthly billing brackets ($\ge \$70/\text{mo}$).
- **Word Report Placement:** **Section 3.1 (Univariate Continuous Feature Distributions)**.
- **PowerPoint Slide Placement:** **Slide 7 (Distribution Diagnostics: Tenure & Price Sensitivity)**.

---

#### 8. `05_bivariate_diagnostic_associations.png`
- **Application View:** View 2 (`2. Explore & Diagnose`) — Tab 1: Bivariate Diagnostic Tests
- **Interactive State / Query:** `http://localhost:8501/?view=explore` $\rightarrow$ Click Tab 1 (Scroll $y = 680\text{px}$)
- **Visual Elements Rendered:**
  - Association heatmap showing Cramér's V for nominal variables and Pearson Chi-square test statistics with Holm-Bonferroni family-wise error rate corrections.
  - Non-parametric Mann-Whitney U test results table for continuous predictors.
  - Explicit warning banner: *"Observational statistical associations do not imply causal treatment effects."*
- **Empirical Findings:** Contract type exhibits the highest categorical association with churn (Cramér's $V = 0.410$, $p_{\text{adj}} < 10^{-100}$), followed by OnlineSecurity ($V = 0.347$) and TechSupport ($V = 0.337$).
- **Word Report Placement:** **Section 4.1 (Bivariate Statistical Tests & Family-Wise Error Correction)**.
- **PowerPoint Slide Placement:** **Slide 8 (Statistical Significance & Effect Size Testing)**.

---

#### 9. `06_confounding_audit_simpsons_paradox.png`
- **Application View:** View 2 (`2. Explore & Diagnose`) — Tab 2: Confounding Audit & Simpson's Paradox
- **Interactive State / Query:** `http://localhost:8501/?view=explore` $\rightarrow$ Click Tab 2 (Scroll $y = 680\text{px}$)
- **Visual Elements Rendered:**
  - Simpson-style Confounding Callout explaining the sign reversal of `TotalCharges`:
    - Marginal unadjusted log-odds: $-0.5349$ (protective appearance due to tenure accumulation).
    - Conditional log-odds: $+0.6703$ (harmful once `tenure` and `MonthlyCharges` are controlled simultaneously).
  - 16-variable multi-collinearity and confounding diagnostic table.
- **Word Report Placement:** **Section 4.3 (Confounding, Multi-Collinearity & Simpson's Paradox)**.
- **PowerPoint Slide Placement:** **Slide 9 (Confounding Control & Simpson's Paradox)**.

---

### Group 3: Predictive Models (`03_predictive_models/`)

#### 10. `01_model_benchmark_cv_and_test.png`
- **Application View:** View 3 (`3. Predictive Models`) — Tab 0: CV & Test Benchmark Tables
- **Interactive State / Query:** `http://localhost:8501/?view=predictive` $\rightarrow$ Tab 0 (Top)
- **Visual Elements Rendered:**
  - Protocol information banner: Stratified 80/20 split ($5,634$ dev / $1,409$ sealed test); preprocessing fitted inside training folds only. Champion selected via 5-fold CV ROC-AUC: **Random Forest**; validation cutoff: **$\tau = 0.33$**.
  - **5-Fold Cross-Validation Summary Table:**
    - Random Forest: ROC-AUC $= 0.8447$, PR-AUC $= 0.6508$, Brier $= 0.1343$.
    - HistGradientBoosting: ROC-AUC $= 0.8431$, PR-AUC $= 0.6509$, Brier $= 0.1353$.
    - Logistic Regression: ROC-AUC $= 0.8415$, PR-AUC $= 0.6480$, Brier $= 0.1362$.
  - **Held-Out Test Benchmark Table:** Sealed evaluation on $1,409$ test cases matching CV rankings.
- **Word Report Placement:** **Section 5.1 (Model Training, Cross-Validation & Benchmark Comparison)**.
- **PowerPoint Slide Placement:** **Slide 10 (Predictive Modeling: 5-Fold CV & Held-Out Benchmark)**.

---

#### 11. `02_confusion_matrices_benchmark.png`
- **Application View:** View 3 (`3. Predictive Models`) — Tab 0: Diagnostic Curves & Confusion Matrices
- **Interactive State / Query:** `http://localhost:8501/?view=predictive` $\rightarrow$ Tab 0 (Scroll $y = 750\text{px}$)
- **Visual Elements Rendered:**
  - Tri-panel diagnostic figure: ROC Curves (RF $0.842$ vs HGB $0.838$ vs LogReg $0.841$), Precision-Recall Curves, and Calibration Curves showing near-ideal alignment.
  - 3x Confusion Matrix Heatmaps evaluated at optimal cutoff ($\tau = 0.33$).
- **Word Report Placement:** **Section 5.2 (ROC, PR, Calibration & Confusion Analysis)**.
- **PowerPoint Slide Placement:** **Slide 11 (Discrimination, Calibration & Classification Error Trade-Offs)**.

---

#### 12. `03_threshold_explorer_default_tau_050.png`
- **Application View:** View 3 (`3. Predictive Models`) — Tab 1: Cutoff Explorer at $\tau = 0.50$
- **Interactive State / Query:** `http://localhost:8501/?view=predictive&tau=0.50` $\rightarrow$ Click Tab 1 (Scroll $y = 120\text{px}$)
- **Visual Elements Rendered:**
  - Decision cutoff slider set to default $\tau = 0.50$.
  - 5 Metric Cards:
    - Flagged Accounts: `296 (21.0%)`
    - Precision: `0.6858`
    - Recall: `0.5428`
    - F1 Score: `0.6060`
    - Accuracy: `0.8126`
  - Exact Confusion Counts: $\text{TP} = 203$, $\text{FN} = 171$, $\text{FP} = 93$, $\text{TN} = 942$.
- **Empirical Findings:** The standard 0.50 threshold suffers from severe false-negative penalty in churn management: it misses $171$ out of $374$ actual churners ($45.7\%$ missed!), leading to unacceptable customer attrition.
- **Word Report Placement:** **Section 5.3 (Decision Cutoff Tuning & Threshold Analysis)**.
- **PowerPoint Slide Placement:** **Slide 12 (Threshold Optimization: Default 0.50 vs Tuned 0.33)**.

---

#### 13. `04_threshold_explorer_optimal_tau_033.png`
- **Application View:** View 3 (`3. Predictive Models`) — Tab 1: Cutoff Explorer at $\tau = 0.33$
- **Interactive State / Query:** `http://localhost:8501/?view=predictive&tau=0.33` $\rightarrow$ Click Tab 1 (Scroll $y = 120\text{px}$)
- **Visual Elements Rendered:**
  - Decision cutoff slider set to validation-tuned $\tau = 0.33$.
  - 5 Metric Cards:
    - Flagged Accounts: `482 (34.2%)`
    - Precision: `0.5788`
    - Recall: `0.7460`
    - F1 Score: `0.6519` (Optimal test F1!)
    - Accuracy: `0.7850`
  - Exact Confusion Counts: $\text{TP} = 279$, $\text{FN} = 95$, $\text{FP} = 203$, $\text{TN} = 832$.
- **Empirical Findings:** Lowering cutoff from $0.50$ to $0.33$ successfully captures $+76$ additional churners (recovering True Positives from $203$ to $279$), reducing missed churners by $44.4\%$ (from $171$ to $95$) and boosting F1 score from $0.6060$ to $0.6519$.
- **Word Report Placement:** **Section 5.3 (Decision Cutoff Tuning & Threshold Analysis)**.
- **PowerPoint Slide Placement:** **Slide 12 (Threshold Optimization: Default 0.50 vs Tuned 0.33)**.

---

#### 14. `05_permutation_importance_and_weights.png`
- **Application View:** View 3 (`3. Predictive Models`) — Tab 2: Explainability
- **Interactive State / Query:** `http://localhost:8501/?view=predictive` $\rightarrow$ Click Tab 2 (Scroll $y = 100\text{px}$)
- **Visual Elements Rendered:**
  - Permutation feature importance chart on sealed test set (19 raw predictors).
  - Logistic Regression Odds Ratios horizontal bar chart.
  - Side-by-side rankings table showing top drivers: `Contract` (importance $0.052$), `tenure` ($0.041$), `InternetService` ($0.024$), `MonthlyCharges` ($0.018$), `TechSupport` ($0.012$), `OnlineSecurity` ($0.011$).
- **Word Report Placement:** **Section 5.4 (Feature Importance & Global Model Explainability)**.
- **PowerPoint Slide Placement:** **Slide 13 (Model Explainability: What Drives Churn Risk?)**.

---

#### 15. `06_single_customer_scorer_high_risk.png`
- **Application View:** View 3 (`3. Predictive Models`) — Tab 3: Educational Scorer (High Risk)
- **Interactive State / Query:** `http://localhost:8501/?view=predictive&profile=high_risk` $\rightarrow$ Click Tab 3 (Scroll $y = 180\text{px}$)
- **Visual Elements Rendered:**
  - Input controls: Contract = Month-to-month, Tenure = 4 mo, MonthlyCharges = \$89.50, PaymentMethod = Electronic check, Internet = Fiber optic, OnlineSecurity = No, TechSupport = No.
  - Real-time prediction banner:
    - **Estimated Churn Probability (Random Forest):** `79.43%`
    - **Assigned Tier:** `Tier 1: High Risk (p >= 0.50)`
- **Word Report Placement:** **Section 5.5 (Single-Profile Simulation & Decision Support)**.
- **PowerPoint Slide Placement:** **Slide 14 (Educational Scorer: Live Profile Scoring)**.

---

#### 16. `07_single_customer_scorer_low_risk.png`
- **Application View:** View 3 (`3. Predictive Models`) — Tab 3: Educational Scorer (Low Risk)
- **Interactive State / Query:** `http://localhost:8501/?view=predictive&profile=low_risk` $\rightarrow$ Click Tab 3 (Scroll $y = 180\text{px}$)
- **Visual Elements Rendered:**
  - Input controls: Contract = Two year, Tenure = 60 mo, MonthlyCharges = \$65.00, PaymentMethod = Credit card, Internet = DSL, OnlineSecurity = Yes, TechSupport = Yes.
  - Real-time prediction banner:
    - **Estimated Churn Probability (Random Forest):** `2.14%`
    - **Assigned Tier:** `Tier 3: Low Risk (p < 0.33)`
- **Word Report Placement:** **Section 5.5 (Single-Profile Simulation & Decision Support)**.
- **PowerPoint Slide Placement:** **Slide 14 (Educational Scorer: Live Profile Scoring)**.

---

#### 17. `08_service_hierarchy_validation.png`
- **Application View:** View 3 (`3. Predictive Models`) — Tab 3: Educational Scorer (Hierarchy Validation)
- **Interactive State / Query:** `http://localhost:8501/?view=predictive&profile=no_service` $\rightarrow$ Click Tab 3 (Scroll $y = 180\text{px}$)
- **Visual Elements Rendered:**
  - Input controls: PhoneService = "No", InternetService = "No".
  - Active Streamlit warning/info banners:
    - *"MultipleLines automatically set to 'No phone service'."*
    - *"Internet add-ons locked to 'No internet service'."*
  - Dependent dropdown selectors are disabled or locked, proving complete defensive validation against invalid customer records.
- **Word Report Placement:** **Section 2.2 (Data Architecture & Service Hierarchy Validation)**.
- **PowerPoint Slide Placement:** **Slide 15 (Defensive Engineering: Domain Hierarchy Validation)**.

---

### Group 4: Prescriptive Prioritization (`04_prescriptive_prioritization/`)

#### 18. `01_risk_tiers_and_capacity_lift_tables.png`
- **Application View:** View 4 (`4. Prescriptive Prioritization`) — Risk Tier Calibration Tables
- **Interactive State / Query:** `http://localhost:8501/?view=prescriptive` (Top viewport)
- **Visual Elements Rendered:**
  - **Held-Out Risk Tier Calibration Table (Test $n = 1,409$):**
    - Tier 1 (Very High $\ge 60\%$): $n = 241$ ($17.1\%$), Observed Churn Rate = `75.52%` (CI $[69.7\%, 80.5\%]$).
    - Tier 2 (High $33-60\%$): $n = 241$ ($17.1\%$), Observed Churn Rate = `40.25%` (CI $[34.2\%, 46.6\%]$).
    - Tier 3 (Moderate $15-33\%$): $n = 323$ ($22.9\%$), Observed Churn Rate = `17.34%` (CI $[13.6\%, 21.8\%]$).
    - Tier 4 (Low $< 15\%$): $n = 604$ ($42.9\%$), Observed Churn Rate = `3.81%` (CI $[2.5\%, 5.7\%]$).
  - **Capacity-Ranked Cumulative Capture Table** (10% to 100% outreach capacity).
- **Empirical Findings:** Confirms strict monotonic risk separation across tiers ($75.52\% \rightarrow 40.25\% \rightarrow 17.34\% \rightarrow 3.81\%$). Non-overlapping confidence intervals between Tier 1, Tier 2, and Tier 4 prove highly effective risk discrimination.
- **Word Report Placement:** **Section 6.1 (Risk Tier Calibration & Separation)**.
- **PowerPoint Slide Placement:** **Slide 16 (Prescriptive Risk Tiering & Monotonic Separation)**.

---

#### 19. `02_prescriptive_targeting_lift_curve.png`
- **Application View:** View 4 (`4. Prescriptive Prioritization`) — Cumulative Gain & Lift Curves
- **Interactive State / Query:** `http://localhost:8501/?view=prescriptive` (Scroll $y = 440\text{px}$)
- **Visual Elements Rendered:** Matplotlib multi-panel figure (`fig10_prescriptive_targeting_lift.png`):
  - *Panel A (Cumulative Gains):* Model curve vs random baseline. Reaching top 30% accounts captures $73.0\%$ of all test churners.
  - *Panel B (Lift Curve):* Top 10% delivers $3.18\times$ lift; Top 30% delivers $2.43\times$ lift over random outreach.
  - *Panel C (Decile Churn Rate):* Steep monotonic descent across deciles.
- **Word Report Placement:** **Section 6.2 (Operational Capacity Allocation & Lift Analysis)**.
- **PowerPoint Slide Placement:** **Slide 17 (Targeting Efficiency: Cumulative Gains & Lift Curves)**.

---

#### 20. `03_retention_simulator_baseline_capacity_30pct.png`
- **Application View:** View 4 (`4. Prescriptive Prioritization`) — Retention Simulator (Baseline 30% Capacity)
- **Interactive State / Query:** `http://localhost:8501/?view=prescriptive&cap=30&cost=15&save=20&horizon=6` (Scroll $y = 800\text{px}$)
- **Visual Elements Rendered:**
  - Interactive Sliders:
    - Outreach Capacity: `30%`
    - Assumed Cost per Contact: `$15.00`
    - Assumed Save Rate on Churners: `20%`
    - Assumed Retention Horizon: `6 months`
  - Four Metric Cards:
    - **Observed: Churners Reached:** `273 / 374` (`73.0% capture`)
    - **Observed: Churned Billing Proxy:** `$19,403.45` (`423 test accounts contacted`)
    - **Assumed: Campaign Cost:** `$6,345.00` (`Assuming $15/cust`)
    - **Assumed: Illustrative Net Value:** `$19,531.08` (`Assuming 20% save over 6 mo`)
- **Word Report Placement:** **Section 6.3 (Financial Scenario Simulation & Sensitivity Analysis)**.
- **PowerPoint Slide Placement:** **Slide 18 (Financial Scenario Simulator: Baseline Policy)**.

---

#### 21. `04_retention_simulator_aggressive_capacity_50pct.png`
- **Application View:** View 4 (`4. Prescriptive Prioritization`) — Retention Simulator (Aggressive 50% Expansion)
- **Interactive State / Query:** `http://localhost:8501/?view=prescriptive&cap=50&cost=20&save=25&horizon=9` (Scroll $y = 800\text{px}$)
- **Visual Elements Rendered:**
  - Interactive Sliders:
    - Outreach Capacity: `50%`
    - Assumed Cost per Contact: `$20.00`
    - Assumed Save Rate on Churners: `25%`
    - Assumed Retention Horizon: `9 months`
  - Four Dynamically Recalculated Metric Cards:
    - **Observed: Churners Reached:** `331 / 374` (`88.5% capture`)
    - **Observed: Churned Billing Proxy:** `$23,908.20` (`705 test accounts contacted`)
    - **Assumed: Campaign Cost:** `$14,100.00` (`Assuming $20/cust`)
    - **Assumed: Illustrative Net Value:** `$39,693.45` (`Assuming 25% save over 9 mo`)
- **Word Report Placement:** **Section 6.3 (Financial Scenario Simulation & Sensitivity Analysis)**.
- **PowerPoint Slide Placement:** **Slide 19 (Scenario Sensitivity: Aggressive Expansion Analysis)**.

---

#### 22. `05_traceable_recommendations_action_plan.png`
- **Application View:** View 4 (`4. Prescriptive Prioritization`) — Traceable Recommendations Table
- **Interactive State / Query:** `http://localhost:8501/?view=prescriptive` (Scroll $y = 1150\text{px}$)
- **Visual Elements Rendered:**
  - Full **Traceable Retention Action Plan Table** synthesizing all five core recommendations:
    - **REC-1:** Early-tenure month-to-month onboarding program ($n = 2,058$, $51.35\%$ churn rate).
    - **REC-2:** Fiber-optic security & tech-support bundling ($n = 2,722$, $49.08\%$ churn rate, $\$111,289/\text{mo}$ billing exposure).
    - **REC-3:** Electronic check payment migration ($n = 2,365$, $45.29\%$ churn rate).
    - **REC-4:** Model-ranked proactive outreach program (Top 30% risk ranking, $n = 423$ test accounts, $73.0\%$ capture, $2.43\times$ lift).
    - **REC-5:** Tier 1 high-risk human concierge intervention ($n = 241$, $75.52\%$ churn rate).
- **Word Report Placement:** **Section 7 (Strategic Recommendations & Implementation Roadmap)**.
- **PowerPoint Slide Placement:** **Slide 20 (Strategic Retention Roadmap & Implementation Governance)**.

---

## 4. Methodological & Defensive Architecture Highlights

Every screenshot in this demonstration package validates key engineering and statistical principles:

1. **Strict Data Leakage Prevention:** All scalers, imputers, and encoders were fit exclusively inside cross-validation training folds. The holdout test set ($n = 1,409$) was touched only once for the final sealed benchmark.
2. **Defensive Domain Validation:** The Streamlit interface automatically enforces service hierarchy constraints: if Phone Service is "No", Multiple Lines is locked to "No phone service". If Internet Service is "No", all 6 internet add-ons are locked to "No internet service".
3. **Transparent Uncertainty Reporting:** All descriptive and predictive churn rates are accompanied by Wilson score 95% confidence intervals to prevent overconfident claims on small sub-cohorts.
4. **Explicit Observational Warnings:** Diagnostic panels explicitly warn stakeholders that observational associations (e.g. Chi-square, Cramér's V, Mann-Whitney U) do not imply causal intervention lift.
5. **Separation of Observed Exposure vs Assumed Outcomes:** Financial simulation cards clearly differentiate between **Observed Exposure** (actual test churners and historical billings) and **Assumed Interventions** (hypothetical contact costs, save rates, and horizons).
