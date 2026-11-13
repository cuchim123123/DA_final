"""Automated verification tests for Descriptive and Diagnostic analytical layers."""

from __future__ import annotations

import pandas as pd

from telco_churn.analysis import (
    compute_descriptive_analytics,
    compute_diagnostic_analytics,
    generate_descriptive_diagnostic_charts,
)
from telco_churn.data import acquire_dataset, load_and_audit_data


def test_descriptive_and_diagnostic_consistency(tmp_path) -> None:
    acquire_dataset()
    df, _, _, _ = load_and_audit_data()

    tables_dir = tmp_path / "tables"
    figures_dir = tmp_path / "figures"

    desc = compute_descriptive_analytics(df, tables_dir=tables_dir, save_tables=True)
    diag = compute_diagnostic_analytics(df, tables_dir=tables_dir, save_tables=True)
    registry = generate_descriptive_diagnostic_charts(df, desc, diag, figures_dir=figures_dir)

    kpis = desc["kpis"]
    assert kpis["n_customers"] == 7043
    assert kpis["n_churned"] + kpis["n_retained"] == 7043
    assert abs(kpis["overall_churn_rate_pct"] - 26.54) < 0.05

    sub_df = pd.read_csv(tables_dir / "descriptive_subgroups.csv")
    contract_sub = sub_df[sub_df["feature"] == "Contract"]
    assert contract_sub["n_customers"].sum() == 7043
    assert contract_sub["n_churned"].sum() == 1869

    comp_df = pd.read_csv(tables_dir / "descriptive_compound_segments.csv").set_index("segment_name")
    assert comp_df.loc["Fiber optic AND (No OnlineSecurity OR No TechSupport)", "n_customers"] == 2722
    assert (
        comp_df.loc["Fiber optic AND (No OnlineSecurity AND No TechSupport)", "n_customers"]
        + comp_df.loc["Fiber optic AND (Lacks exactly one of Security/TechSupport)", "n_customers"]
        + comp_df.loc["Fiber optic AND (Both OnlineSecurity & TechSupport = Yes)", "n_customers"]
    ) == comp_df.loc["InternetService = Fiber optic (All)", "n_customers"]

    cat_diag = pd.read_csv(tables_dir / "diagnostic_categorical_associations.csv")
    assert (cat_diag["cramers_v"] >= 0).all()
    assert cat_diag.loc[cat_diag["feature"] == "Contract", "cramers_v"].iloc[0] > 0.35

    # Verify confounding demonstration: TotalCharges marginal association vs adjusted odds
    conf_df = pd.read_csv(tables_dir / "diagnostic_confounding_adjusted_odds.csv")
    tc_row = conf_df[conf_df["encoded_term"] == "TotalCharges"].iloc[0]
    assert tc_row["unadjusted_log_odds"] < 0
    assert tc_row["direction_reversed_after_control"] is True or bool(tc_row["direction_reversed_after_control"])

    assert len(registry) == 6
    distinct_types = {r["chart_type"] for r in registry}
    assert len(distinct_types) == 6
    for entry in registry:
        fname = entry["relative_path"].split("/")[-1]
        assert (figures_dir / fname).exists()
