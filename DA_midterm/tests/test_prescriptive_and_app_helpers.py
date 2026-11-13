"""Automated verification tests for prescriptive analytics, app helpers, and Streamlit UI."""

from __future__ import annotations

from app.helpers import (
    compute_filtered_kpis,
    compute_threshold_metrics,
    filter_customer_cohort,
    load_dashboard_artifacts,
    score_hypothetical_customer,
    simulate_retention_scenario,
)
from streamlit.testing.v1 import AppTest

from telco_churn.config import PROJECT_ROOT


def test_dashboard_helpers_filtering_scoring_and_scenarios() -> None:
    art = load_dashboard_artifacts()
    recs = art.recommendations_df.set_index("rec_id")
    assert len(recs) == 5
    assert int(recs.loc["REC-2", "segment_n"]) == 2722
    assert int(recs.loc["REC-4", "segment_n"]) == 499
    assert int(recs.loc["REC-5", "segment_n"]) == 423
    for col in ["descriptive_evidence", "diagnostic_evidence", "predictive_evidence", "assumptions_and_caveats"]:
        assert art.recommendations_df[col].notna().all()

    # Interactive cohort filter changes counts & rates accurately
    sub = filter_customer_cohort(art.df_eda, contracts=["Month-to-month"], tenure_range=(1, 12))
    kpis = compute_filtered_kpis(sub)
    assert kpis["n_customers"] == 1994
    assert abs(kpis["churn_rate_pct"] - 51.35) < 0.1

    # Held-out threshold metrics match confusion counts
    tm = compute_threshold_metrics(art.test_pred_df, "prob_champion", 0.33)
    assert tm["tp"] + tm["fn"] + tm["fp"] + tm["tn"] == 1409
    assert tm["tp"] + tm["fn"] == 374

    # Hypothetical scoring normalizes service dependencies and calls champion pipeline
    scored = score_hypothetical_customer(
        art.champion_pipeline,
        {
            "gender": "Female",
            "SeniorCitizen": 0,
            "Partner": "No",
            "Dependents": "No",
            "tenure": 2,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "No",
            "OnlineBackup": "No",
            "DeviceProtection": "No",
            "TechSupport": "No",
            "StreamingTV": "Yes",
            "StreamingMovies": "Yes",
            "Contract": "Month-to-month",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",
            "MonthlyCharges": 95.0,
            "TotalCharges": 190.0,
        },
        val_threshold=0.33,
    )
    assert scored["predicted_churn_probability"] > 0.50
    assert scored["risk_tier"].startswith("Tier 1")

    # Prescriptive scenario math verification
    sim = simulate_retention_scenario(
        art.test_pred_df,
        outreach_capacity_pct=30.0,
        outreach_cost_per_customer_usd=15.0,
        assumed_save_rate=0.20,
        assumed_horizon_months=6,
    )
    assert sim["customers_targeted"] == 423
    assert sim["observed_test_churners_reached"] == 246
    assert abs(sim["assumed_campaign_cost_usd"] - 6345.0) < 1e-6


def test_streamlit_app_all_four_views_render_cleanly() -> None:
    at = AppTest.from_file(PROJECT_ROOT / "app" / "streamlit_app.py", default_timeout=20)
    at.run()
    assert not at.exception

    # Switch through all 4 radio views and check interactive filter reactivity
    views = list(at.sidebar.radio[0].options)
    assert len(views) == 4
    for v in views:
        at.sidebar.radio[0].set_value(v).run()
        assert not at.exception
        if v.startswith("2."):
            # Apply a filter change and confirm filtered metrics execute cleanly
            at.multiselect[0].set_value(["Month-to-month"]).run()
            assert not at.exception
        elif v.startswith("4."):
            at.slider[0].set_value(20).run()
            assert not at.exception
