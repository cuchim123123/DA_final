"""Automated statistical consistency tests enforcing single source of truth across Bike Sharing analytics."""

from __future__ import annotations

from pathlib import Path
import pytest
import numpy as np
import pandas as pd

from app.helpers import (
    load_dashboard_artifacts,
    compute_filtered_eda_kpis,
    filter_bike_cohort,
    predict_bike_demand,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_core_dataset_kpis_and_peak_date():
    """Verify core dataset volume invariants and absolute peak rental date."""
    art = load_dashboard_artifacts()
    df = art.df

    assert len(df) == 731
    total_rentals = int(df["cnt"].sum())
    assert total_rentals == 3_292_679

    mean_rentals = float(df["cnt"].mean())
    std_rentals = float(df["cnt"].std(ddof=1))
    assert np.isclose(mean_rentals, 4504.3488, atol=0.01)
    assert np.isclose(std_rentals, 1937.2115, atol=0.01)

    # All-time peak day must be 2012-09-15 with 8,714 rentals
    peak_row = df.loc[df["cnt"].idxmax()]
    assert peak_row["dteday"] == "2012-09-15"
    assert peak_row["cnt"] == 8714

    # KPI calculation helper check
    kpis = compute_filtered_eda_kpis(df)
    assert kpis["n_days"] == 731
    assert kpis["total_rentals"] == 3_292_679
    assert kpis["peak_day_date"] == "2012-09-15"
    assert kpis["peak_day_cnt"] == 8714


def test_hypothesis_test_consistency():
    """Verify hypothesis test statistics and decisions match authoritative evidence."""
    art = load_dashboard_artifacts()

    # 1. H1 Working day Welch t-test
    h1_table = art.tables.get("h1_ttest_workingday")
    assert h1_table is not None
    h1_cnt = h1_table.loc[h1_table["segment"] == "cnt"].iloc[0]
    assert np.isclose(float(h1_cnt["t_welch"]), 1.6014, atol=0.005)
    assert np.isclose(float(h1_cnt["p_value_welch"]), 0.1101, atol=0.005)
    assert np.isclose(float(h1_cnt["df_welch"]), 413.94, atol=0.1)
    # Fail to reject H0 at alpha = 0.05
    assert float(h1_cnt["p_value_welch"]) > 0.05

    # 2. H2 Seasonal ANOVA & Kruskal-Wallis
    h2_om = art.results.get("hypothesis_tests", {}).get("h2_anova", {}).get("omnibus_results", {})
    assert np.isclose(float(h2_om["f_statistic_ordinary"]), 128.7696, atol=0.05)
    assert np.isclose(float(h2_om["kruskal_wallis_h"]), 250.9335, atol=0.05)
    assert float(h2_om["p_value_ordinary_anova"]) < 1e-50
    assert float(h2_om["p_value_kruskal_wallis"]) < 1e-50

    # 3. H3 Weather Chi-Square
    h3_om = art.results.get("hypothesis_tests", {}).get("h3_chisq", {}).get("omnibus_results", {})
    assert np.isclose(float(h3_om["pearson_chi2"]), 44.0879, atol=0.05)
    assert np.isclose(float(h3_om["cramers_v"]), 0.2456, atol=0.005)
    assert float(h3_om["p_value_chi2"]) < 1e-8

    h_summary = art.tables.get("hypothesis_tests_summary")
    assert h_summary is not None
    h3_row = h_summary.loc[h_summary["hypothesis_id"] == "H3"].iloc[0]
    assert "44.0879" in str(h3_row["test_statistic"])
    assert float(h3_row["p_value_unadjusted"]) < 1e-8
    assert "0.2456" in str(h3_row["effect_size"])


def test_correlation_coefficients_and_vif():
    """Verify linear and monotonic rank correlation coefficients and VIF diagnostics."""
    art = load_dashboard_artifacts()

    corr_table = art.tables.get("correlation_pairwise_tests")
    assert corr_table is not None
    cnt_temp = corr_table.loc[corr_table["pair_label"] == "cnt vs temp"].iloc[0]
    assert np.isclose(float(cnt_temp["pearson_r"]), 0.6275, atol=0.005)
    assert np.isclose(float(cnt_temp["spearman_rho"]), 0.6220, atol=0.005)

    temp_atemp = corr_table.loc[corr_table["pair_label"] == "temp vs atemp"].iloc[0]
    assert np.isclose(float(temp_atemp["pearson_r"]), 0.9917, atol=0.005)

    vif_table = art.tables.get("regression_vif_diagnostics")
    assert vif_table is not None
    temp_vif = vif_table.loc[vif_table["feature"] == "num__temp"].iloc[0]
    assert float(temp_vif["vif_when_atemp_included"]) > 64.0
    assert float(temp_vif["vif"]) < 4.0


def test_held_out_model_evaluation_metrics():
    """Verify held-out test evaluation metrics preserve chronological 80/20 train/test split."""
    art = load_dashboard_artifacts()
    reg_table = art.tables.get("regression_model_comparison")
    assert reg_table is not None

    ols_row = reg_table.loc[reg_table["model_name"].str.contains("Primary", case=False)].iloc[0]

    # In-sample Train metrics
    assert np.isclose(float(ols_row["train_r2"]), 0.8387, atol=0.005)
    assert np.isclose(float(ols_row["train_rmse"]), 717.85, atol=0.5)

    # Out-of-sample Held-Out Test metrics (Chronological 20%)
    assert np.isclose(float(ols_row["test_r2"]), 0.6139, atol=0.005)
    assert np.isclose(float(ols_row["test_rmse"]), 1164.87, atol=0.5)
    assert np.isclose(float(ols_row["test_mae"]), 891.69, atol=0.5)
    assert np.isclose(float(ols_row["test_bias_pred_minus_true"]), -204.70, atol=0.5)


def test_simulator_fixed_scenarios():
    """Verify interactive simulator outputs for fixed baseline and adverse profiles."""
    art = load_dashboard_artifacts()

    # 1. Baseline Workday Scenario:
    # 2012 (yr=1), Fall (season=3), Workday (workingday=1, holiday=0), Clear (weathersit=1), temp=24C, hum=55%, wind=14km/h
    res_base = predict_bike_demand(
        art=art,
        yr=1,
        season=3,
        holiday=0,
        workingday=1,
        weathersit=1,
        temp_c=24.0,
        hum_pct=55.0,
        windspeed_kmh=14.0,
    )
    assert res_base["predicted_cnt"] == 6019.0
    assert res_base["predicted_registered"] == 5149.0
    assert res_base["predicted_casual"] == 870.0
    assert res_base["mean_ci_95"] == (5832.0, 6206.0)
    assert res_base["prediction_interval_95"] == (4582.0, 7456.0)
    assert res_base["fleet_advisory"] == "Standard Fleet Operations"

    # 2. Adverse Weekend Scenario:
    # 2012 (yr=1), Winter (season=4), Weekend/Holiday (workingday=0, holiday=0), Light Rain/Snow (weathersit=3), temp=4C, hum=85%, wind=28km/h
    res_adverse = predict_bike_demand(
        art=art,
        yr=1,
        season=4,
        holiday=0,
        workingday=0,
        weathersit=3,
        temp_c=4.0,
        hum_pct=85.0,
        windspeed_kmh=28.0,
    )
    assert res_adverse["predicted_cnt"] == 1781.0
    assert res_adverse["predicted_registered"] == 1530.0
    assert res_adverse["predicted_casual"] == 250.0
    assert res_adverse["mean_ci_95"] == (1322.0, 2239.0)
    assert res_adverse["prediction_interval_95"] == (284.0, 3277.0)
    assert "Low Demand Notice" in res_adverse["fleet_advisory"]


def test_absence_of_stale_hardcoded_values():
    """Verify that stale hardcoded numbers identified in the audit do not exist in streamlit_app.py."""
    app_path = PROJECT_ROOT / "app" / "streamlit_app.py"
    content = app_path.read_text(encoding="utf-8")

    stale_values = [
        "0.5734",
        "0.5667",
        "265.17",
        "68.74",
        "0.8174",
        "744.2",
    ]

    for val in stale_values:
        assert val not in content, f"Found stale hardcoded value '{val}' in {app_path.name}"
