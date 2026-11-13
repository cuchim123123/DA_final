# Prescriptive Targeting Tiers, Capacity Lift & Assumption Sensitivity

## 1. Held-Out Risk Tier Realization (`prescriptive_risk_tiers.csv`, `n_test = 1,409`)
- **Tier 1: High Risk (p >= 0.50):** `275` customers (`19.52%`), mean predicted churn `64.32%` vs **realized churn `67.27%`** (`185` churners = **`49.47%`** of all test churn; `$14,369.20/mo` historical monthly billing among churned test records).
- **Tier 2: Elevated Risk (0.33 <= p < 0.50):** `224` customers (`15.90%`), mean predicted `41.54%` vs **realized churn `41.96%`** (`94` churners = `25.13%` of all test churn; `$6,622.25/mo` historical churned billing).
- **Tier 3: Low Risk (p < 0.33):** `910` customers (`64.58%`), mean predicted `11.68%` vs **realized churn `10.44%`**.

## 2. Threshold Policy (`REC-4`) vs. Capacity Queue (`REC-5`) & Scenario Sensitivity
- **Why Two Policies Differ:** Evaluating `Random Forest` on the sealed `1,409`-account test set at its CV F1-optimal probability threshold `tau = 0.330` (`REC-4`) flags **`499` accounts (`35.42%`)**, reaching `279 / 374` (`74.60%`) of churners. By contrast, capping outreach strictly at the Top **`30%`** capacity tier (`REC-5`, empirical test rank cutoff `p >= 0.3918`) selects **`423` test accounts (`30.02%`)**, reaching **`246 / 374` (`65.78%`)** of churners (`2.19x` lift over random outreach) covering `$18,907.85/mo` in historical churned monthly charges.
- **Explicit Separation of Facts vs Assumptions:** All financial scenario numbers (`$15`/`$25` outreach cost, `10%–30%` assumed save rate, `6`-month horizon) in `prescriptive_scenario_sensitivity.csv` and the Streamlit Scenario Simulator are **user-adjustable hypothetical assumptions** — NOT measured treatment effects or guaranteed revenue saved. If actual outreach costs `$25/cust` and only saves `10%` at `40%` outreach capacity, illustrative 6-month net value turns negative (`-$919.05`). A controlled A/B retention pilot is required before rollout.
