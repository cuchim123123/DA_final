"""
Automated Data Integrity Tests (Phase 1 Verification).

Verifies dataset dimensions, schema, domain bounds, exact accounting identity
(`cnt == casual + registered`), cryptographic SHA-256 immutability of raw data,
and reproducibility of missing/duplicate audit decisions.
"""

from pathlib import Path
import json
import pandas as pd

from src.load_validate import (
    DAY_CSV_PATH,
    EXPECTED_COLUMNS,
    EXPECTED_DAY_CSV_SHA256,
    OUTPUTS_DIR,
    TABLES_DIR,
    compute_sha256,
    load_and_validate_data,
)


def test_dataset_minimum_dimensions() -> None:
    """Verify dataset meets >=500 rows and >=5 columns and matches 731x16."""
    df, audit = load_and_validate_data(save_outputs=True)
    assert df.shape[0] >= 500, "Dataset must have at least 500 observations."
    assert df.shape[1] >= 5, "Dataset must have at least 5 variables."
    assert audit["dimensions"]["n_rows"] == 731
    assert audit["dimensions"]["n_cols"] == 16


def test_data_dictionary_matches_csv() -> None:
    """Verify required columns, legal categories, parseable dates, and normalized ranges."""
    raw_df = pd.read_csv(DAY_CSV_PATH)
    assert list(raw_df.columns) == EXPECTED_COLUMNS

    # Verify parseable consecutive dates
    dates = pd.to_datetime(raw_df["dteday"], format="%Y-%m-%d", errors="raise")
    assert dates.is_monotonic_increasing
    assert (dates.diff().dropna().dt.days == 1).all()

    # Verify categorical domains
    assert set(raw_df["season"].unique()) == {1, 2, 3, 4}
    assert set(raw_df["yr"].unique()) == {0, 1}
    assert set(raw_df["mnth"].unique()) == set(range(1, 13))
    assert set(raw_df["holiday"].unique()) == {0, 1}
    assert set(raw_df["weekday"].unique()) == set(range(0, 7))
    assert set(raw_df["workingday"].unique()) == {0, 1}
    assert set(raw_df["weathersit"].unique()).issubset({1, 2, 3, 4})

    # Verify normalized continuous bounds in [0, 1]
    for col in ["temp", "atemp", "hum", "windspeed"]:
        assert (raw_df[col] >= 0.0).all() and (raw_df[col] <= 1.0).all(), f"{col} out of [0, 1]"


def test_target_invariant() -> None:
    """Verify exact accounting identity cnt == casual + registered for every row."""
    raw_df = pd.read_csv(DAY_CSV_PATH)
    assert (raw_df["cnt"] == raw_df["casual"] + raw_df["registered"]).all()


def test_raw_data_unchanged() -> None:
    """Verify raw CSV SHA-256 matches the official UCI checksum without modification."""
    assert DAY_CSV_PATH.exists(), "data/raw/day.csv is missing."
    assert compute_sha256(DAY_CSV_PATH) == EXPECTED_DAY_CSV_SHA256


def test_duplicate_and_missing_decisions() -> None:
    """Verify audit file exists, reports zero missing/duplicates, and introduces no fake cleaning."""
    _, audit = load_and_validate_data(save_outputs=True)
    audit_path = OUTPUTS_DIR / "dataset_audit.json"
    dict_table_path = TABLES_DIR / "data_dictionary_summary.csv"

    assert audit_path.exists()
    assert dict_table_path.exists()

    with open(audit_path, "r", encoding="utf-8") as f:
        saved_audit = json.load(f)

    assert saved_audit["data_quality"]["total_missing_cells"] == 0
    assert saved_audit["data_quality"]["duplicate_rows"] == 0
    assert saved_audit["data_quality"]["duplicate_dates"] == 0
    assert saved_audit["data_quality"]["target_identity_violations"] == 0
