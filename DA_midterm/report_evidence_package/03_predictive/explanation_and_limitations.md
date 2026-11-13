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
