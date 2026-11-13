# Sources, Methodology Boundaries, and Honest Limitations

1. **Fictional Snapshot Caveat:** IBM's sample CSV (`N = 7,043`) describes a fictional carrier snapshot rather than verified real-world commercial transactions or multi-month longitudinal follow-up.
2. **Historical Billing Exposure vs Prospective Revenue:** Metrics labeled `monthly_revenue_at_risk_usd` (e.g., `$139,130.85/mo`) measure current monthly charges on records labeled `Churn = Yes`. They quantify retrospective billing exposure in the snapshot, NOT verified multi-month lost revenue or guaranteed retention savings.
3. **Non-Causality:** Bivariate diagnostics (`Cramer's V`, `Mann-Whitney U`) and model explanations (`Permutation Importance`, `Logistic Odds`) reveal statistical associations and predictive signal; they do **not** establish that modifying an attribute (e.g., gifting OnlineSecurity or migrating contracts) will causally reduce churn by the observational difference.
4. **Missingness & Duplicate Handling Transparency:** Exact `TotalCharges` blanks (`n = 11`, `100%` at `tenure = 0`) and `22` non-ID matching feature profiles are documented rather than silently deleted.
5. **No Treatment Uplift Data:** Financial figures in `prescriptive_scenario_sensitivity.csv` quantify sensitivity across explicit scenario assumptions (`cost`, `save rate`, `horizon`) rather than observed campaign ROI.
