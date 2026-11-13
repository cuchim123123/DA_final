# Comprehensive Results & Interpretation Guide (`RESULTS_AND_INTERPRETATION_GUIDE.md`)

> **For the Report-Writing AI Assistant:** Every count, rate, confidence interval, test statistic, model score, and recommendation metric below was computed from the actual execution of the `Telco-Customer-Churn.csv` analytical pipeline. Monetary totals on `Churn = Yes` rows reflect historical monthly billing in churned snapshot records, not verified future lost revenue or causal savings.

---

# Layer 1 — Descriptive Analytics Findings (`01_descriptive/`)

- **Population & Target Composition:** `7,043` subscribers, of whom `1,869` churned (**`26.54%`**, 95% Wilson CI `[25.52%, 27.58%]`) and `5,174` stayed (`73.46%`).
- **Disproportionate Monthly Churned Billing Proxy (`monthly_revenue_at_risk_usd`):** Total snapshot billing across all records is `$456,116.60/mo`, of which **`$139,130.85/mo` (`30.50%`)** is summed from records labeled `Churn = Yes` — higher than their `26.54%` headcount share because churners carry higher median monthly bills (`$79.65` vs `$64.42`). *(Note: this metric is a static monthly billing-exposure proxy across churned accounts, not verified future multi-month revenue lost.)*
- **Contract Concentration (`descriptive_subgroups.csv`, `fig01`):** `Month-to-month` accounts (`n=3,875`, `55.02%` of base) experience `42.71%` churn, contributing **`88.55%`** of all churners (`$120,847.10/mo` historical churned billing), compared with `11.27%` on `One year` (`n=1,473`) and `2.83%` on `Two year` (`n=1,695`).
- **Early-Tenure Cliff (`fig02`, `fig04`, `fig06`):** Customers in months `1-12` (`n=2,175`) churn at `47.68%` (`55.48%` of all churn), vs `9.51%` in `49-72 mo` (`n=2,239`). Within the compound segment `Month-to-month AND 1-12 mo` (`n=1,994`), churn peaks at **`51.35%`**.
- **Broad vs Intersected Fiber & Add-On Patterns (`descriptive_subgroups.csv`, `descriptive_compound_segments.csv`):** Broad `Fiber optic` accounts (`n=3,096`) churn at `41.89%` (`$114,300.05/mo` historical churned billing) vs `18.96%` for `DSL` and `7.40%` for no internet. Narrowing Fiber optic to subscribers lacking `OnlineSecurity` OR `TechSupport` isolates **`n=2,722`** accounts (`38.65%` of base) with **`45.70%` churn** (`1,244` churners = `66.56%` of all churn; `$108,733.60/mo` historical churned billing); those lacking *both* add-ons (`n=1,765`) churn at **`55.01%`** compared with **`14.17%`** among Fiber subscribers holding both (`n=374`). Meanwhile, `Electronic check` payers (`n=2,365`) churn at `45.29%` vs `15.24%` for automatic credit card billing.


---

# Layer 2 — Diagnostic Analytics Findings (`02_diagnostic/`)

> **Non-Causality Qualification:** All tests below evaluate observational associations in a cross-sectional snapshot (`N = 7,043`). "Strong association" does not prove causal intervention effects.

- **Categorical Bivariate Associations (`diagnostic_categorical_associations.csv`, `fig06`):**
  1. `Contract`: `chi2=1184.60`, `df=2`, `Cramer's V=0.4101`, Holm `p=9.97e-257` (`39.88` pp spread).
  2. `tenure_tier`: `chi2=868.86`, `V=0.3512`, Holm `p=1.49e-185`.
  3. `OnlineSecurity`: `V=0.3474`, Holm `p=3.99e-184` (`41.77%` without vs `14.61%` with add-on).
  4. `TechSupport`: `V=0.3429`, Holm `p=2.02e-179` (`41.64%` without vs `15.17%` with add-on).
  5. `InternetService` (`V=0.3225`) and `PaymentMethod` (`V=0.3034`).
  - By contrast, `gender` (`V=0.0086`, Holm `p=0.6325`) and `PhoneService` (`V=0.0119`, Holm `p=0.6325`) show **no statistically significant** association with Churn.
- **Continuous Group Comparisons (`diagnostic_continuous_comparisons.csv`, `fig02`, `fig03`, `fig05`):**
  - `tenure`: Churners mean `17.98` mo vs retained `37.57` mo (Welch `t=-34.82`, Mann-Whitney `p=2.42e-208`, `rank-biserial r=-0.4797`).
  - `MonthlyCharges`: Churners mean `$74.44` vs retained `$61.27` (`t=18.41`, `p=3.31e-54`, `r_rb=+0.2416`).
  - `TotalCharges`: Churners mean `$1,531.80` vs retained `$2,555.34` (`r_rb=-0.3035`).
- **Multivariable Confounding Reversal (`diagnostic_confounding_adjusted_odds.csv`):**
  - Marginally, `TotalCharges` exhibits negative association with churn (`unadjusted log-odds=-0.5349`, `OR=0.5857`) purely because cumulative charges increase mechanically with tenure (`TotalCharges ~ tenure * MonthlyCharges`). Controlling for `tenure` and `MonthlyCharges` reverses `TotalCharges` to `adjusted log-odds=+0.6703` (`OR=1.9549`).


---

# Split Strategy, Cross-Validation & Leak-Free Evaluation (`03_predictive/`)

- **Why Stratified Random Split (Instead of Chronological):** The IBM CSV (`7,043` records) contains no calendar timestamps (`tenure` is subscription duration in months `0..72`). Inventing a chronological split would impose arbitrary ordering. Stratified random sampling (`test_size=0.20`, `random_state=42`, `stratify=Churn`) preserves exact class prevalence (`26.54%`) and enforces 0 overlapping `customerID`s:
  - **Training / CV Development Split:** `n = 5,634` (`79.99%`; `1,495` Churn = Yes, `26.5353%`)
  - **Sealed Hold-Out Test Split:** `n = 1,409` (`20.01%`; `374` Churn = Yes, `26.5436%`)
- **Cross-Validation & Independent Threshold Protocol (`model_cv_comparison.csv`):**
  - All imputers (`SimpleImputer(strategy="median")`), numeric scalers (`StandardScaler`), categorical `OneHotEncoder(handle_unknown="ignore")`, hyperparameter grid searches (`5-fold Stratified CV`), probability calibration assessment, and each model's F1-optimal cutoff (`Logistic Regression`: `tau=0.325`; `Random Forest`: `tau=0.330`; `HistGradientBoosting`: `tau=0.340`) were selected **exclusively from 5-fold CV out-of-fold probabilities inside the 5,634 training records**, with zero hold-out test peeking.
  - Sigmoid calibration check: Uncalibrated `Random Forest` already achieved superior CV Brier score (`0.1345` vs calibrated `0.1351`, ECE `0.0196`), so `Random Forest` probabilities were retained unwarped (`calibration_applied=False`).


# Predictive Model Specifications & Held-Out Test Benchmarks (`03_predictive/`)

- **Algorithms Evaluated Fairly Under Identical Preprocessing (`n_test = 1,409`, `374` positive churners):**
  1. **No-Skill Floor (`DummyClassifier` most frequent):** Accuracy `0.7346`, Recall `0.0000`, ROC-AUC `0.5000`, PR-AUC `0.2654`. *(Reference only; not counted as a trained ML algorithm.)*
  2. **Simple Baseline Algorithm (`Logistic Regression`, L2 C=5.0):**
     - Default `0.50`: Test ROC-AUC **`0.8412`**, PR-AUC **`0.6286`**, Brier `0.1385`, Accuracy `0.8055`, F1 `0.6040` (`TP=209, FP=109, FN=165, TN=926`).
     - Own CV F1-Opt (`tau=0.325`): Precision `0.5335`, Recall `0.7246`, F1 `0.6145` (`TP=271, FP=237, FN=103, TN=798`).
  3. **Selected Champion Model (`Random Forest`, selected via highest 5-fold CV ROC-AUC=0.8480):**
     - Default `0.50`: Test ROC-AUC **`0.8440`**, PR-AUC **`0.6513`**, Brier **`0.1361`**, ECE **`0.0173`**, Accuracy `0.8020`, Precision `0.6727`, Recall `0.4947`, F1 `0.5701` (`TP=185, FN=189`).
     - Own CV F1-Opt (`tau=0.330`): Precision `0.5591`, Recall **`0.7460`** (`279/374` churners captured; `FN` drops from `189` to `95`), **F1 `0.6392`**, Accuracy `0.7764`.
  4. **Runner-Up Boosting Ensemble (`HistGradientBoosting`):**
     - Default `0.50`: Test ROC-AUC **`0.8461`**, PR-AUC **`0.6610`**, Brier `0.1354`, Accuracy `0.7977`, F1 `0.5753`.
     - Own CV F1-Opt (`tau=0.340`): Precision `0.5622`, Recall `0.7246`, **F1 `0.6332`** (`TP=271, FP=211, FN=103, TN=824`).
- **Critical Modeling Finding:** Linear `Logistic Regression` (`ROC-AUC=0.8412`) performs very close to tree ensembles (`0.8440`–`0.8461`) because churn propensity in the IBM sample is predominantly smooth and additive across contract length, tenure, and internet tier, with modest non-linear interaction gains (`HistGradientBoosting` PR-AUC `+0.0324` over baseline).


# Model Explainability & Limitations (`03_predictive/`)

## 1. Raw-Column Test Permutation Importance (`permutation_importance.csv`, `fig09`)
Evaluating permutation drops on raw input columns before one-hot encoding preserves unified feature credit:
  1. `Contract`: mean dROC-AUC = `0.0428` (±`0.0063`), mean dPR-AUC = `0.0632`
  2. `tenure`: mean dROC-AUC = `0.0256` (±`0.0034`), mean dPR-AUC = `0.0636`
  3. `InternetService`: mean dROC-AUC = `0.0162` (±`0.0038`), mean dPR-AUC = `0.0307`
  4. `TotalCharges`: mean dROC-AUC = `0.0137` (±`0.0022`), mean dPR-AUC = `0.0389`
  5. `OnlineSecurity`: mean dROC-AUC = `0.0040` (±`0.0020`), mean dPR-AUC = `0.0189`

## 2. Logistic Regression Directional Log-Odds (`logistic_odds_ratios.csv`, `fig09`)
- Strongest **risk-increasing** active indicators: `InternetService_Fiber optic` (`beta=+1.1535`, OR=`3.1694`), `Contract_Month-to-month` (`beta=+0.5525`, OR=`1.7375`), `StreamingMovies_Yes` (`+0.4474`), `StreamingTV_Yes` (`+0.4464`), `PaymentMethod_Electronic check` (`+0.1727`).
- Strongest **protective** signals: `tenure` (`beta=-1.2677` per 1 SD, OR=`0.2815`), `InternetService_DSL` (`beta=-1.0366`), `Contract_Two year` (`beta=-0.8248`, OR=`0.4383`), `Dependents_Yes` (`beta=-0.3213`).
- **Collinearity Explanation on `MonthlyCharges`:** In unconditional diagnostics `MonthlyCharges` increases churn (`r_rb=+0.2416`), yet its conditional Logistic Regression coefficient turns negative (`-1.6791`) because `MonthlyCharges` is almost collinear with holding `Fiber optic` + streaming + multiple-line indicators simultaneously. Permutation importance on `Random Forest` avoids coefficient sign-splitting and shows predictive credit consistently ranks `Contract`, `tenure`, `InternetService`, and `TotalCharges` at the top.

## 3. Practical Limitations of Predictive Scores
- **Missed Churn vs False Alarm Tradeoff:** Even at `tau=0.330`, `95` of `374` test churners (`25.40%`) are missed while `220` non-churners are flagged as false alarms (`Precision=55.91%`), justifying low-cost outreach rather than expensive universal discounts.
- **Snapshot Restriction:** Predicts retrospective class membership (*left last month*) on synthetic sample customers; does not incorporate network outage logs, competitor price drops, or customer support transcripts.


---

# Layer 4 — Prescriptive Recommendations Backed by Evidence (`04_prescriptive/`)
Each recommendation cites concrete statistics from Descriptive, Diagnostic, and Predictive outputs alongside explicit non-causal assumptions. `REC-4` (probability threshold `p >= 0.33`) and `REC-5` (budget-capped top-30% queue `p >= 0.3918`) are explicitly separated as distinct targeting policies.
## REC-1: Month-to-month subscribers in early tenure (1-12 months) [P1 (Highest Immediate Volume)]- **Measured Segment Count & Scope:** `n = 1,994` (28.31% of `Full Sample Compound Subgroup (N=7,043)`)- **Descriptive Evidence:** Month-to-month accounts span 3,875 customers (55.02% of base) at 42.71% churn (95% CI [41.16%, 44.27%]), accounting for 88.55% of all churn and $120,847.10/mo in historical monthly billing of churned records. The narrowed 1-12 mo subset (n=1,994, 28.31% of base) churns at 51.35% (1,024 churners = 54.79% of all churn).- **Diagnostic Evidence:** Contract has the strongest categorical association with Churn (chi2=1184.6, Cramer's V=0.4101, Holm p=9.97e-257), followed by tenure_tier (V=0.3512). Controlling for covariates, Two-year contracts show adjusted OR=0.2602 vs Month-to-month.- **Predictive Evidence:** Raw-column test permutation ranks Contract #1 (dROC-AUC=0.0428) and tenure #2 (dROC-AUC=0.0256). Test Tier 1 (p>=0.50, n=275) realizes 67.27% churn.- **Proposed Action:** Launch structured first-90-day onboarding check-ins and test step-down annual contract migration incentives (e.g., locked rate or waived upgrade fee) specifically among Model Tier 1 & Tier 2 early-tenure accounts.- **Assumptions & Caveats:** Assumes contract-migration incentives achieve an assumed 15-25% relative churn reduction without eroding net margin; IBM data is cross-sectional and does not test experimental discount elasticity.- **Source Paths:** `01_descriptive/tables/descriptive_compound_segments.csv; 01_descriptive/tables/descriptive_contract_by_tenure.csv; 02_diagnostic/tables/diagnostic_categorical_associations.csv; 03_predictive/tables/permutation_importance.csv`
## REC-2: Fiber optic subscribers lacking OnlineSecurity or TechSupport [P1 (Highest Billing Exposure)]- **Measured Segment Count & Scope:** `n = 2,722` (38.65% of `Full Sample Intersected Cohort (N=7,043)`)- **Descriptive Evidence:** Within broad Fiber optic accounts (n=3,096, 41.89% churn, $114,300.05/mo historical churned billing), the narrowed target cohort lacking OnlineSecurity or TechSupport comprises n=2,722 accounts (38.65% of base) with 45.70% churn (95% CI [43.84%, 47.58%], 1,244 churners = 66.56% of all churn, $108,733.60/mo historical churned billing). Those lacking both add-ons (n=1,765) churn at 55.01% vs 14.17% for Fiber users with both (n=374).- **Diagnostic Evidence:** OnlineSecurity (V=0.3474), TechSupport (V=0.3429), and InternetService (V=0.3225) rank 3rd-5th in association strength. Even after controlling for tenure and contract, Fiber optic retains adjusted OR=2.5646, whereas OnlineSecurity_Yes (OR=0.6913) and TechSupport_Yes (OR=0.7099) remain protective.- **Predictive Evidence:** InternetService ranks #3 (dROC-AUC=0.0162), OnlineSecurity ranks #5, and TechSupport ranks #6 in held-out Random Forest permutation importance.- **Proposed Action:** Audit Fiber optic service reliability/price perception and pilot bundled OnlineSecurity + priority TechSupport packages at no extra promotional cost for 3-6 months on Tier 1/2 Fiber accounts lacking both add-ons.- **Assumptions & Caveats:** Assumes lack of add-ons reflects unaddressed perceived value rather than pure unmeasured customer stickiness bias (existing add-on holders may reflect self-selected loyal subscribers rather than causal add-on protection).- **Source Paths:** `01_descriptive/tables/descriptive_compound_segments.csv; 01_descriptive/tables/descriptive_subgroups.csv; 02_diagnostic/tables/diagnostic_confounding_adjusted_odds.csv; 03_predictive/tables/permutation_importance.csv`
## REC-3: Electronic check manual payers [P2 (Billing & Payment Friction)]- **Measured Segment Count & Scope:** `n = 2,365` (33.58% of `Full Sample Subgroup (N=7,043)`)- **Descriptive Evidence:** Electronic check accounts (n=2,365, 33.58% of base) churn at 45.29% (95% CI [43.29%, 47.30%], $84,288.75/mo historical churned billing) vs 15.24% for Credit card automatic payers — accounting for 57.30% of all churn.- **Diagnostic Evidence:** PaymentMethod shows strong bivariate dependence (chi2=648.1, V=0.3034, Holm p=4.42e-139). After controlling for contract, tenure, and charges, Electronic check retains an elevated adjusted OR=1.3601.- **Predictive Evidence:** PaymentMethod ranks #7 (dROC-AUC=0.0022) in held-out test importance and helps separate Tier 2 Elevated Risk accounts (41.96% actual churn) from Tier 3 Low Risk.- **Proposed Action:** Promote streamlined enrollment into automatic credit card or bank transfer autopay with small one-time billing credits paired with clear paperless payment reminders.- **Assumptions & Caveats:** Assumes payment-method switching reduces accidental/bill-shock churn rather than merely selecting already loyal customers.- **Source Paths:** `01_descriptive/tables/descriptive_subgroups.csv; 01_descriptive/figures/fig01_churn_by_contract_payment.png; 02_diagnostic/tables/diagnostic_confounding_adjusted_odds.csv`
## REC-4: Hold-out accounts exceeding CV F1-optimal cutoff (p >= 0.33) [P2 (Threshold Classification Policy)]- **Measured Segment Count & Scope:** `n = 499` (35.42% of `Held-Out Test Probability Threshold (n=1,409)`)- **Descriptive Evidence:** Baseline full-sample churn is 26.54% (n=1,869 / 7,043) with $139,130.85/mo historical billing across churned records (30.50% of total monthly billing); untargeted outreach wastes 73.46% of contacts on non-churners.- **Diagnostic Evidence:** Multivariate churn risk spans Contract (V=0.4101), tenure_tier (V=0.3512), OnlineSecurity (V=0.3474), and PaymentMethod (V=0.3034); a calibrated probability threshold integrates all risk factors simultaneously without arbitrary single-variable exclusions.- **Predictive Evidence:** Random Forest (Test ROC-AUC=0.8440, PR-AUC=0.6513, Brier=0.1361) at CV F1-optimal cutoff tau=0.33 flags n=499/1,409 (35.42%) test accounts (Tier 1 p>=0.50: n=275, 67.27% realized churn; Tier 2 0.33<=p<0.50: n=224, 41.96% churn), capturing 74.60% of test churners (279/374) at 55.91% precision (F1=0.6392) vs Tier 3 Low Risk (10.44% churn).- **Proposed Action:** Use probability-threshold triage when outreach budget scales to ~35% of base: route Tier 1 (p>=0.50) to high-touch agent outreach, Tier 2 (0.33<=p<0.50) to automated digital offers, and exclude Tier 3 (p<0.33).- **Assumptions & Caveats:** Distinct from a fixed Top-30% budget queue (see REC-5). Model trained on fictional cross-sectional snapshot; live deployment requires A/B uplift validation and periodic calibration monitoring.- **Source Paths:** `03_predictive/tables/model_test_comparison.csv; 03_predictive/tables/test_predictions.csv; 04_prescriptive/tables/prescriptive_risk_tiers.csv`
## REC-5: Top 30% capacity-ranked risk queue (empirical test cutoff p >= 0.3918) [P2 (Budget-Capped Queue Policy)]- **Measured Segment Count & Scope:** `n = 423` (30.02% of `Held-Out Test Capacity Queue (n=1,409)`)- **Descriptive Evidence:** In the full snapshot, churned records carry $139,130.85/mo in historical monthly charges ($64.76 avg across all vs $74.44 among churned), making volume-capped prioritization critical when retention team capacity is strictly budgeted below the 35.42% F1-threshold share.- **Diagnostic Evidence:** High-risk concentration within short-tenure Fiber and Month-to-month segments creates steep diminishing marginal risk in the bottom 70% of accounts, supporting ranked queue ordering by calibrated churn probability.- **Predictive Evidence:** Ranking the sealed 1,409 test accounts by Random Forest probability selects n=423 (30.02% capacity, min predicted p=0.3918), capturing 246/374 (65.78%) test churners at 58.16% precision (2.19x lift over random) and covering $18,907.85/mo (69.48% of the $27,214.90/mo historical churned billing in test).- **Proposed Action:** When outreach team capacity is fixed at <=30% of accounts (~2,113 seats if scaled proportionally across a 7,043-customer base as an illustrative benchmark), rank customers descending by predicted probability and contact the top-30% queue rather than using the looser 0.33 cutoff.- **Assumptions & Caveats:** Observed lift (2.19x) is measured strictly on n=423/1,409 held-out test records; illustrative 6-mo net financial scenarios ($15-$25 cost, 10%-30% save rate) depend on untested causal uplift assumptions.- **Source Paths:** `04_prescriptive/tables/prescriptive_capacity_lift.csv; 04_prescriptive/tables/prescriptive_scenario_sensitivity.csv; 04_prescriptive/figures/fig10_prescriptive_targeting_lift.png`


# Prescriptive Targeting Tiers, Capacity Lift & Assumption Sensitivity

## 1. Held-Out Risk Tier Realization (`prescriptive_risk_tiers.csv`, `n_test = 1,409`)
- **Tier 1: High Risk (p >= 0.50):** `275` customers (`19.52%`), mean predicted churn `64.32%` vs **realized churn `67.27%`** (`185` churners = **`49.47%`** of all test churn; `$14,369.20/mo` historical monthly billing among churned test records).
- **Tier 2: Elevated Risk (0.33 <= p < 0.50):** `224` customers (`15.90%`), mean predicted `41.54%` vs **realized churn `41.96%`** (`94` churners = `25.13%` of all test churn; `$6,622.25/mo` historical churned billing).
- **Tier 3: Low Risk (p < 0.33):** `910` customers (`64.58%`), mean predicted `11.68%` vs **realized churn `10.44%`**.

## 2. Threshold Policy (`REC-4`) vs. Capacity Queue (`REC-5`) & Scenario Sensitivity
- **Why Two Policies Differ:** Evaluating `Random Forest` on the sealed `1,409`-account test set at its CV F1-optimal probability threshold `tau = 0.330` (`REC-4`) flags **`499` accounts (`35.42%`)**, reaching `279 / 374` (`74.60%`) of churners. By contrast, capping outreach strictly at the Top **`30%`** capacity tier (`REC-5`, empirical test rank cutoff `p >= 0.3918`) selects **`423` test accounts (`30.02%`)**, reaching **`246 / 374` (`65.78%`)** of churners (`2.19x` lift over random outreach) covering `$18,907.85/mo` in historical churned monthly charges.
- **Explicit Separation of Facts vs Assumptions:** All financial scenario numbers (`$15`/`$25` outreach cost, `10%–30%` assumed save rate, `6`-month horizon) in `prescriptive_scenario_sensitivity.csv` and the Streamlit Scenario Simulator are **user-adjustable hypothetical assumptions** — NOT measured treatment effects or guaranteed revenue saved. If actual outreach costs `$25/cust` and only saves `10%` at `40%` outreach capacity, illustrative 6-month net value turns negative (`-$919.05`). A controlled A/B retention pilot is required before rollout.


---

# Sources, Methodology Boundaries, and Honest Limitations

1. **Fictional Snapshot Caveat:** IBM's sample CSV (`N = 7,043`) describes a fictional carrier snapshot rather than verified real-world commercial transactions or multi-month longitudinal follow-up.
2. **Historical Billing Exposure vs Prospective Revenue:** Metrics labeled `monthly_revenue_at_risk_usd` (e.g., `$139,130.85/mo`) measure current monthly charges on records labeled `Churn = Yes`. They quantify retrospective billing exposure in the snapshot, NOT verified multi-month lost revenue or guaranteed retention savings.
3. **Non-Causality:** Bivariate diagnostics (`Cramer's V`, `Mann-Whitney U`) and model explanations (`Permutation Importance`, `Logistic Odds`) reveal statistical associations and predictive signal; they do **not** establish that modifying an attribute (e.g., gifting OnlineSecurity or migrating contracts) will causally reduce churn by the observational difference.
4. **Missingness & Duplicate Handling Transparency:** Exact `TotalCharges` blanks (`n = 11`, `100%` at `tenure = 0`) and `22` non-ID matching feature profiles are documented rather than silently deleted.
5. **No Treatment Uplift Data:** Financial figures in `prescriptive_scenario_sensitivity.csv` quantify sensitivity across explicit scenario assumptions (`cost`, `save rate`, `horizon`) rather than observed campaign ROI.

