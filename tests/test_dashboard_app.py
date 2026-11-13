"""Automated verification tests for Bike Sharing Streamlit dashboard and helper functions."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from app.helpers import (
    compute_filtered_eda_kpis,
    filter_bike_cohort,
    get_figure_path,
    load_dashboard_artifacts,
    predict_bike_demand,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_load_dashboard_artifacts() -> None:
    art = load_dashboard_artifacts()
    assert len(art.df) == 731
    assert "cnt" in art.df.columns
    assert "dteday_parsed" in art.df.columns
    assert len(art.tables) > 10
    assert "h1_ttest_workingday" in art.tables
    assert "regression_model_comparison" in art.tables
    assert art.ols_pipe is not None
    assert art.ols_statsmodels is not None
    assert len(art.feature_names) == 11


def test_filter_bike_cohort_and_kpis() -> None:
    art = load_dashboard_artifacts()

    # Filter to Spring (season == 1)
    sub = filter_bike_cohort(art.df, seasons=[1])
    assert len(sub) == 181

    # Filter to Working Days only
    sub_work = filter_bike_cohort(art.df, day_types=["Working Days"])
    assert len(sub_work) == 500

    # Test dynamic KPI calculations
    kpis = compute_filtered_eda_kpis(sub)
    assert kpis["n_days"] == 181
    assert kpis["total_rentals"] > 0
    assert np.isclose(kpis["casual_share_pct"] + kpis["registered_share_pct"], 100.0, atol=0.2)
    assert kpis["mean_daily_rentals"] > 2000.0


def test_predict_bike_demand_simulation() -> None:
    art = load_dashboard_artifacts()

    # Moderate pleasant summer workday scenario
    res = predict_bike_demand(
        art=art,
        yr=1,
        season=2,
        holiday=0,
        workingday=1,
        weathersit=1,
        temp_c=24.0,
        hum_pct=55.0,
        windspeed_kmh=14.0,
    )

    assert res["predicted_cnt"] > 3000
    assert res["predicted_cnt"] < 9000
    assert res["predicted_registered"] > res["predicted_casual"]  # Workday pattern
    ci_mean = res["mean_ci_95"]
    assert ci_mean[0] <= res["predicted_cnt"] <= ci_mean[1]
    pi_obs = res["prediction_interval_95"]
    assert pi_obs[0] < res["predicted_cnt"] < pi_obs[1]
    assert pi_obs[0] < ci_mean[0]
    assert pi_obs[1] > ci_mean[1]


def test_get_figure_path() -> None:
    p = get_figure_path("fig01_daily_rentals_timeseries.png")
    assert p is not None
    assert p.exists()

    p_bad = get_figure_path("non_existent_figure.png")
    assert p_bad is None


def test_streamlit_app_all_five_views_render_cleanly() -> None:
    at = AppTest.from_file(PROJECT_ROOT / "app" / "streamlit_app.py", default_timeout=25)
    at.run()
    assert not at.exception

    # Test switching to all 5 navigation views
    views = list(at.sidebar.radio[0].options)
    assert len(views) == 5

    for v in views:
        at.sidebar.radio[0].set_value(v).run()
        assert not at.exception
