"""Automated tests for self-contained report_evidence_package and ZIP validation."""

from __future__ import annotations

import pandas as pd

from telco_churn.config import REPORT_PACKAGE_DIR, REPORT_PACKAGE_ZIP
from telco_churn.reporting import build_and_validate_evidence_package, validate_evidence_package


def test_evidence_package_export_and_integrity() -> None:
    summary = build_and_validate_evidence_package()
    assert summary["n_files"] >= 45
    assert summary["n_csv"] >= 18
    assert summary["n_png"] == 14  # 10 analytical charts + 4 live dashboard screenshots
    assert summary["n_distinct_chart_types"] >= 6
    assert summary["zip_size_bytes"] > 500_000

    recheck = validate_evidence_package(REPORT_PACKAGE_DIR, REPORT_PACKAGE_ZIP)
    assert recheck["n_files"] == summary["n_files"]

    # Confirm all 10 analytical charts have non-empty interpretations and distinct types
    chart_inv = pd.read_csv(
        REPORT_PACKAGE_DIR / "06_references_and_report_helpers" / "chart_inventory.csv"
    )
    assert len(chart_inv) == 10
    assert chart_inv["interpretation_1"].notna().all()
    assert chart_inv["interpretation_2"].notna().all()
    assert chart_inv["title"].notna().all()
    assert chart_inv["axis_labels"].notna().all()
