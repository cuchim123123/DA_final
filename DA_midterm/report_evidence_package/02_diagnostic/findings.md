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
