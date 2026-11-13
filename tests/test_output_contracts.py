"""Automated Output Contracts & Reproducibility Verification Suite (Phases 1–6)."""

import json
import numpy as np
import pandas as pd

from src.correlations import CORRELATION_CONTINUOUS_VARS
from src.load_validate import OUTPUTS_DIR, PROJECT_ROOT, TABLES_DIR
from src.run_all import run_all_pipeline
from src.visualizations import FIGURES_DIR


def test_correlation_tables() -> None:
    """Verify both Pearson and Spearman correlation matrices exist with explicit labels."""
    p_df = pd.read_csv(TABLES_DIR / "pearson_correlation_matrix.csv", index_col=0)
    s_df = pd.read_csv(TABLES_DIR / "spearman_correlation_matrix.csv", index_col=0)
    pair_df = pd.read_csv(TABLES_DIR / "correlation_pairwise_tests.csv")

    assert list(p_df.columns) == CORRELATION_CONTINUOUS_VARS
    assert list(s_df.columns) == CORRELATION_CONTINUOUS_VARS
    assert np.allclose(np.diag(p_df.to_numpy()), 1.0)
    assert np.allclose(np.diag(s_df.to_numpy()), 1.0)
    assert len(pair_df) == 10
    for cat_col in ["season", "weathersit", "mnth", "weekday"]:
        assert cat_col not in p_df.columns and cat_col not in s_df.columns


def test_required_plots() -> None:
    """Verify all 18 registered figures exist on disk and are non-empty PNG files."""
    with open(OUTPUTS_DIR / "results.json", "r", encoding="utf-8") as f:
        res = json.load(f)
    assert len(res["figures"]) == 18
    for fig_meta in res["figures"]:
        fpath = FIGURES_DIR / fig_meta["filename"]
        assert fpath.exists() and fpath.stat().st_size > 15_000


def test_all_tables_and_notebook_exist() -> None:
    """Verify all required CSV tables and executed walkthrough notebook exist."""
    expected_tables = [
        "data_dictionary_summary.csv",
        "eda_continuous_summary.csv",
        "eda_group_by_year.csv",
        "eda_group_by_season.csv",
        "eda_group_by_weathersit.csv",
        "eda_group_by_workingday.csv",
        "eda_group_by_holiday.csv",
        "eda_weather_by_workingday.csv",
        "eda_outlier_audit.csv",
        "eda_outlier_handling_sensitivity.csv",
        "probability_distribution_summary.csv",
        "cnt_overdispersion_and_fit.csv",
        "temp_distribution_diagnostics.csv",
        "hypothesis_tests_summary.csv",
        "h1_ttest_workingday.csv",
        "h2_anova_season_posthoc.csv",
        "h3_chisq_contingency_table.csv",
        "pearson_correlation_matrix.csv",
        "spearman_correlation_matrix.csv",
        "correlation_pairwise_tests.csv",
        "regression_model_comparison.csv",
        "regression_ols_coefficients.csv",
        "regression_vif_diagnostics.csv",
        "regression_residual_diagnostics.csv",
    ]
    for tbl in expected_tables:
        tpath = TABLES_DIR / tbl
        assert tpath.exists() and len(pd.read_csv(tpath)) >= 1

    nb_path = PROJECT_ROOT / "notebooks" / "analysis.ipynb"
    assert nb_path.exists() and nb_path.stat().st_size > 5_000


def test_dynamic_values_consistency() -> None:
    """Verify no stale or hardcoded numbers exist in model comparison and summary tables."""
    with open(OUTPUTS_DIR / "results.json", "r", encoding="utf-8") as f:
        res = json.load(f)

    train_pred_df = pd.read_csv(OUTPUTS_DIR / "model" / "train_predictions.csv")
    actual_train_mean = float(train_pred_df["y_true"].mean())
    base_role = res["regression"]["model_comparison_table"][0]["role"]
    assert f"{actual_train_mean:,.2f}" in base_role


def test_reproducibility() -> None:
    """Verify an independent rerun produces identical numerical results."""
    with open(OUTPUTS_DIR / "results.json", "r", encoding="utf-8") as f:
        first_run = json.load(f)
    second_run = run_all_pipeline(build_notebook=False)

    assert first_run["eda"]["key_findings"]["overall_mean_cnt"] == second_run["eda"]["key_findings"]["overall_mean_cnt"]
    assert (
        first_run["probability"]["cnt"]["poisson_diagnostics"]["variance_to_mean_ratio_index_of_dispersion"]
        == second_run["probability"]["cnt"]["poisson_diagnostics"]["variance_to_mean_ratio_index_of_dispersion"]
    )
    assert (
        first_run["hypothesis_tests"]["h2_anova"]["omnibus_results"]["f_statistic_ordinary"]
        == second_run["hypothesis_tests"]["h2_anova"]["omnibus_results"]["f_statistic_ordinary"]
    )
    assert first_run["regression"]["metrics"]["ols_test"]["rmse"] == second_run["regression"]["metrics"]["ols_test"]["rmse"]
    assert first_run["regression"]["metrics"]["ols_test"]["r2"] == second_run["regression"]["metrics"]["ols_test"]["r2"]
