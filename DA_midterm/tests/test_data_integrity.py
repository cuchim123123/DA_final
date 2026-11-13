"""Automated data integrity, provenance, and schema validation tests."""

from __future__ import annotations

import pandas as pd

from telco_churn.config import EXPECTED_COLUMNS, PROVENANCE_PATH, RAW_CSV_PATH
from telco_churn.data import acquire_dataset, load_and_audit_data, validate_customer_record


def test_acquire_and_checksum() -> None:
    provenance = acquire_dataset()
    assert RAW_CSV_PATH.exists()
    assert PROVENANCE_PATH.exists()
    assert provenance["checksum_verified"] is True
    assert len(provenance["sha256"]) == 64


def test_schema_dimensions_and_quality_audit() -> None:
    acquire_dataset()
    df, overview, schema_df, audit_df = load_and_audit_data()

    assert list(df.columns) == EXPECTED_COLUMNS
    assert len(df) == 7043
    assert df.shape[1] == 21
    assert df["customerID"].nunique() == 7043
    assert set(df["Churn"].unique()) == {"No", "Yes"}

    dq = overview["data_quality"]
    assert dq["exact_duplicate_rows"] == 0
    assert dq["blank_total_charges_count"] == 11
    assert dq["all_blank_total_charges_are_tenure_zero"] is True
    assert dq["service_consistency"]["phone_service_mismatches"] == 0
    assert dq["service_consistency"]["internet_service_mismatches"] == 0
    assert len(schema_df) == 21
    assert not audit_df.empty


def test_customer_record_service_hierarchy_validation() -> None:
    valid_record = {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 12,
        "PhoneService": "No",
        "MultipleLines": "No phone service",
        "InternetService": "DSL",
        "OnlineSecurity": "Yes",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "Yes",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "One year",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Bank transfer (automatic)",
        "MonthlyCharges": 45.5,
        "TotalCharges": 546.0,
    }
    assert validate_customer_record(valid_record) == []

    bad_phone = dict(valid_record, MultipleLines="Yes")
    assert any("No phone service" in e for e in validate_customer_record(bad_phone))

    bad_internet = dict(valid_record, InternetService="No")
    assert any("No internet service" in e for e in validate_customer_record(bad_internet))
    assert pd.isna(pd.Series([None], dtype="float64")).all()
