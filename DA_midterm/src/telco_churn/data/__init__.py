"""Data acquisition, cryptographic provenance verification, and schema validation modules."""

from telco_churn.data.ingest import acquire_dataset, compute_sha256
from telco_churn.data.validate import (
    export_data_audit,
    load_and_audit_data,
    validate_customer_record,
)

__all__ = [
    "acquire_dataset",
    "compute_sha256",
    "export_data_audit",
    "load_and_audit_data",
    "validate_customer_record",
]
