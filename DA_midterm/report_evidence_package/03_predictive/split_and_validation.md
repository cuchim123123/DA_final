# Split Strategy, Cross-Validation & Leak-Free Evaluation (`03_predictive/`)

- **Why Stratified Random Split (Instead of Chronological):** The IBM CSV (`7,043` records) contains no calendar timestamps (`tenure` is subscription duration in months `0..72`). Inventing a chronological split would impose arbitrary ordering. Stratified random sampling (`test_size=0.20`, `random_state=42`, `stratify=Churn`) preserves exact class prevalence (`26.54%`) and enforces 0 overlapping `customerID`s:
  - **Training / CV Development Split:** `n = 5,634` (`79.99%`; `1,495` Churn = Yes, `26.5353%`)
  - **Sealed Hold-Out Test Split:** `n = 1,409` (`20.01%`; `374` Churn = Yes, `26.5436%`)
- **Cross-Validation & Independent Threshold Protocol (`model_cv_comparison.csv`):**
  - All imputers (`SimpleImputer(strategy="median")`), numeric scalers (`StandardScaler`), categorical `OneHotEncoder(handle_unknown="ignore")`, hyperparameter grid searches (`5-fold Stratified CV`), probability calibration assessment, and each model's F1-optimal cutoff (`Logistic Regression`: `tau=0.325`; `Random Forest`: `tau=0.330`; `HistGradientBoosting`: `tau=0.340`) were selected **exclusively from 5-fold CV out-of-fold probabilities inside the 5,634 training records**, with zero hold-out test peeking.
  - Sigmoid calibration check: Uncalibrated `Random Forest` already achieved superior CV Brier score (`0.1345` vs calibrated `0.1351`, ECE `0.0196`), so `Random Forest` probabilities were retained unwarped (`calibration_applied=False`).
