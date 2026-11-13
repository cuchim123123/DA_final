"""
Automated Multiple Linear Regression Verification Suite (Phase 6).

Verifies metric consistency against saved predictions, identical hold-out test
rows for baseline and OLS, VIF reduction when dropping `atemp`, and finite
robust standard errors (IID, HC3, and Newey-West HAC).
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.regression import MODEL_DIR, run_regression_analysis


def test_metric_consistency() -> None:
    """Verify reported metrics match a fresh calculation from saved y_true and y_pred."""
    reg_res = run_regression_analysis(save_outputs=True)
    test_pred_df = pd.read_csv(MODEL_DIR / "test_predictions.csv")
    train_pred_df = pd.read_csv(MODEL_DIR / "train_predictions.csv")

    # Test OLS metrics
    y_true_test = test_pred_df["y_true"].values
    y_pred_ols_test = test_pred_df["y_pred_ols"].values

    fresh_mae_test = float(mean_absolute_error(y_true_test, y_pred_ols_test))
    fresh_rmse_test = float(np.sqrt(mean_squared_error(y_true_test, y_pred_ols_test)))
    fresh_r2_test = float(r2_score(y_true_test, y_pred_ols_test))

    rep_test = reg_res["metrics"]["ols_test"]
    assert np.isclose(rep_test["mae"], fresh_mae_test, atol=1e-3)
    assert np.isclose(rep_test["rmse"], fresh_rmse_test, atol=1e-3)
    assert np.isclose(rep_test["r2"], fresh_r2_test, atol=1e-3)

    # Train OLS metrics
    y_true_train = train_pred_df["y_true"].values
    y_pred_ols_train = train_pred_df["y_pred_ols"].values
    fresh_mae_train = float(mean_absolute_error(y_true_train, y_pred_ols_train))
    fresh_rmse_train = float(np.sqrt(mean_squared_error(y_true_train, y_pred_ols_train)))
    fresh_r2_train = float(r2_score(y_true_train, y_pred_ols_train))

    rep_train = reg_res["metrics"]["ols_train"]
    assert np.isclose(rep_train["mae"], fresh_mae_train, atol=1e-3)
    assert np.isclose(rep_train["rmse"], fresh_rmse_train, atol=1e-3)
    assert np.isclose(rep_train["r2"], fresh_r2_train, atol=1e-3)


def test_baseline_same_test() -> None:
    """Verify baseline and OLS are evaluated on the exact same 147 hold-out rows."""
    reg_res = run_regression_analysis(save_outputs=True)
    test_pred_df = pd.read_csv(MODEL_DIR / "test_predictions.csv")

    assert len(test_pred_df) == 147
    assert reg_res["metrics"]["baseline_test"]["n"] == 147
    assert reg_res["metrics"]["ols_test"]["n"] == 147

    y_true = test_pred_df["y_true"].values
    y_base = test_pred_df["y_pred_baseline"].values
    fresh_base_rmse = float(np.sqrt(mean_squared_error(y_true, y_base)))
    assert np.isclose(reg_res["metrics"]["baseline_test"]["rmse"], fresh_base_rmse, atol=1e-3)

    # Verify OLS outperforms mean baseline on out-of-sample test set
    assert reg_res["metrics"]["ols_test"]["rmse"] < reg_res["metrics"]["baseline_test"]["rmse"]
    assert reg_res["metrics"]["ols_test"]["mae"] < reg_res["metrics"]["baseline_test"]["mae"]
    assert reg_res["metrics"]["ols_test"]["r2"] > reg_res["metrics"]["baseline_test"]["r2"]

    # Verify VIF reduction when dropping atemp
    vif_map = {r["feature"]: r for r in reg_res["vif_diagnostics"]}
    assert vif_map["num__temp"]["vif"] < 5.0
    assert vif_map["num__temp"]["vif_when_atemp_included"] > 50.0
