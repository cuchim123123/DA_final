"""Model training, Stratified 5-Fold CV tuning, probability calibration, and threshold selection."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    f1_score,
    log_loss,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline

from telco_churn.config import MODELS_DIR, N_CV_FOLDS, RANDOM_STATE, TABLES_DIR
from telco_churn.modeling.pipeline import build_preprocessor
from telco_churn.modeling.split import DatasetSplit


@dataclass
class TrainingBundle:
    cv_summary_df: pd.DataFrame
    fitted_models: dict[str, Pipeline]
    oof_probs: dict[str, np.ndarray]
    champion_name: str
    baseline_name: str
    optimal_threshold: float
    calibration_applied: bool
    cv_details: dict[str, Any]


def compute_ece(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
    """Compute Expected Calibration Error across equal-width probability bins."""
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    n = len(y_true)
    for lo, hi in zip(bins[:-1], bins[1:], strict=True):
        if hi == 1.0:
            mask = (y_prob >= lo) & (y_prob <= hi)
        else:
            mask = (y_prob >= lo) & (y_prob < hi)
        if mask.any():
            acc = float(y_true[mask].mean())
            conf = float(y_prob[mask].mean())
            ece += (mask.sum() / n) * abs(acc - conf)
    return float(ece)


def select_validation_f1_threshold(y_true: np.ndarray, oof_prob: np.ndarray) -> tuple[float, float]:
    """Select decision cutoff exclusively on out-of-fold validation predictions maximizing F1."""
    thresholds = np.linspace(0.15, 0.70, 111)
    best_tau = 0.50
    best_f1 = -1.0
    for tau in thresholds:
        preds = (oof_prob >= tau).astype(int)
        score = float(f1_score(y_true, preds, zero_division=0))
        if score > best_f1:
            best_f1 = score
            best_tau = float(round(float(tau), 4))
    return best_tau, float(best_f1)


def _summarize_cv_oof(model_name: str, role: str, y_true: np.ndarray, oof_prob: np.ndarray, best_params: str) -> dict[str, Any]:
    y_arr = np.asarray(y_true, dtype=int)
    preds_05 = (oof_prob >= 0.50).astype(int)
    opt_tau, opt_f1 = select_validation_f1_threshold(y_arr, oof_prob)
    return {
        "model_name": model_name,
        "role": role,
        "cv_roc_auc": round(float(roc_auc_score(y_arr, oof_prob)), 4),
        "cv_pr_auc": round(float(average_precision_score(y_arr, oof_prob)), 4),
        "cv_brier_score": round(float(brier_score_loss(y_arr, oof_prob)), 4),
        "cv_ece": round(compute_ece(y_arr, oof_prob), 4),
        "cv_log_loss": round(float(log_loss(y_arr, np.clip(oof_prob, 1e-6, 1 - 1e-6))), 4),
        "cv_f1_at_0_50": round(float(f1_score(y_arr, preds_05, zero_division=0)), 4),
        "val_optimal_threshold": opt_tau,
        "cv_f1_at_val_threshold": round(opt_f1, 4),
        "best_hyperparameters": best_params,
    }


def train_and_select_models(
    split: DatasetSplit,
    models_dir: Path = MODELS_DIR,
    tables_dir: Path = TABLES_DIR,
    save_artifacts: bool = True,
) -> TrainingBundle:
    """Train fair competing classifiers using training-only 5-fold Stratified CV and calibration checks."""
    cv = StratifiedKFold(n_splits=N_CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    X_tr, y_tr = split.X_train, split.y_train
    y_tr_np = y_tr.to_numpy()

    fitted_models: dict[str, Pipeline] = {}
    oof_probs: dict[str, np.ndarray] = {}
    cv_rows: list[dict[str, Any]] = []

    # 0. Prevalence / Majority Floor Reference (Not counted as a trained ML algorithm)
    dummy_pipe = Pipeline(
        [("prep", build_preprocessor(scale_numeric=False)), ("clf", DummyClassifier(strategy="most_frequent"))]
    )
    dummy_oof = cross_val_predict(dummy_pipe, X_tr, y_tr, cv=cv, method="predict_proba")[:, 1]
    dummy_pipe.fit(X_tr, y_tr)
    fitted_models["Dummy Floor (Most Frequent)"] = dummy_pipe
    oof_probs["Dummy Floor (Most Frequent)"] = dummy_oof
    cv_rows.append(
        _summarize_cv_oof(
            "Dummy Floor (Most Frequent)",
            "Reference No-Skill Floor",
            y_tr_np,
            dummy_oof,
            "strategy='most_frequent'",
        )
    )

    # 1. Baseline Interpretable Classifier: Regularized Logistic Regression
    lr_pipe = Pipeline(
        [
            ("prep", build_preprocessor(scale_numeric=True)),
            ("clf", LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)),
        ]
    )
    lr_gs = GridSearchCV(
        lr_pipe,
        param_grid={"clf__C": [0.05, 0.25, 1.0, 5.0]},
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1,
        refit=True,
    )
    lr_gs.fit(X_tr, y_tr)
    lr_best = lr_gs.best_estimator_
    lr_oof = cross_val_predict(lr_best, X_tr, y_tr, cv=cv, method="predict_proba")[:, 1]
    fitted_models["Logistic Regression"] = lr_best
    oof_probs["Logistic Regression"] = lr_oof
    cv_rows.append(
        _summarize_cv_oof(
            "Logistic Regression",
            "Simple Linear Baseline Model",
            y_tr_np,
            lr_oof,
            str(lr_gs.best_params_),
        )
    )

    # 2. Advanced Bagging Ensemble: Random Forest
    rf_pipe = Pipeline(
        [
            ("prep", build_preprocessor(scale_numeric=False)),
            ("clf", RandomForestClassifier(n_estimators=300, random_state=RANDOM_STATE, n_jobs=-1)),
        ]
    )
    rf_gs = GridSearchCV(
        rf_pipe,
        param_grid={
            "clf__max_depth": [6, 10],
            "clf__min_samples_leaf": [5, 15],
            "clf__max_features": ["sqrt", 0.4],
        },
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1,
        refit=True,
    )
    rf_gs.fit(X_tr, y_tr)
    rf_best = rf_gs.best_estimator_
    rf_oof = cross_val_predict(rf_best, X_tr, y_tr, cv=cv, method="predict_proba")[:, 1]
    fitted_models["Random Forest"] = rf_best
    oof_probs["Random Forest"] = rf_oof
    cv_rows.append(
        _summarize_cv_oof(
            "Random Forest",
            "Advanced Tree Ensemble (Bagging)",
            y_tr_np,
            rf_oof,
            str(rf_gs.best_params_),
        )
    )

    # 3. Advanced Gradient Boosting Ensemble: HistGradientBoosting
    hgb_pipe = Pipeline(
        [
            ("prep", build_preprocessor(scale_numeric=False)),
            ("clf", HistGradientBoostingClassifier(max_iter=250, random_state=RANDOM_STATE)),
        ]
    )
    hgb_gs = GridSearchCV(
        hgb_pipe,
        param_grid={
            "clf__learning_rate": [0.03, 0.06],
            "clf__max_leaf_nodes": [15, 31],
            "clf__min_samples_leaf": [25, 50],
            "clf__l2_regularization": [0.5, 2.0],
        },
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1,
        refit=True,
    )
    hgb_gs.fit(X_tr, y_tr)
    hgb_best = hgb_gs.best_estimator_
    hgb_oof = cross_val_predict(hgb_best, X_tr, y_tr, cv=cv, method="predict_proba")[:, 1]
    fitted_models["HistGradientBoosting"] = hgb_best
    oof_probs["HistGradientBoosting"] = hgb_oof
    cv_rows.append(
        _summarize_cv_oof(
            "HistGradientBoosting",
            "Advanced Tree Ensemble (Boosting)",
            y_tr_np,
            hgb_oof,
            str(hgb_gs.best_params_),
        )
    )

    cv_df = pd.DataFrame(cv_rows)
    # Select champion strictly on non-dummy CV ROC-AUC
    real_candidates = cv_df[cv_df["role"] != "Reference No-Skill Floor"].copy()
    best_row = real_candidates.sort_values(["cv_roc_auc", "cv_pr_auc"], ascending=[False, False]).iloc[0]
    champion_name = str(best_row["model_name"])
    champion_pipe = fitted_models[champion_name]

    # Evaluate sigmoid calibration strictly on OOF CV predictions of the champion
    cal_wrapper = CalibratedClassifierCV(champion_pipe, method="sigmoid", cv=cv)
    cal_oof = cross_val_predict(cal_wrapper, X_tr, y_tr, cv=cv, method="predict_proba")[:, 1]
    raw_brier = float(brier_score_loss(y_tr_np, oof_probs[champion_name]))
    cal_brier = float(brier_score_loss(y_tr_np, cal_oof))
    calibration_applied = cal_brier < raw_brier - 1e-4

    if calibration_applied:
        cal_wrapper.fit(X_tr, y_tr)
        champion_final = cal_wrapper
        champion_oof_final = cal_oof
        cv_rows.append(
            _summarize_cv_oof(
                f"{champion_name} (Sigmoid Calibrated)",
                "Selected Champion Model",
                y_tr_np,
                cal_oof,
                f"Calibrated {champion_name} (CV Brier improved {raw_brier:.4f} -> {cal_brier:.4f})",
            )
        )
        final_champ_label = f"{champion_name} (Sigmoid Calibrated)"
        fitted_models[final_champ_label] = champion_final
        oof_probs[final_champ_label] = champion_oof_final
        cv_df = pd.DataFrame(cv_rows)
    else:
        final_champ_label = champion_name

    opt_threshold, opt_oof_f1 = select_validation_f1_threshold(y_tr_np, oof_probs[final_champ_label])

    if save_artifacts:
        models_dir.mkdir(parents=True, exist_ok=True)
        tables_dir.mkdir(parents=True, exist_ok=True)
        cv_df.to_csv(tables_dir / "model_cv_comparison.csv", index=False)
        joblib.dump(fitted_models[final_champ_label], models_dir / "champion_pipeline.joblib")
        joblib.dump(fitted_models["Logistic Regression"], models_dir / "logistic_regression_pipeline.joblib")
        joblib.dump(fitted_models, models_dir / "all_fitted_models.joblib")

    cv_details = {
        "n_cv_folds": N_CV_FOLDS,
        "random_state": RANDOM_STATE,
        "base_champion_model": champion_name,
        "final_champion_label": final_champ_label,
        "baseline_model": "Logistic Regression",
        "calibration_applied": calibration_applied,
        "raw_champion_cv_brier": round(raw_brier, 4),
        "calibrated_champion_cv_brier": round(cal_brier, 4),
        "validation_optimal_threshold": opt_threshold,
        "validation_oof_f1_at_optimal_threshold": round(opt_oof_f1, 4),
    }

    return TrainingBundle(
        cv_summary_df=cv_df,
        fitted_models=fitted_models,
        oof_probs=oof_probs,
        champion_name=final_champ_label,
        baseline_name="Logistic Regression",
        optimal_threshold=opt_threshold,
        calibration_applied=calibration_applied,
        cv_details=cv_details,
    )
