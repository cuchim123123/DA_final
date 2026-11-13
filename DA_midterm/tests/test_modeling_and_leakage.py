"""Automated anti-leakage, split-isolation, calibration, and metric-recomputation tests."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, average_precision_score, f1_score, roc_auc_score

from telco_churn.config import FORBIDDEN_FEATURE_COLS, RAW_PREDICTORS
from telco_churn.data import acquire_dataset, load_and_audit_data
from telco_churn.modeling import (
    evaluate_and_plot_models,
    explain_and_plot_models,
    make_stratified_split,
    train_and_select_models,
)


def test_split_isolation_and_no_leakage() -> None:
    acquire_dataset()
    df, _, _, _ = load_and_audit_data()
    split = make_stratified_split(df, save_table=False)

    assert len(split.X_train) == 5634
    assert len(split.X_test) == 1409
    assert set(split.ids_train).isdisjoint(set(split.ids_test))
    assert list(split.X_train.columns) == RAW_PREDICTORS
    assert set(split.X_train.columns).isdisjoint(FORBIDDEN_FEATURE_COLS)
    assert abs(split.y_train.mean() - split.y_test.mean()) < 0.005


def test_training_evaluation_recomputation_and_explainability(tmp_path) -> None:
    acquire_dataset()
    df, _, _, _ = load_and_audit_data()
    tables_dir = tmp_path / "tables"
    models_dir = tmp_path / "models"
    figures_dir = tmp_path / "figures"

    split = make_stratified_split(df, tables_dir=tables_dir, save_table=True)
    bundle = train_and_select_models(split, models_dir=models_dir, tables_dir=tables_dir, save_artifacts=True)
    eval_res = evaluate_and_plot_models(split, bundle, tables_dir=tables_dir, figures_dir=figures_dir, save_outputs=True)
    explain_res = explain_and_plot_models(split, bundle, tables_dir=tables_dir, figures_dir=figures_dir, save_outputs=True)

    # Check genuine models present, outperform no-skill floor, and test cutoffs match CV cutoffs 1:1
    cv_df = pd.read_csv(tables_dir / "model_cv_comparison.csv").set_index("model_name")
    test_df = pd.read_csv(tables_dir / "model_test_comparison.csv")
    for m_name in ["Logistic Regression", "Random Forest", "HistGradientBoosting"]:
        opt_row = test_df[(test_df["model_name"] == m_name) & (test_df["threshold_setting"] != "Default (0.50)")].iloc[0]
        assert np.isclose(opt_row["threshold_value"], cv_df.loc[m_name, "val_optimal_threshold"], atol=1e-4)

    lr_auc = test_df.loc[test_df["model_name"] == "Logistic Regression", "roc_auc"].iloc[0]
    rf_auc = test_df.loc[test_df["model_name"] == "Random Forest", "roc_auc"].iloc[0]
    hgb_auc = test_df.loc[test_df["model_name"] == "HistGradientBoosting", "roc_auc"].iloc[0]
    assert lr_auc > 0.80
    assert rf_auc > 0.80
    assert hgb_auc > 0.80

    # Independently recompute metrics directly from saved test_predictions.csv
    pred_df = pd.read_csv(tables_dir / "test_predictions.csv")
    assert len(pred_df) == 1409
    y_true = pred_df["y_true"].to_numpy()
    p_champ = pred_df["prob_champion"].to_numpy()
    tau = bundle.optimal_threshold

    champ_opt_row = test_df[
        (test_df["model_name"] == bundle.champion_name) & (test_df["threshold_setting"] != "Default (0.50)")
    ].iloc[0]
    recomputed_auc = round(float(roc_auc_score(y_true, p_champ)), 4)
    recomputed_pr = round(float(average_precision_score(y_true, p_champ)), 4)
    recomputed_acc = round(float(accuracy_score(y_true, (p_champ >= tau).astype(int))), 4)
    recomputed_f1 = round(float(f1_score(y_true, (p_champ >= tau).astype(int))), 4)

    assert np.isclose(recomputed_auc, champ_opt_row["roc_auc"], atol=1e-4)
    assert np.isclose(recomputed_pr, champ_opt_row["pr_auc"], atol=1e-4)
    assert np.isclose(recomputed_acc, champ_opt_row["accuracy"], atol=1e-4)
    assert np.isclose(recomputed_f1, champ_opt_row["f1_score"], atol=1e-4)

    # Verify single-record scoring consistency on blank TotalCharges (no leakage crash)
    single_new = split.X_test.iloc[[0]].copy()
    single_new["tenure"] = 0
    single_new["TotalCharges"] = np.nan
    single_prob = float(bundle.fitted_models[bundle.champion_name].predict_proba(single_new)[0, 1])
    assert 0.0 <= single_prob <= 1.0

    # Verify explainability covers all 19 predictors and figures exist
    perm_df = pd.DataFrame(explain_res["permutation_importance"])
    assert len(perm_df) == 19
    assert (figures_dir / "fig07_model_roc_pr_calibration_curves.png").exists()
    assert (figures_dir / "fig08_confusion_matrices_heatmap.png").exists()
    assert (figures_dir / "fig09_model_explainability.png").exists()
    assert len(eval_res["chart_registry"]) == 2
