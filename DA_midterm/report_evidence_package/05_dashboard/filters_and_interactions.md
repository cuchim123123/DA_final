# Dashboard Interactive Controls & State Guarantees

1. **Zero UI Retraining:** All tables and `champion_pipeline.joblib` are loaded once via `@st.cache_resource`; changing filters, thresholds, or scenario sliders never retrains models or leaks test labels.
2. **Cohort Filters (`Explore & Diagnose`):** `Contract`, `InternetService`, `PaymentMethod`, `SeniorCitizen`, and `tenure` slider `[0..72]` dynamically recompute sample size `n`, churn rate %, 95% Wilson CI bounds, historical churned monthly billing, and subgroup bar charts.
3. **Cutoff Explorer (`Predictive Models`):** Adjusting `tau` in `[0.15, 0.75]` recalculates exact confusion counts (`TP/FP/FN/TN`), Precision, Recall, F1, and Accuracy directly on precomputed held-out `test_predictions.csv`.
4. **Hierarchy-Safe Single-Profile Scorer:** Setting `PhoneService = "No"` locks `MultipleLines = "No phone service"` and setting `InternetService = "No"` locks all six add-ons to `"No internet service"` before calling `validate_customer_record()` and `champion_pipeline.predict_proba()`.
5. **Scenario Simulator (`Prescriptive Prioritization`):** Strictly separates observed held-out churners reached and historical churned billing from user-adjustable inputs (`Outreach Capacity %`, `Cost/Contact $`, `Assumed Save Rate %`, `Horizon Months`).
