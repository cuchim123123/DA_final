"""Pure, testable data loading, cohort filtering, scoring, and simulation helpers for Bike Sharing Streamlit App."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import statsmodels.api as sm

# Robust project root resolution
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
TABLES_DIR = OUTPUTS_DIR / "tables"
FIGURES_DIR = OUTPUTS_DIR / "figures"
DATA_DIR = PROJECT_ROOT / "data" / "raw"
RESULTS_JSON_PATH = OUTPUTS_DIR / "results.json"

from src.load_validate import (
    EXPECTED_COLUMNS,
    SEASON_LABELS,
    SEASON_SHORT_LABELS,
    WEATHERSIT_LABELS,
    WORKINGDAY_LABELS,
    YEAR_LABELS,
    load_and_validate_data,
)
from src.regression import (
    PRIMARY_PREDICTOR_ALLOWLIST,
    build_preprocessing_transformer,
    chronological_train_test_split,
)


@dataclass
class DashboardArtifacts:
    """Container for all verified analytical outputs, models, and reference data."""

    df: pd.DataFrame
    results: Dict[str, Any]
    tables: Dict[str, pd.DataFrame]
    ols_pipe: Pipeline
    ols_statsmodels: sm.regression.linear_model.RegressionResultsWrapper
    ols_casual_pipe: Pipeline
    ols_registered_pipe: Pipeline
    train_df: pd.DataFrame
    test_df: pd.DataFrame
    feature_names: List[str]


def get_figure_path(fig_name: str) -> Optional[Path]:
    """Return verified path to generated figure or None if not found."""
    p = FIGURES_DIR / fig_name
    return p if p.exists() else None


def load_dashboard_artifacts() -> DashboardArtifacts:
    """Load dataset, results.json, tables, and fit real-time regression simulator models."""
    df, _ = load_and_validate_data(save_outputs=False)

    # Load results.json if available
    results_payload: Dict[str, Any] = {}
    if RESULTS_JSON_PATH.exists():
        with open(RESULTS_JSON_PATH, "r", encoding="utf-8") as f:
            results_payload = json.load(f)

    # Load all CSV tables in outputs/tables
    tables: Dict[str, pd.DataFrame] = {}
    if TABLES_DIR.exists():
        for csv_file in TABLES_DIR.glob("*.csv"):
            tables[csv_file.stem] = pd.read_csv(csv_file)

    # Train / test chronological split (80% train, 20% test)
    train_df, test_df = chronological_train_test_split(df, train_fraction=0.80)

    # Fit Champion OLS Total Demand Pipeline
    X_tr = train_df[PRIMARY_PREDICTOR_ALLOWLIST].copy()
    y_tr = train_df["cnt"].astype(float).to_numpy()

    transformer = build_preprocessing_transformer()
    ols_pipe = Pipeline([
        ("preprocess", transformer),
        ("model", LinearRegression()),
    ]).fit(X_tr, y_tr)

    # Fit Statsmodels OLS for prediction intervals
    pre = ols_pipe.named_steps["preprocess"]
    feature_names = list(pre.get_feature_names_out())
    X_tr_transformed = pd.DataFrame(pre.transform(X_tr), columns=feature_names)
    X_sm = sm.add_constant(X_tr_transformed, has_constant="add")
    ols_statsmodels = sm.OLS(y_tr, X_sm).fit()

    # Fit secondary pipelines for Casual and Registered demand estimation
    ols_casual_pipe = Pipeline([
        ("preprocess", build_preprocessing_transformer()),
        ("model", LinearRegression()),
    ]).fit(X_tr, train_df["casual"].astype(float).to_numpy())

    ols_registered_pipe = Pipeline([
        ("preprocess", build_preprocessing_transformer()),
        ("model", LinearRegression()),
    ]).fit(X_tr, train_df["registered"].astype(float).to_numpy())

    return DashboardArtifacts(
        df=df,
        results=results_payload,
        tables=tables,
        ols_pipe=ols_pipe,
        ols_statsmodels=ols_statsmodels,
        ols_casual_pipe=ols_casual_pipe,
        ols_registered_pipe=ols_registered_pipe,
        train_df=train_df,
        test_df=test_df,
        feature_names=feature_names,
    )


def filter_bike_cohort(
    df: pd.DataFrame,
    date_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None,
    seasons: Optional[List[int]] = None,
    weather_conditions: Optional[List[int]] = None,
    years: Optional[List[int]] = None,
    day_types: Optional[List[str]] = None,
    temp_range_celsius: Optional[Tuple[float, float]] = None,
) -> pd.DataFrame:
    """Filter the master dataset reactively based on user sidebar controls."""
    sub = df.copy()

    if date_range is not None and len(date_range) == 2:
        sub = sub[
            (sub["dteday_parsed"] >= pd.to_datetime(date_range[0]))
            & (sub["dteday_parsed"] <= pd.to_datetime(date_range[1]))
        ]

    if seasons:
        sub = sub[sub["season"].isin(seasons)]

    if weather_conditions:
        sub = sub[sub["weathersit"].isin(weather_conditions)]

    if years is not None and len(years) > 0:
        sub = sub[sub["yr"].isin(years)]

    if day_types:
        # Options: "Working Days", "Weekends & Holidays"
        masks = []
        if "Working Days" in day_types:
            masks.append(sub["workingday"] == 1)
        if "Weekends & Holidays" in day_types:
            masks.append(sub["workingday"] == 0)
        if masks:
            sub = sub[pd.concat(masks, axis=1).any(axis=1)]

    if temp_range_celsius is not None:
        sub = sub[
            (sub["temp_celsius"] >= temp_range_celsius[0])
            & (sub["temp_celsius"] <= temp_range_celsius[1])
        ]

    return sub


def compute_filtered_eda_kpis(filtered_df: pd.DataFrame) -> Dict[str, Any]:
    """Compute summary KPIs reactively for a filtered cohort."""
    n_days = len(filtered_df)
    if n_days == 0:
        return {
            "n_days": 0,
            "total_rentals": 0,
            "mean_daily_rentals": 0.0,
            "std_daily_rentals": 0.0,
            "median_daily_rentals": 0.0,
            "total_casual": 0,
            "total_registered": 0,
            "casual_share_pct": 0.0,
            "registered_share_pct": 0.0,
            "mean_temp_c": 0.0,
            "mean_hum_pct": 0.0,
            "mean_wind_kmh": 0.0,
            "peak_day_date": "N/A",
            "peak_day_cnt": 0,
        }

    total_cnt = int(filtered_df["cnt"].sum())
    total_casual = int(filtered_df["casual"].sum())
    total_registered = int(filtered_df["registered"].sum())
    peak_row = filtered_df.loc[filtered_df["cnt"].idxmax()]

    return {
        "n_days": n_days,
        "total_rentals": total_cnt,
        "mean_daily_rentals": round(float(filtered_df["cnt"].mean()), 1),
        "std_daily_rentals": round(float(filtered_df["cnt"].std(ddof=1)), 1) if n_days > 1 else 0.0,
        "median_daily_rentals": round(float(filtered_df["cnt"].median()), 1),
        "total_casual": total_casual,
        "total_registered": total_registered,
        "casual_share_pct": round(100.0 * total_casual / total_cnt, 2) if total_cnt > 0 else 0.0,
        "registered_share_pct": round(100.0 * total_registered / total_cnt, 2) if total_cnt > 0 else 0.0,
        "mean_temp_c": round(float(filtered_df["temp_celsius"].mean()), 1),
        "mean_hum_pct": round(float(filtered_df["hum_pct"].mean()), 1),
        "mean_wind_kmh": round(float(filtered_df["windspeed_kmh"].mean()), 1),
        "peak_day_date": str(peak_row["dteday"]),
        "peak_day_cnt": int(peak_row["cnt"]),
    }


def predict_bike_demand(
    art: DashboardArtifacts,
    yr: int,
    season: int,
    holiday: int,
    workingday: int,
    weathersit: int,
    temp_c: float,
    hum_pct: float,
    windspeed_kmh: float,
) -> Dict[str, Any]:
    """Execute real-time OLS prediction with 95% confidence and prediction intervals."""
    # Convert physical units to normalized predictors
    temp_norm = float(np.clip(temp_c / 41.0, 0.0, 1.0))
    hum_norm = float(np.clip(hum_pct / 100.0, 0.0, 1.0))
    windspeed_norm = float(np.clip(windspeed_kmh / 67.0, 0.0, 1.0))

    input_dict = {
        "temp": temp_norm,
        "hum": hum_norm,
        "windspeed": windspeed_norm,
        "yr": int(yr),
        "holiday": int(holiday),
        "workingday": int(workingday),
        "season": int(season),
        "weathersit": int(weathersit),
    }
    input_df = pd.DataFrame([input_dict])

    # Point predictions via Scikit-Learn pipelines
    pred_cnt_raw = float(art.ols_pipe.predict(input_df)[0])
    pred_casual_raw = float(art.ols_casual_pipe.predict(input_df)[0])
    pred_registered_raw = float(art.ols_registered_pipe.predict(input_df)[0])

    # Physical clipping (demand cannot be negative)
    pred_cnt = max(0.0, pred_cnt_raw)
    pred_casual = max(0.0, pred_casual_raw)
    pred_registered = max(0.0, pred_registered_raw)

    # Statistical prediction intervals via Statsmodels
    pre = art.ols_pipe.named_steps["preprocess"]
    x_transformed = pd.DataFrame(pre.transform(input_df), columns=art.feature_names)
    x_sm = sm.add_constant(x_transformed, has_constant="add")
    pred_frame = art.ols_statsmodels.get_prediction(x_sm).summary_frame(alpha=0.05).iloc[0]

    mean_ci_lower = max(0.0, float(pred_frame["mean_ci_lower"]))
    mean_ci_upper = max(0.0, float(pred_frame["mean_ci_upper"]))
    obs_ci_lower = max(0.0, float(pred_frame["obs_ci_lower"]))
    obs_ci_upper = max(0.0, float(pred_frame["obs_ci_upper"]))

    # Fleet sizing advisory
    fleet_rebalance = "Standard Fleet Operations"
    if pred_cnt > 6500:
        fleet_rebalance = "High Demand Alert: Maximize fleet dispatch, stage extra vans at transit hubs."
    elif pred_cnt < 2500:
        fleet_rebalance = "Low Demand Notice: Opportunity window for bike maintenance and station rebalancing."

    return {
        "predicted_cnt": round(pred_cnt, 0),
        "predicted_casual": round(pred_casual, 0),
        "predicted_registered": round(pred_registered, 0),
        "mean_se": round(float(pred_frame["mean_se"]), 1),
        "mean_ci_95": (round(mean_ci_lower, 0), round(mean_ci_upper, 0)),
        "prediction_interval_95": (round(obs_ci_lower, 0), round(obs_ci_upper, 0)),
        "normalized_inputs": {
            "temp_norm": round(temp_norm, 4),
            "hum_norm": round(hum_norm, 4),
            "windspeed_norm": round(windspeed_norm, 4),
        },
        "fleet_advisory": fleet_rebalance,
    }
