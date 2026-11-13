"""Pure, testable data loading, cohort filtering, scoring, and scenario helpers for Streamlit."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from telco_churn.analysis.descriptive import add_derived_analysis_columns, wilson_ci_pct
from telco_churn.config import (
    FIGURES_DIR,
    INTERNET_DEPENDENT_COLS,
    MODELS_DIR,
    PHONE_DEPENDENT_COL,
    RAW_PREDICTORS,
    RESULTS_SUMMARY_PATH,
    TABLES_DIR,
)
from telco_churn.data.validate import load_and_audit_data, validate_customer_record
from telco_churn.recommendations.prescriptive import simulate_retention_scenario


@dataclass
class DashboardArtifacts:
    df: pd.DataFrame
    df_eda: pd.DataFrame
    summary: dict[str, Any]
    champion_pipeline: Any
    schema_df: pd.DataFrame
    audit_df: pd.DataFrame
    subgroups_df: pd.DataFrame
    cat_diag_df: pd.DataFrame
    cont_diag_df: pd.DataFrame
    conf_diag_df: pd.DataFrame
    cv_comp_df: pd.DataFrame
    test_comp_df: pd.DataFrame
    test_pred_df: pd.DataFrame
    perm_imp_df: pd.DataFrame
    logistic_or_df: pd.DataFrame
    risk_tiers_df: pd.DataFrame
    lift_df: pd.DataFrame
    sensitivity_df: pd.DataFrame
    recommendations_df: pd.DataFrame


def load_dashboard_artifacts(
    tables_dir: Path = TABLES_DIR,
    models_dir: Path = MODELS_DIR,
    summary_path: Path = RESULTS_SUMMARY_PATH,
) -> DashboardArtifacts:
    """Load precomputed analytical tables, metadata JSON, and persisted ML pipeline."""
    required = [
        summary_path,
        models_dir / "champion_pipeline.joblib",
        tables_dir / "test_predictions.csv",
        tables_dir / "prescriptive_recommendations.csv",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Required precomputed artifacts are missing. Run `python -m telco_churn.cli run-all` first. "
            f"Missing: {missing}"
        )

    df, _, schema_df, audit_df = load_and_audit_data()
    df_eda = add_derived_analysis_columns(df)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    champion_pipeline = joblib.load(models_dir / "champion_pipeline.joblib")

    return DashboardArtifacts(
        df=df,
        df_eda=df_eda,
        summary=summary,
        champion_pipeline=champion_pipeline,
        schema_df=schema_df,
        audit_df=audit_df,
        subgroups_df=pd.read_csv(tables_dir / "descriptive_subgroups.csv"),
        cat_diag_df=pd.read_csv(tables_dir / "diagnostic_categorical_associations.csv"),
        cont_diag_df=pd.read_csv(tables_dir / "diagnostic_continuous_comparisons.csv"),
        conf_diag_df=pd.read_csv(tables_dir / "diagnostic_confounding_adjusted_odds.csv"),
        cv_comp_df=pd.read_csv(tables_dir / "model_cv_comparison.csv"),
        test_comp_df=pd.read_csv(tables_dir / "model_test_comparison.csv"),
        test_pred_df=pd.read_csv(tables_dir / "test_predictions.csv"),
        perm_imp_df=pd.read_csv(tables_dir / "permutation_importance.csv"),
        logistic_or_df=pd.read_csv(tables_dir / "logistic_odds_ratios.csv"),
        risk_tiers_df=pd.read_csv(tables_dir / "prescriptive_risk_tiers.csv"),
        lift_df=pd.read_csv(tables_dir / "prescriptive_capacity_lift.csv"),
        sensitivity_df=pd.read_csv(tables_dir / "prescriptive_scenario_sensitivity.csv"),
        recommendations_df=pd.read_csv(tables_dir / "prescriptive_recommendations.csv"),
    )


def filter_customer_cohort(
    df_eda: pd.DataFrame,
    contracts: list[str] | None = None,
    internet_types: list[str] | None = None,
    payment_methods: list[str] | None = None,
    tenure_range: tuple[int, int] = (0, 72),
    senior_filter: str = "All",
) -> pd.DataFrame:
    """Filter full cross-sectional cohort cleanly without mutating original frame."""
    mask = (df_eda["tenure"] >= tenure_range[0]) & (df_eda["tenure"] <= tenure_range[1])
    if contracts:
        mask &= df_eda["Contract"].isin(contracts)
    if internet_types:
        mask &= df_eda["InternetService"].isin(internet_types)
    if payment_methods:
        mask &= df_eda["PaymentMethod"].isin(payment_methods)
    if senior_filter == "Senior Citizens Only (1)":
        mask &= df_eda["SeniorCitizen"] == 1
    elif senior_filter == "Non-Seniors Only (0)":
        mask &= df_eda["SeniorCitizen"] == 0
    return df_eda.loc[mask].copy()


def compute_filtered_kpis(sub_df: pd.DataFrame) -> dict[str, Any]:
    """Compute exact cohort KPI metrics with 95% Wilson CI and revenue at risk."""
    n = len(sub_df)
    if n == 0:
        return {
            "n_customers": 0,
            "n_churned": 0,
            "churn_rate_pct": 0.0,
            "ci95_low_pct": 0.0,
            "ci95_high_pct": 0.0,
            "monthly_rev_at_risk_usd": 0.0,
            "median_tenure": 0.0,
            "median_monthly_charges": 0.0,
        }
    n_c = int((sub_df["Churn"] == "Yes").sum())
    rate = n_c / n * 100.0
    ci_lo, ci_hi = wilson_ci_pct(n_c, n)
    rev_risk = float(sub_df.loc[sub_df["Churn"] == "Yes", "MonthlyCharges"].sum())
    return {
        "n_customers": n,
        "n_churned": n_c,
        "churn_rate_pct": round(rate, 2),
        "ci95_low_pct": round(ci_lo, 2),
        "ci95_high_pct": round(ci_hi, 2),
        "monthly_rev_at_risk_usd": round(rev_risk, 2),
        "median_tenure": round(float(sub_df["tenure"].median()), 1),
        "median_monthly_charges": round(float(sub_df["MonthlyCharges"].median()), 2),
    }


def compute_threshold_metrics(
    test_pred_df: pd.DataFrame,
    prob_col: str,
    threshold: float,
) -> dict[str, Any]:
    """Recompute confusion matrix and threshold classification metrics on held-out test scores."""
    y_true = test_pred_df["y_true"].to_numpy()
    probs = test_pred_df[prob_col].to_numpy()
    preds = (probs >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, preds, labels=[0, 1]).ravel()
    flagged = int(preds.sum())
    return {
        "threshold": round(float(threshold), 3),
        "n_test": int(len(y_true)),
        "flagged_count": flagged,
        "flagged_pct": round(flagged / len(y_true) * 100.0, 2),
        "accuracy": round(float(accuracy_score(y_true, preds)), 4),
        "precision": round(float(precision_score(y_true, preds, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, preds, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_true, preds, zero_division=0)), 4),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def score_hypothetical_customer(
    pipeline: Any,
    record: dict[str, Any],
    val_threshold: float,
) -> dict[str, Any]:
    """Validate service-hierarchy consistency and score one hypothetical customer via champion pipeline."""
    normalized = dict(record)
    if normalized.get("PhoneService") == "No":
        normalized[PHONE_DEPENDENT_COL] = "No phone service"
    elif normalized.get(PHONE_DEPENDENT_COL) == "No phone service":
        normalized[PHONE_DEPENDENT_COL] = "No"

    if normalized.get("InternetService") == "No":
        for col in INTERNET_DEPENDENT_COLS:
            normalized[col] = "No internet service"
    else:
        for col in INTERNET_DEPENDENT_COLS:
            if normalized.get(col) == "No internet service":
                normalized[col] = "No"

    errors = validate_customer_record(normalized)
    if errors:
        raise ValueError("; ".join(errors))

    payload_df = pd.DataFrame([{col: normalized[col] for col in RAW_PREDICTORS}])
    prob = float(pipeline.predict_proba(payload_df)[0, 1])

    if prob >= 0.50:
        tier = "Tier 1: High Risk (p >= 0.50)"
    elif prob >= val_threshold:
        tier = f"Tier 2: Elevated Risk ({val_threshold:.2f} <= p < 0.50)"
    else:
        tier = f"Tier 3: Low Risk (p < {val_threshold:.2f})"

    return {
        "predicted_churn_probability": round(prob, 4),
        "predicted_churn_probability_pct": round(prob * 100.0, 2),
        "risk_tier": tier,
        "flagged_at_default_050": prob >= 0.50,
        "flagged_at_val_threshold": prob >= val_threshold,
        "normalized_record": normalized,
    }


def get_figure_path(filename: str, figures_dir: Path = FIGURES_DIR) -> Path:
    """Resolve an exported static chart path cleanly."""
    return figures_dir / filename


__all__ = [
    "DashboardArtifacts",
    "compute_filtered_kpis",
    "compute_threshold_metrics",
    "filter_customer_cohort",
    "get_figure_path",
    "load_dashboard_artifacts",
    "score_hypothetical_customer",
    "simulate_retention_scenario",
]
