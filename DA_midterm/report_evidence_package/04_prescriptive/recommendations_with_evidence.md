# Layer 4 — Prescriptive Recommendations Backed by Evidence (`04_prescriptive/`)

Each recommendation cites concrete statistics from Descriptive, Diagnostic, and Predictive outputs alongside explicit non-causal assumptions. `REC-4` (probability threshold `p >= 0.33`) and `REC-5` (budget-capped top-30% queue `p >= 0.3918`) are explicitly separated as distinct targeting policies.

## REC-1: Month-to-month subscribers in early tenure (1-12 months) [P1 (Highest Immediate Volume)]
- **Measured Segment Count & Scope:** `n = 1,994` (28.31% of `Full Sample Compound Subgroup (N=7,043)`)
- **Descriptive Evidence:** Month-to-month accounts span 3,875 customers (55.02% of base) at 42.71% churn (95% CI [41.16%, 44.27%]), accounting for 88.55% of all churn and $120,847.10/mo in historical monthly billing of churned records. The narrowed 1-12 mo subset (n=1,994, 28.31% of base) churns at 51.35% (1,024 churners = 54.79% of all churn).
- **Diagnostic Evidence:** Contract has the strongest categorical association with Churn (chi2=1184.6, Cramer's V=0.4101, Holm p=9.97e-257), followed by tenure_tier (V=0.3512). Controlling for covariates, Two-year contracts show adjusted OR=0.2602 vs Month-to-month.
- **Predictive Evidence:** Raw-column test permutation ranks Contract #1 (dROC-AUC=0.0428) and tenure #2 (dROC-AUC=0.0256). Test Tier 1 (p>=0.50, n=275) realizes 67.27% churn.
- **Proposed Action:** Launch structured first-90-day onboarding check-ins and test step-down annual contract migration incentives (e.g., locked rate or waived upgrade fee) specifically among Model Tier 1 & Tier 2 early-tenure accounts.
- **Assumptions & Caveats:** Assumes contract-migration incentives achieve an assumed 15-25% relative churn reduction without eroding net margin; IBM data is cross-sectional and does not test experimental discount elasticity.
- **Source Paths:** `01_descriptive/tables/descriptive_compound_segments.csv; 01_descriptive/tables/descriptive_contract_by_tenure.csv; 02_diagnostic/tables/diagnostic_categorical_associations.csv; 03_predictive/tables/permutation_importance.csv`

## REC-2: Fiber optic subscribers lacking OnlineSecurity or TechSupport [P1 (Highest Billing Exposure)]
- **Measured Segment Count & Scope:** `n = 2,722` (38.65% of `Full Sample Intersected Cohort (N=7,043)`)
- **Descriptive Evidence:** Within broad Fiber optic accounts (n=3,096, 41.89% churn, $114,300.05/mo historical churned billing), the narrowed target cohort lacking OnlineSecurity or TechSupport comprises n=2,722 accounts (38.65% of base) with 45.70% churn (95% CI [43.84%, 47.58%], 1,244 churners = 66.56% of all churn, $108,733.60/mo historical churned billing). Those lacking both add-ons (n=1,765) churn at 55.01% vs 14.17% for Fiber users with both (n=374).
- **Diagnostic Evidence:** OnlineSecurity (V=0.3474), TechSupport (V=0.3429), and InternetService (V=0.3225) rank 3rd-5th in association strength. Even after controlling for tenure and contract, Fiber optic retains adjusted OR=2.5646, whereas OnlineSecurity_Yes (OR=0.6913) and TechSupport_Yes (OR=0.7099) remain protective.
- **Predictive Evidence:** InternetService ranks #3 (dROC-AUC=0.0162), OnlineSecurity ranks #5, and TechSupport ranks #6 in held-out Random Forest permutation importance.
- **Proposed Action:** Audit Fiber optic service reliability/price perception and pilot bundled OnlineSecurity + priority TechSupport packages at no extra promotional cost for 3-6 months on Tier 1/2 Fiber accounts lacking both add-ons.
- **Assumptions & Caveats:** Assumes lack of add-ons reflects unaddressed perceived value rather than pure unmeasured customer stickiness bias (existing add-on holders may reflect self-selected loyal subscribers rather than causal add-on protection).
- **Source Paths:** `01_descriptive/tables/descriptive_compound_segments.csv; 01_descriptive/tables/descriptive_subgroups.csv; 02_diagnostic/tables/diagnostic_confounding_adjusted_odds.csv; 03_predictive/tables/permutation_importance.csv`

## REC-3: Electronic check manual payers [P2 (Billing & Payment Friction)]
- **Measured Segment Count & Scope:** `n = 2,365` (33.58% of `Full Sample Subgroup (N=7,043)`)
- **Descriptive Evidence:** Electronic check accounts (n=2,365, 33.58% of base) churn at 45.29% (95% CI [43.29%, 47.30%], $84,288.75/mo historical churned billing) vs 15.24% for Credit card automatic payers — accounting for 57.30% of all churn.
- **Diagnostic Evidence:** PaymentMethod shows strong bivariate dependence (chi2=648.1, V=0.3034, Holm p=4.42e-139). After controlling for contract, tenure, and charges, Electronic check retains an elevated adjusted OR=1.3601.
- **Predictive Evidence:** PaymentMethod ranks #7 (dROC-AUC=0.0022) in held-out test importance and helps separate Tier 2 Elevated Risk accounts (41.96% actual churn) from Tier 3 Low Risk.
- **Proposed Action:** Promote streamlined enrollment into automatic credit card or bank transfer autopay with small one-time billing credits paired with clear paperless payment reminders.
- **Assumptions & Caveats:** Assumes payment-method switching reduces accidental/bill-shock churn rather than merely selecting already loyal customers.
- **Source Paths:** `01_descriptive/tables/descriptive_subgroups.csv; 01_descriptive/figures/fig01_churn_by_contract_payment.png; 02_diagnostic/tables/diagnostic_confounding_adjusted_odds.csv`

## REC-4: Hold-out accounts exceeding CV F1-optimal cutoff (p >= 0.33) [P2 (Threshold Classification Policy)]
- **Measured Segment Count & Scope:** `n = 499` (35.42% of `Held-Out Test Probability Threshold (n=1,409)`)
- **Descriptive Evidence:** Baseline full-sample churn is 26.54% (n=1,869 / 7,043) with $139,130.85/mo historical billing across churned records (30.50% of total monthly billing); untargeted outreach wastes 73.46% of contacts on non-churners.
- **Diagnostic Evidence:** Multivariate churn risk spans Contract (V=0.4101), tenure_tier (V=0.3512), OnlineSecurity (V=0.3474), and PaymentMethod (V=0.3034); a calibrated probability threshold integrates all risk factors simultaneously without arbitrary single-variable exclusions.
- **Predictive Evidence:** Random Forest (Test ROC-AUC=0.8440, PR-AUC=0.6513, Brier=0.1361) at CV F1-optimal cutoff tau=0.33 flags n=499/1,409 (35.42%) test accounts (Tier 1 p>=0.50: n=275, 67.27% realized churn; Tier 2 0.33<=p<0.50: n=224, 41.96% churn), capturing 74.60% of test churners (279/374) at 55.91% precision (F1=0.6392) vs Tier 3 Low Risk (10.44% churn).
- **Proposed Action:** Use probability-threshold triage when outreach budget scales to ~35% of base: route Tier 1 (p>=0.50) to high-touch agent outreach, Tier 2 (0.33<=p<0.50) to automated digital offers, and exclude Tier 3 (p<0.33).
- **Assumptions & Caveats:** Distinct from a fixed Top-30% budget queue (see REC-5). Model trained on fictional cross-sectional snapshot; live deployment requires A/B uplift validation and periodic calibration monitoring.
- **Source Paths:** `03_predictive/tables/model_test_comparison.csv; 03_predictive/tables/test_predictions.csv; 04_prescriptive/tables/prescriptive_risk_tiers.csv`

## REC-5: Top 30% capacity-ranked risk queue (empirical test cutoff p >= 0.3918) [P2 (Budget-Capped Queue Policy)]
- **Measured Segment Count & Scope:** `n = 423` (30.02% of `Held-Out Test Capacity Queue (n=1,409)`)
- **Descriptive Evidence:** In the full snapshot, churned records carry $139,130.85/mo in historical monthly charges ($64.76 avg across all vs $74.44 among churned), making volume-capped prioritization critical when retention team capacity is strictly budgeted below the 35.42% F1-threshold share.
- **Diagnostic Evidence:** High-risk concentration within short-tenure Fiber and Month-to-month segments creates steep diminishing marginal risk in the bottom 70% of accounts, supporting ranked queue ordering by calibrated churn probability.
- **Predictive Evidence:** Ranking the sealed 1,409 test accounts by Random Forest probability selects n=423 (30.02% capacity, min predicted p=0.3918), capturing 246/374 (65.78%) test churners at 58.16% precision (2.19x lift over random) and covering $18,907.85/mo (69.48% of the $27,214.90/mo historical churned billing in test).
- **Proposed Action:** When outreach team capacity is fixed at <=30% of accounts (~2,113 seats if scaled proportionally across a 7,043-customer base as an illustrative benchmark), rank customers descending by predicted probability and contact the top-30% queue rather than using the looser 0.33 cutoff.
- **Assumptions & Caveats:** Observed lift (2.19x) is measured strictly on n=423/1,409 held-out test records; illustrative 6-mo net financial scenarios ($15-$25 cost, 10%-30% save rate) depend on untested causal uplift assumptions.
- **Source Paths:** `04_prescriptive/tables/prescriptive_capacity_lift.csv; 04_prescriptive/tables/prescriptive_scenario_sensitivity.csv; 04_prescriptive/figures/fig10_prescriptive_targeting_lift.png`
