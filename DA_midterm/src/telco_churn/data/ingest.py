"""Acquire the official IBM Telco Customer Churn CSV and verify cryptographic provenance."""

from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from telco_churn.config import (
    DATA_RAW_DIR,
    DATASET_CAVEAT,
    IBM_DATASET_URL,
    IBM_REPO_URL,
    PROVENANCE_PATH,
    RAW_CSV_PATH,
)


def compute_sha256(file_path: Path) -> str:
    """Compute hex SHA-256 checksum for a file using chunked streaming."""
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def acquire_dataset(
    csv_path: Path = RAW_CSV_PATH,
    provenance_path: Path = PROVENANCE_PATH,
    dataset_url: str = IBM_DATASET_URL,
    force_download: bool = False,
) -> dict[str, Any]:
    """Ensure the official IBM CSV exists locally, verify checksum, and persist provenance."""
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    downloaded_now = False

    if force_download or not csv_path.exists():
        req = urllib.request.Request(
            dataset_url,
            headers={"User-Agent": "telco-churn-analytics/1.0 (academic-project)"},
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"Failed to download dataset from {dataset_url}; HTTP status {response.status}"
                )
            payload = response.read()
        csv_path.write_bytes(payload)
        downloaded_now = True

    actual_sha256 = compute_sha256(csv_path)
    actual_bytes = csv_path.stat().st_size

    if provenance_path.exists() and not downloaded_now:
        existing = json.loads(provenance_path.read_text(encoding="utf-8"))
        expected_sha256 = existing.get("sha256")
        if expected_sha256 and expected_sha256 != actual_sha256:
            raise ValueError(
                f"Checksum mismatch for {csv_path}: expected {expected_sha256}, got {actual_sha256}"
            )
        provenance = existing
        provenance["last_verified_utc"] = datetime.now(UTC).isoformat()
        provenance["checksum_verified"] = True
    else:
        provenance = {
            "dataset_name": "IBM Sample Telco Customer Churn Dataset",
            "filename": csv_path.name,
            "relative_path": "data/raw/Telco-Customer-Churn.csv",
            "source_url": dataset_url,
            "source_repository": IBM_REPO_URL,
            "retrieved_utc": datetime.now(UTC).isoformat(),
            "last_verified_utc": datetime.now(UTC).isoformat(),
            "file_size_bytes": actual_bytes,
            "sha256": actual_sha256,
            "checksum_verified": True,
            "caveat": DATASET_CAVEAT,
        }

    provenance_path.write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    return provenance
