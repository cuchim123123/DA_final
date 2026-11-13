"""Phase 2: Exploratory Data Analysis (EDA), subgroup summaries, and outlier diagnostics."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd
from scipy import stats

from src.load_validate import (
    CONTINUOUS_VARIABLES,
    SEASON_LABELS,
    TABLES_DIR,
    WEATHERSIT_LABELS,
    WORKINGDAY_LABELS,
    YEAR_LABELS,
    compute_series_stats,
    load_and_validate_data,
)

PHYSICAL_UNITS = {
    "cnt": ("bikes/day", 1.0),
    "casual": ("bikes/day", 1.0),
    "registered": ("bikes/day", 1.0),
    "temp": ("normalized [0,1] (×41°C)", 41.0),
    "atemp": ("normalized [0,1] (×50°C)", 50.0),
    "hum": ("normalized [0,1] (×100%)", 100.0),
    "windspeed": ("normalized [0,1] (×67 km/h)", 67.0),
}


def _compute_group_summary(
    df: pd.DataFrame, group_col: str, label_map: Dict[int, str], target_col: str = "cnt"
) -> List[Dict[str, Any]]:
    """Compute subgroup descriptive statistics for `target_col` stratified by `group_col`."""
    total_n = len(df)
    rows: List[Dict[str, Any]] = []
    for code, label in label_map.items():
        sub = df.loc[df[group_col] == code, target_col]
        if sub.empty:
            rows.append({
                "group_variable": group_col, "group_code": int(code), "group_label": label,
                "n": 0, "pct_of_days": 0.0, "mean": np.nan, "sd": np.nan, "se_mean": np.nan,
                "ci95_mean_low": np.nan, "ci95_mean_high": np.nan, "median": np.nan,
                "iqr": np.nan, "min": np.nan, "max": np.nan,
            })
            continue
        st = compute_series_stats(sub)
        rows.append({
            "group_variable": group_col, "group_code": int(code), "group_label": label,
            "n": st["n"], "pct_of_days": round(100.0 * st["n"] / total_n, 2),
            **{k: st[k] for k in ["mean", "sd", "se_mean", "ci95_mean_low", "ci95_mean_high", "median", "iqr", "min", "max"]},
        })
    return rows


def _detect_outliers_table(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Detect outliers across all continuous variables using Tukey 1.5*IQR, 3.0*IQR, and |z| > 3."""
    rows: List[Dict[str, Any]] = []
    for col in CONTINUOUS_VARIABLES:
        s = df[col].astype(float)
        q25, q75 = float(s.quantile(0.25)), float(s.quantile(0.75))
        iqr = q75 - q25
        low15, high15 = q25 - 1.5 * iqr, q75 + 1.5 * iqr
        low30, high30 = q25 - 3.0 * iqr, q75 + 3.0 * iqr
        z = (s - float(s.mean())) / float(s.std(ddof=1))

        iqr_low, iqr_high = s < low15, s > high15
        iqr_mask = iqr_low | iqr_high
        z_mask = z.abs() > 3.0
        iqr_cnt, z_cnt = int(iqr_mask.sum()), int(z_mask.sum())

        rows.append({
            "variable": col,
            "q25": round(q25, 4), "q75": round(q75, 4), "iqr": round(iqr, 4),
            "tukey_lower_fence_1_5_iqr": round(low15, 4),
            "tukey_upper_fence_1_5_iqr": round(high15, 4),
            "iqr_outliers_below_count": int(iqr_low.sum()),
            "iqr_outliers_above_count": int(iqr_high.sum()),
            "iqr_outliers_total_count": iqr_cnt,
            "iqr_outliers_pct": round(100.0 * iqr_cnt / len(s), 2),
            "extreme_3_0_iqr_count": int(((s < low30) | (s > high30)).sum()),
            "zscore_abs_gt_3_count": z_cnt,
            "zscore_abs_gt_3_pct": round(100.0 * z_cnt / len(s), 2),
            "max_abs_zscore": round(float(z.abs().max()), 4),
            "sample_iqr_outlier_dates": ", ".join(df.loc[iqr_mask, "dteday"].astype(str).tolist()[:5]),
            "sample_z_outlier_dates": ", ".join(df.loc[z_mask, "dteday"].astype(str).tolist()[:5]),
        })
    return rows


def _compute_outlier_handling_sensitivity(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Quantify impact of outlier and sensor-anomaly handling strategies on key metrics."""
    df_no_zero_hum = df[df["hum"] > 0.0]
    df_winsor = df.copy()
    for c in ["hum", "windspeed"]:
        q25, q75 = float(df[c].quantile(0.25)), float(df[c].quantile(0.75))
        iqr = q75 - q25
        df_winsor[c] = df[c].clip(q25 - 1.5 * iqr, q75 + 1.5 * iqr)

    rows = []
    for label, sub in [
        ("Untouched Full Dataset", df),
        ("Drop Sensor Anomaly (hum > 0)", df_no_zero_hum),
        ("Winsorized Weather (1.5*IQR)", df_winsor),
    ]:
        r_hum, p_hum = stats.pearsonr(sub["hum"].astype(float), sub["cnt"].astype(float))
        r_wind, p_wind = stats.pearsonr(sub["windspeed"].astype(float), sub["cnt"].astype(float))
        rows.append({
            "strategy": label,
            "n_days": int(len(sub)),
            "mean_cnt": round(float(sub["cnt"].mean()), 2),
            "sd_cnt": round(float(sub["cnt"].std(ddof=1)), 2),
            "pearson_r_cnt_hum": round(float(r_hum), 4),
            "pearson_p_cnt_hum": float(p_hum),
            "pearson_r_cnt_windspeed": round(float(r_wind), 4),
            "pearson_p_cnt_windspeed": float(p_wind),
        })
    return rows


def run_exploratory_data_analysis(
    df: pd.DataFrame | None = None, save_outputs: bool = True
) -> Dict[str, Any]:
    """Execute Phase 2 EDA and export summary CSV tables."""
    if df is None:
        df, _ = load_and_validate_data(save_outputs=save_outputs)

    continuous_rows, continuous_dict = [], {}
    for col in CONTINUOUS_VARIABLES:
        unit, scale = PHYSICAL_UNITS[col]
        st = compute_series_stats(df[col])
        row = {
            "variable": col, "unit_description": unit, **st,
            "physical_mean": round(st["mean"] * scale, 2),
            "physical_sd": round(st["sd"] * scale, 2),
            "physical_median": round(st["median"] * scale, 2),
            "physical_iqr": round(st["iqr"] * scale, 2),
        }
        continuous_rows.append(row)
        continuous_dict[col] = row

    by_year = _compute_group_summary(df, "yr", YEAR_LABELS)
    by_season = _compute_group_summary(df, "season", SEASON_LABELS)
    by_weathersit = _compute_group_summary(df, "weathersit", WEATHERSIT_LABELS)
    by_workingday = _compute_group_summary(df, "workingday", WORKINGDAY_LABELS)
    by_holiday = _compute_group_summary(df, "holiday", {0: "0: Regular Day", 1: "1: Holiday"})

    weather_workday_rows = []
    for w in [1, 2, 3]:
        for wd in [0, 1]:
            st = compute_series_stats(df.loc[(df["weathersit"] == w) & (df["workingday"] == wd), "cnt"])
            weather_workday_rows.append({
                "weathersit": w, "workingday": wd, "n": st["n"], "mean_cnt": st["mean"],
                "sd_cnt": st["sd"], "ci95_low": st["ci95_mean_low"], "ci95_high": st["ci95_mean_high"],
                "median_cnt": st["median"], "iqr_cnt": st["iqr"],
            })

    outlier_rows = _detect_outliers_table(df)
    sensitivity_rows = _compute_outlier_handling_sensitivity(df)

    if save_outputs:
        TABLES_DIR.mkdir(parents=True, exist_ok=True)
        for name, data in [
            ("eda_continuous_summary.csv", continuous_rows),
            ("eda_group_by_year.csv", by_year),
            ("eda_group_by_season.csv", by_season),
            ("eda_group_by_weathersit.csv", by_weathersit),
            ("eda_group_by_workingday.csv", by_workingday),
            ("eda_group_by_holiday.csv", by_holiday),
            ("eda_weather_by_workingday.csv", weather_workday_rows),
            ("eda_outlier_audit.csv", outlier_rows),
            ("eda_outlier_handling_sensitivity.csv", sensitivity_rows),
        ]:
            pd.DataFrame(data).to_csv(TABLES_DIR / name, index=False)

    y0, y1 = by_year[0]["mean"], by_year[1]["mean"]
    cnt_st = continuous_dict["cnt"]
    return {
        "continuous_summary": continuous_dict,
        "group_summaries": {
            "by_year": by_year, "by_season": by_season, "by_weathersit": by_weathersit,
            "by_workingday": by_workingday, "by_holiday": by_holiday,
            "weather_by_workingday": weather_workday_rows,
        },
        "outlier_audit": outlier_rows,
        "outlier_handling_sensitivity": sensitivity_rows,
        "key_findings": {
            "year_over_year_mean_growth_pct": round(100.0 * (y1 - y0) / y0, 2),
            "mean_cnt_2011": y0, "mean_cnt_2012": y1,
            "overall_mean_cnt": cnt_st["mean"], "overall_sd_cnt": cnt_st["sd"],
            "overall_median_cnt": cnt_st["median"], "overall_iqr_cnt": cnt_st["iqr"],
            "registered_share_of_total_rides_pct": round(100.0 * float(df["registered"].sum() / df["cnt"].sum()), 2),
            "casual_share_of_total_rides_pct": round(100.0 * float(df["casual"].sum() / df["cnt"].sum()), 2),
        },
    }
