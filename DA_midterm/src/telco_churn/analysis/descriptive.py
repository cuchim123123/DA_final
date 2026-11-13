"""Descriptive analytics: headline KPIs, distributions, subgroup counts/rates, and 95% Wilson CIs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pandas as pd

from telco_churn.config import (
    CATEGORICAL_FEATURES,
    CONTRACT_ORDER,
    INTERNET_ORDER,
    NUMERIC_FEATURES,
    PAYMENT_ORDER,
    TABLES_DIR,
    TENURE_TIER_BINS,
    TENURE_TIER_LABELS,
)


def wilson_ci_pct(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Compute binomial proportion 95% Wilson score confidence interval in percentage points."""
    if total <= 0:
        return (0.0, 0.0)
    p = successes / total
    denom = 1.0 + (z * z) / total
    center = (p + (z * z) / (2.0 * total)) / denom
    half_width = (z * math.sqrt((p * (1.0 - p) + (z * z) / (4.0 * total)) / total)) / denom
    return (max(0.0, (center - half_width) * 100.0), min(100.0, (center + half_width) * 100.0))


def add_derived_analysis_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Create non-mutating exploratory grouping columns (for EDA/Diagnostics only, not ML raw features)."""
    out = df.copy()
    out["tenure_tier"] = pd.cut(
        out["tenure"], bins=TENURE_TIER_BINS, labels=TENURE_TIER_LABELS
    ).astype(str)
    out["SeniorCitizenLabel"] = out["SeniorCitizen"].map({0: "No (0)", 1: "Yes (1)"})
    return out


def _summarize_numeric_series(s: pd.Series) -> dict[str, float | int]:
    clean = s.dropna().astype(float)
    q25 = float(clean.quantile(0.25))
    q75 = float(clean.quantile(0.75))
    return {
        "n_valid": int(clean.shape[0]),
        "missing_count": int(s.isna().sum()),
        "mean": round(float(clean.mean()), 4),
        "sd": round(float(clean.std(ddof=1)), 4),
        "min": round(float(clean.min()), 4),
        "q25": round(q25, 4),
        "median": round(float(clean.median()), 4),
        "q75": round(q75, 4),
        "max": round(float(clean.max()), 4),
        "iqr": round(q75 - q25, 4),
        "skewness": round(float(clean.skew()), 4),
    }


def _ordered_categories(series: pd.Series, col_name: str) -> list[Any]:
    observed = list(series.dropna().unique())
    custom_orders = {
        "Contract": CONTRACT_ORDER,
        "InternetService": INTERNET_ORDER,
        "PaymentMethod": PAYMENT_ORDER,
        "tenure_tier": TENURE_TIER_LABELS,
    }
    if col_name in custom_orders:
        ordered = [v for v in custom_orders[col_name] if v in observed]
        extras = [v for v in observed if v not in ordered]
        return ordered + sorted(extras, key=str)
    return sorted(observed, key=str)


def compute_subgroup_rates(df_eda: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Compute subgroup counts, churn rates, 95% Wilson CIs, and revenue exposure."""
    total_n = len(df_eda)
    total_churn = int((df_eda["Churn"] == "Yes").sum())
    rows = []
    for cat in _ordered_categories(df_eda[group_col], group_col):
        sub = df_eda[df_eda[group_col] == cat]
        n = len(sub)
        n_churn = int((sub["Churn"] == "Yes").sum())
        n_retained = n - n_churn
        rate_pct = (n_churn / n * 100.0) if n > 0 else 0.0
        ci_low, ci_high = wilson_ci_pct(n_churn, n)
        rev_at_risk = float(sub.loc[sub["Churn"] == "Yes", "MonthlyCharges"].sum())
        rows.append(
            {
                "feature": group_col,
                "category": str(cat),
                "n_customers": n,
                "pct_of_population": round(n / total_n * 100.0, 2),
                "n_churned": n_churn,
                "n_retained": n_retained,
                "churn_rate_pct": round(rate_pct, 2),
                "ci95_low_pct": round(ci_low, 2),
                "ci95_high_pct": round(ci_high, 2),
                "share_of_all_churn_pct": round(n_churn / total_churn * 100.0, 2) if total_churn else 0.0,
                "mean_tenure_months": round(float(sub["tenure"].mean()), 2),
                "mean_monthly_charges_usd": round(float(sub["MonthlyCharges"].mean()), 2),
                "monthly_revenue_at_risk_usd": round(rev_at_risk, 2),
            }
        )
    return pd.DataFrame(rows)


def compute_compound_segments(df_eda: pd.DataFrame) -> pd.DataFrame:
    """Compute exact counts, churn rates, 95% Wilson CIs, and billing exposure for compound cohorts."""
    total_n = len(df_eda)
    total_churn = int((df_eda["Churn"] == "Yes").sum())
    fiber = df_eda["InternetService"] == "Fiber optic"
    no_sec = df_eda["OnlineSecurity"] == "No"
    no_tech = df_eda["TechSupport"] == "No"
    has_sec = df_eda["OnlineSecurity"] == "Yes"
    has_tech = df_eda["TechSupport"] == "Yes"
    m2m = df_eda["Contract"] == "Month-to-month"

    segment_masks = [
        ("Contract = Month-to-month (All)", "Broad Contract Cohort", m2m),
        ("Month-to-month AND tenure 1-12 mo", "REC-1 Target Cohort", m2m & (df_eda["tenure_tier"] == "1-12 mo")),
        ("InternetService = Fiber optic (All)", "Broad Fiber Cohort", fiber),
        (
            "Fiber optic AND (No OnlineSecurity OR No TechSupport)",
            "REC-2 Target Cohort",
            fiber & (no_sec | no_tech),
        ),
        (
            "Fiber optic AND (No OnlineSecurity AND No TechSupport)",
            "REC-2 Highest-Risk Core",
            fiber & no_sec & no_tech,
        ),
        (
            "Fiber optic AND (Lacks exactly one of Security/TechSupport)",
            "Fiber Partition Sub-Cohort",
            fiber & ((no_sec & has_tech) | (has_sec & no_tech)),
        ),
        (
            "Fiber optic AND (Both OnlineSecurity & TechSupport = Yes)",
            "Fiber Protected Comparison",
            fiber & has_sec & has_tech,
        ),
        ("PaymentMethod = Electronic check (All)", "REC-3 Target Cohort", df_eda["PaymentMethod"] == "Electronic check"),
    ]

    rows = []
    for label, role, mask in segment_masks:
        sub = df_eda.loc[mask]
        n = len(sub)
        n_churn = int((sub["Churn"] == "Yes").sum())
        rate = (n_churn / n * 100.0) if n > 0 else 0.0
        lo, hi = wilson_ci_pct(n_churn, n)
        rev_at_risk = float(sub.loc[sub["Churn"] == "Yes", "MonthlyCharges"].sum())
        rows.append(
            {
                "segment_name": label,
                "analytical_role": role,
                "n_customers": n,
                "pct_of_population": round(n / total_n * 100.0, 2) if total_n else 0.0,
                "n_churned": n_churn,
                "n_retained": n - n_churn,
                "churn_rate_pct": round(rate, 2),
                "ci95_low_pct": round(lo, 2),
                "ci95_high_pct": round(hi, 2),
                "share_of_all_churn_pct": round(n_churn / total_churn * 100.0, 2) if total_churn else 0.0,
                "mean_monthly_charges_usd": round(float(sub["MonthlyCharges"].mean()), 2) if n else 0.0,
                "monthly_revenue_at_risk_usd": round(rev_at_risk, 2),
            }
        )
    return pd.DataFrame(rows)


def compute_descriptive_analytics(
    df: pd.DataFrame,
    tables_dir: Path = TABLES_DIR,
    save_tables: bool = True,
) -> dict[str, Any]:
    """Run full descriptive analytics and optionally persist summary CSV tables."""
    df_eda = add_derived_analysis_columns(df)
    n_total = len(df_eda)
    n_churn = int((df_eda["Churn"] == "Yes").sum())
    n_retained = n_total - n_churn
    churn_rate_pct = n_churn / n_total * 100.0
    ci_low, ci_high = wilson_ci_pct(n_churn, n_total)

    total_monthly_rev = float(df_eda["MonthlyCharges"].sum())
    churned_monthly_rev = float(df_eda.loc[df_eda["Churn"] == "Yes", "MonthlyCharges"].sum())

    kpis = {
        "n_customers": n_total,
        "n_churned": n_churn,
        "n_retained": n_retained,
        "overall_churn_rate_pct": round(churn_rate_pct, 2),
        "overall_churn_ci95_low_pct": round(ci_low, 2),
        "overall_churn_ci95_high_pct": round(ci_high, 2),
        "total_monthly_charges_usd": round(total_monthly_rev, 2),
        "monthly_revenue_at_risk_usd": round(churned_monthly_rev, 2),
        "monthly_revenue_at_risk_pct": round(churned_monthly_rev / total_monthly_rev * 100.0, 2),
        "mean_tenure_months": round(float(df_eda["tenure"].mean()), 2),
        "median_tenure_months": round(float(df_eda["tenure"].median()), 2),
        "mean_monthly_charges_usd": round(float(df_eda["MonthlyCharges"].mean()), 2),
        "median_monthly_charges_usd": round(float(df_eda["MonthlyCharges"].median()), 2),
        "mean_total_charges_usd": round(float(df_eda["TotalCharges"].mean()), 2),
        "median_total_charges_usd": round(float(df_eda["TotalCharges"].median()), 2),
    }

    # Numeric distributions overall and stratified by Churn
    num_rows = []
    for var in NUMERIC_FEATURES:
        overall_stats = _summarize_numeric_series(df_eda[var])
        num_rows.append({"variable": var, "segment": "All Customers", **overall_stats})
        for label in ("No", "Yes"):
            seg_stats = _summarize_numeric_series(df_eda.loc[df_eda["Churn"] == label, var])
            num_rows.append({"variable": var, "segment": f"Churn = {label}", **seg_stats})
    numeric_df = pd.DataFrame(num_rows)

    # Subgroup breakdowns across categorical predictors + SeniorCitizenLabel + tenure_tier
    group_cols = ["Contract", "tenure_tier", "InternetService", "PaymentMethod", "PaperlessBilling", "SeniorCitizenLabel"]
    for col in CATEGORICAL_FEATURES:
        if col not in group_cols:
            group_cols.append(col)
    subgroups_df = pd.concat([compute_subgroup_rates(df_eda, c) for c in group_cols], ignore_index=True)

    # Two-way Contract x Tenure Tier summary table
    ct_rows = []
    for contract in CONTRACT_ORDER:
        for tier in TENURE_TIER_LABELS:
            sub = df_eda[(df_eda["Contract"] == contract) & (df_eda["tenure_tier"] == tier)]
            n = len(sub)
            n_c = int((sub["Churn"] == "Yes").sum())
            rate = (n_c / n * 100.0) if n > 0 else float("nan")
            lo, hi = wilson_ci_pct(n_c, n) if n > 0 else (float("nan"), float("nan"))
            ct_rows.append(
                {
                    "Contract": contract,
                    "tenure_tier": tier,
                    "n_customers": n,
                    "n_churned": n_c,
                    "churn_rate_pct": round(rate, 2) if n > 0 else float("nan"),
                    "ci95_low_pct": round(lo, 2) if n > 0 else float("nan"),
                    "ci95_high_pct": round(hi, 2) if n > 0 else float("nan"),
                }
            )
    contract_tenure_df = pd.DataFrame(ct_rows)
    compound_df = compute_compound_segments(df_eda)

    if save_tables:
        tables_dir.mkdir(parents=True, exist_ok=True)
        pd.DataFrame([kpis]).to_csv(tables_dir / "descriptive_kpis.csv", index=False)
        numeric_df.to_csv(tables_dir / "descriptive_numeric_summary.csv", index=False)
        subgroups_df.to_csv(tables_dir / "descriptive_subgroups.csv", index=False)
        contract_tenure_df.to_csv(tables_dir / "descriptive_contract_by_tenure.csv", index=False)
        compound_df.to_csv(tables_dir / "descriptive_compound_segments.csv", index=False)

    return {
        "kpis": kpis,
        "numeric_summary_table": numeric_df.to_dict(orient="records"),
        "subgroups_table": subgroups_df.to_dict(orient="records"),
        "contract_by_tenure_table": contract_tenure_df.to_dict(orient="records"),
        "compound_segments_table": compound_df.to_dict(orient="records"),
    }
