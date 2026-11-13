"""Phase 1: Dataset loading, SHA-256 verification, schema validation, and shared stats helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
DAY_CSV_PATH = RAW_DATA_DIR / "day.csv"
README_TXT_PATH = RAW_DATA_DIR / "Readme.txt"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
TABLES_DIR = OUTPUTS_DIR / "tables"

EXPECTED_DAY_CSV_SHA256 = "a6bcf826782d3c0fbfdcbeead17cd0884185a0dafe8ff10cd48a874ee7ba18be"
EXPECTED_COLUMNS = [
    "instant", "dteday", "season", "yr", "mnth", "holiday", "weekday",
    "workingday", "weathersit", "temp", "atemp", "hum", "windspeed",
    "casual", "registered", "cnt",
]
CONTINUOUS_VARIABLES = ["cnt", "casual", "registered", "temp", "atemp", "hum", "windspeed"]

SEASON_SHORT_LABELS = {
    1: "1: Spring (UCI 1)",
    2: "2: Summer (UCI 2)",
    3: "3: Fall (UCI 3)",
    4: "4: Winter (UCI 4)",
}
SEASON_LABELS = {
    1: "1: Spring (Dec 21–Mar 20)",
    2: "2: Summer (Mar 21–Jun 20)",
    3: "3: Fall (Jun 21–Sep 22)",
    4: "4: Winter (Sep 23–Dec 20)",
}
WEATHERSIT_LABELS = {
    1: "1: Clear / Partly Cloudy",
    2: "2: Mist / Cloudy",
    3: "3: Light Snow / Light Rain",
    4: "4: Heavy Rain / Ice Pellets",
}
WORKINGDAY_LABELS = {
    0: "0: Non-Working Day",
    1: "1: Working Day",
}
YEAR_LABELS = {0: "2011 (Year 0)", 1: "2012 (Year 1)"}


def compute_sha256(file_path: Path) -> str:
    """Return hex SHA-256 digest of `file_path`."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_series_stats(s: pd.Series) -> Dict[str, float]:
    """Compute canonical parametric and non-parametric summary statistics for a numeric Series."""
    clean = s.dropna().astype(float)
    arr = clean.to_numpy()
    n = len(arr)
    mean, sd, var = float(np.mean(arr)), float(np.std(arr, ddof=1)), float(np.var(arr, ddof=1))
    se = float(sd / np.sqrt(n))
    hw = float(stats.t.ppf(0.975, df=n - 1) * se)
    q25, med, q75 = [float(x) for x in np.percentile(arr, [25, 50, 75])]
    iqr = q75 - q25
    min_v, max_v = float(np.min(arr)), float(np.max(arr))

    vc = clean.value_counts()
    if int(vc.iloc[0]) > 1:
        mode_v = float(vc.index[0])
    else:
        hist_c, edges = np.histogram(arr, bins="fd")
        idx = int(np.argmax(hist_c))
        mode_v = float(0.5 * (edges[idx] + edges[idx + 1]))

    return {
        "n": int(n),
        "mean": round(mean, 4),
        "sd": round(sd, 4),
        "variance": round(var, 4),
        "se_mean": round(se, 4),
        "ci95_mean_low": round(mean - hw, 4),
        "ci95_mean_high": round(mean + hw, 4),
        "trimmed_mean_10pct": round(float(stats.trim_mean(arr, 0.10)), 4),
        "mode_empirical": round(mode_v, 4),
        "min": round(min_v, 4),
        "q25": round(q25, 4),
        "median": round(med, 4),
        "q75": round(q75, 4),
        "max": round(max_v, 4),
        "range": round(max_v - min_v, 4),
        "iqr": round(iqr, 4),
        "mad_median": round(float(np.median(np.abs(arr - med))), 4),
        "cv_pct": round(100.0 * sd / mean, 4) if abs(mean) > 1e-12 else float("nan"),
        "skewness": round(float(stats.skew(arr, bias=False)), 4),
        "excess_kurtosis": round(float(stats.kurtosis(arr, fisher=True, bias=False)), 4),
    }


def load_and_validate_data(
    csv_path: Path = DAY_CSV_PATH, save_outputs: bool = True
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Load `day.csv`, validate schema/domains/invariants, and export data quality audit."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")
    sha = compute_sha256(csv_path)
    if sha != EXPECTED_DAY_CSV_SHA256:
        raise ValueError(f"SHA-256 mismatch: expected {EXPECTED_DAY_CSV_SHA256}, got {sha}")

    raw_df = pd.read_csv(csv_path)
    if list(raw_df.columns) != EXPECTED_COLUMNS:
        raise ValueError(f"Schema mismatch: {list(raw_df.columns)}")
    n_rows, n_cols = raw_df.shape
    if n_rows < 500 or n_cols < 5:
        raise ValueError(f"Dimensions {n_rows}x{n_cols} below minimum 500x5.")

    parsed_dates = pd.to_datetime(raw_df["dteday"], format="%Y-%m-%d", errors="raise")
    is_monotonic = bool(parsed_dates.is_monotonic_increasing)
    is_consecutive = bool((parsed_dates.diff().dropna().dt.days == 1).all())
    total_missing = int(raw_df.isna().sum().sum())
    dup_rows = int(raw_df.duplicated().sum())
    dup_dates = int(raw_df["dteday"].duplicated().sum())
    id_violations = int((raw_df["cnt"] != raw_df["casual"] + raw_df["registered"]).sum())

    domain_checks = {
        "season": bool(raw_df["season"].isin([1, 2, 3, 4]).all()),
        "yr": bool(raw_df["yr"].isin([0, 1]).all()),
        "mnth": bool(raw_df["mnth"].isin(range(1, 13)).all()),
        "holiday": bool(raw_df["holiday"].isin([0, 1]).all()),
        "weekday": bool(raw_df["weekday"].isin(range(0, 7)).all()),
        "workingday": bool(raw_df["workingday"].isin([0, 1]).all()),
        "weathersit": bool(raw_df["weathersit"].isin([1, 2, 3, 4]).all()),
        "unit_bounds": bool(
            all(raw_df[c].between(0.0, 1.0).all() for c in ["temp", "atemp", "hum", "windspeed"])
        ),
        "counts_valid": bool(
            (raw_df["casual"] >= 0).all() and (raw_df["registered"] >= 0).all() and (raw_df["cnt"] > 0).all()
        ),
    }
    if total_missing or dup_rows or dup_dates or id_violations or not (is_monotonic and is_consecutive) or not all(domain_checks.values()):
        raise ValueError("Data validation check failed.")

    df = raw_df.copy()
    df["dteday_parsed"] = parsed_dates
    df["season_label"] = df["season"].map(SEASON_SHORT_LABELS)
    df["weathersit_label"] = df["weathersit"].map(WEATHERSIT_LABELS)
    df["workingday_label"] = df["workingday"].map(WORKINGDAY_LABELS)
    df["year_label"] = df["yr"].map(YEAR_LABELS)
    df["temp_celsius"] = df["temp"] * 41.0
    df["atemp_celsius"] = df["atemp"] * 50.0
    df["hum_pct"] = df["hum"] * 100.0
    df["windspeed_kmh"] = df["windspeed"] * 67.0
    df["high_demand"] = (df["cnt"] > float(df["cnt"].median())).astype(int)

    dict_rows = []
    for col in EXPECTED_COLUMNS:
        s = raw_df[col]
        num = pd.api.types.is_numeric_dtype(s)
        dict_rows.append({
            "column": col, "dtype": str(s.dtype), "missing_count": int(s.isna().sum()),
            "unique_count": int(s.nunique()), "min": float(s.min()) if num else str(s.min()),
            "max": float(s.max()) if num else str(s.max()),
            "mean": round(float(s.mean()), 4) if num else None,
            "std": round(float(s.std(ddof=1)), 4) if num else None,
            "median": round(float(s.median()), 4) if num else None,
        })

    gap_s = (raw_df["temp"] - raw_df["atemp"]).abs()
    audit_report: Dict[str, Any] = {
        "dataset_name": "UCI Bike Sharing Dataset (day.csv)",
        "provenance": {
            "day_csv_path": str(csv_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "day_csv_sha256": sha,
            "day_csv_checksum_verified": True,
            "readme_exists": README_TXT_PATH.exists(),
        },
        "dimensions": {"n_rows": int(n_rows), "n_cols": int(n_cols)},
        "temporal_coverage": {
            "start_date": str(raw_df["dteday"].iloc[0]),
            "end_date": str(raw_df["dteday"].iloc[-1]),
            "n_days_2011": int((raw_df["yr"] == 0).sum()),
            "n_days_2012": int((raw_df["yr"] == 1).sum()),
            "is_monotonic_increasing": is_monotonic,
            "is_consecutive_daily_without_gaps": is_consecutive,
        },
        "data_quality": {
            "total_missing_cells": total_missing,
            "duplicate_rows": dup_rows,
            "duplicate_dates": dup_dates,
            "target_identity_violations": id_violations,
            "domain_checks": domain_checks,
            "zero_humidity_dates": raw_df.loc[raw_df["hum"] == 0.0, "dteday"].tolist(),
            "temp_atemp_anomaly_dates": raw_df.loc[gap_s > 0.20, "dteday"].tolist(),
        },
    }

    if save_outputs:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        TABLES_DIR.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(dict_rows).to_csv(TABLES_DIR / "data_dictionary_summary.csv", index=False)
        with open(OUTPUTS_DIR / "dataset_audit.json", "w", encoding="utf-8") as f:
            json.dump(audit_report, f, indent=2)

    return df, audit_report
