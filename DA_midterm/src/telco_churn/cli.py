"""Unified CLI entrypoint orchestrating the complete Telco Churn Analytics pipeline."""

from __future__ import annotations

import argparse
import json
import time
from typing import Any

from telco_churn.analysis import (
    compute_descriptive_analytics,
    compute_diagnostic_analytics,
    generate_descriptive_diagnostic_charts,
)
from telco_churn.config import RESULTS_SUMMARY_PATH
from telco_churn.data import acquire_dataset, export_data_audit, load_and_audit_data
from telco_churn.modeling import (
    evaluate_and_plot_models,
    explain_and_plot_models,
    make_stratified_split,
    train_and_select_models,
)
from telco_churn.recommendations import compute_prescriptive_analytics


def run_all(force_download: bool = False) -> dict[str, Any]:
    """Execute Phases 1-4 deterministically from clean raw data through prescriptive artifacts."""
    t0 = time.perf_counter()

    acquire_dataset(force_download=force_download)
    df, overview, schema_df, audit_df = load_and_audit_data()
    export_data_audit(overview, schema_df, audit_df)

    descriptive_res = compute_descriptive_analytics(df)
    diagnostic_res = compute_diagnostic_analytics(df)
    eda_charts = generate_descriptive_diagnostic_charts(df, descriptive_res, diagnostic_res)

    split = make_stratified_split(df)
    bundle = train_and_select_models(split)
    eval_res = evaluate_and_plot_models(split, bundle)
    explain_res = explain_and_plot_models(split, bundle)

    prescriptive_res = compute_prescriptive_analytics(
        df=df,
        descriptive_res=descriptive_res,
        diagnostic_res=diagnostic_res,
        eval_res=eval_res,
        explain_res=explain_res,
        val_threshold=bundle.optimal_threshold,
        champion_name=bundle.champion_name,
    )

    chart_inventory = (
        eda_charts
        + eval_res["chart_registry"]
        + [explain_res["chart_entry"], prescriptive_res["chart_entry"]]
    )

    results_summary = {
        "dataset_overview": overview,
        "descriptive": descriptive_res,
        "diagnostic": diagnostic_res,
        "predictive": {
            "split_balance": split.summary_df.to_dict(orient="records"),
            "cv_details": bundle.cv_details,
            "cv_comparison": bundle.cv_summary_df.to_dict(orient="records"),
            "test_comparison": eval_res["test_comparison_table"],
            "permutation_importance": explain_res["permutation_importance"],
            "logistic_odds_ratios": explain_res["logistic_odds_ratios"],
        },
        "prescriptive": {
            "risk_tiers": prescriptive_res["risk_tiers"],
            "capacity_lift": prescriptive_res["capacity_lift"],
            "scenario_sensitivity": prescriptive_res["scenario_sensitivity"],
            "recommendations": prescriptive_res["recommendations"],
        },
        "chart_inventory": chart_inventory,
        "runtime_seconds": round(time.perf_counter() - t0, 2),
    }

    RESULTS_SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_SUMMARY_PATH.write_text(json.dumps(results_summary, indent=2), encoding="utf-8")
    return results_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Telco Customer Churn Analytics Pipeline CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run-all", help="Execute complete data, analytics, modeling, and prescriptive pipeline.")
    run_p.add_argument("--force-download", action="store_true", help="Re-download raw IBM CSV from source URL.")

    sub.add_parser("export-package", help="Assemble and validate report_evidence_package/ and ZIP archive.")

    args = parser.parse_args()
    if args.command == "run-all":
        res = run_all(force_download=args.force_download)
        champ = res["predictive"]["cv_details"]["final_champion_label"]
        print(f"Pipeline completed in {res['runtime_seconds']}s | Champion: {champ} | Charts: {len(res['chart_inventory'])}")
    elif args.command == "export-package":
        from telco_churn.reporting.evidence_exporter import build_and_validate_evidence_package

        summary = build_and_validate_evidence_package()
        print(
            f"Exported {summary['n_files']} files to {summary['package_dir']} "
            f"and {summary['zip_path']} ({summary['zip_size_bytes']:,} bytes)"
        )


if __name__ == "__main__":
    main()
