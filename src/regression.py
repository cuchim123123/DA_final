"""Phase 6: Multiple Linear Regression (OLS), anti-leakage pipeline, VIF, and robust diagnostics."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox, het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson, jarque_bera

from src.load_validate import OUTPUTS_DIR, TABLES_DIR, load_and_validate_data

MODEL_DIR = OUTPUTS_DIR / "model"

FORBIDDEN_LEAKAGE_FEATURES = {
    "cnt", "casual", "registered", "instant", "dteday", "dteday_parsed",
    "high_demand", "season_label", "weathersit_label", "workingday_label",
    "year_label", "temp_celsius", "atemp_celsius", "hum_pct", "windspeed_kmh",
}
PRIMARY_CONTINUOUS_FEATURES = ["temp", "hum", "windspeed"]
PRIMARY_BINARY_FEATURES = ["yr", "holiday", "workingday"]
PRIMARY_CATEGORICAL_FEATURES = ["season", "weathersit"]
PRIMARY_PREDICTOR_ALLOWLIST = (
    PRIMARY_CONTINUOUS_FEATURES + PRIMARY_BINARY_FEATURES + PRIMARY_CATEGORICAL_FEATURES
)

FEATURE_READABLE_NAMES = {
    "const": "Intercept (Ref: 2011, Season 1, Clear Weather, Non-Workday)",
    "num__temp": "Normalized Temperature (temp)",
    "num__hum": "Normalized Humidity (hum)",
    "num__windspeed": "Normalized Wind Speed (windspeed)",
    "bin__yr": "Year Indicator (yr: 1 = 2012)",
    "bin__holiday": "Public Holiday Indicator (holiday: 1 = Yes)",
    "bin__workingday": "Working Day Indicator (workingday: 1 = Workday)",
    "cat__season_2": "Season 2: Summer (vs Season 1)",
    "cat__season_3": "Season 3: Fall (vs Season 1)",
    "cat__season_4": "Season 4: Winter (vs Season 1)",
    "cat__weathersit_2": "Weather 2: Mist/Cloudy (vs Clear 1)",
    "cat__weathersit_3": "Weather 3: Light Snow/Rain (vs Clear 1)",
}


def validate_feature_allowlist(feature_cols: List[str]) -> None:
    """Assert that no target-leakage, index, or forbidden columns enter X."""
    leaked = set(feature_cols).intersection(FORBIDDEN_LEAKAGE_FEATURES)
    if leaked:
        raise ValueError(f"CRITICAL LEAKAGE DETECTED in predictor list: {sorted(leaked)}")
    unknown = set(feature_cols) - set(PRIMARY_PREDICTOR_ALLOWLIST) - {"atemp"}
    if unknown:
        raise ValueError(f"Unregistered predictors in feature list: {sorted(unknown)}")


def chronological_train_test_split(
    df: pd.DataFrame, train_fraction: float = 0.80
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Sort strictly by `dteday_parsed` ascending and split 80% train / 20% test without shuffling."""
    df_s = df.sort_values("dteday_parsed", kind="mergesort").reset_index(drop=True)
    n_train = int(np.floor(len(df_s) * train_fraction))
    train_df, test_df = df_s.iloc[:n_train].copy(), df_s.iloc[n_train:].copy()
    if train_df["dteday_parsed"].max() >= test_df["dteday_parsed"].min():
        raise ValueError("Chronological split violated.")
    return train_df, test_df


def build_preprocessing_transformer(cont_cols: List[str] | None = None) -> ColumnTransformer:
    """Build train-only ColumnTransformer with reference-category one-hot encoding (`drop='first'`)."""
    c_cols = cont_cols if cont_cols is not None else PRIMARY_CONTINUOUS_FEATURES
    return ColumnTransformer(
        transformers=[
            ("num", "passthrough", c_cols),
            ("bin", "passthrough", PRIMARY_BINARY_FEATURES),
            ("cat", OneHotEncoder(categories=[[1, 2, 3, 4], [1, 2, 3]], drop="first", sparse_output=False, handle_unknown="ignore"), PRIMARY_CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )


def _compute_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray, p: int) -> Dict[str, float]:
    """Compute MAE, RMSE, R^2, Adjusted R^2, MAPE, and mean prediction bias."""
    n = len(y_true)
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = float(r2_score(y_true, y_pred))
    adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - p - 1)) if (p > 0 and n > p + 1) else r2
    return {
        "n": int(n), "n_predictors": int(p),
        "mae": round(mae, 4), "rmse": round(rmse, 4),
        "r2": round(r2, 4), "adj_r2": round(adj_r2, 4),
        "mape_pct": round(float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100.0), 4),
        "mean_prediction_bias_pred_minus_true": round(float(np.mean(y_pred - y_true)), 4),
    }


def _compute_vif_table(X_design: pd.DataFrame) -> List[Dict[str, Any]]:
    """Compute Variance Inflation Factor (VIF) for every non-intercept predictor."""
    Xc = sm.add_constant(X_design, has_constant="add")
    vals = Xc.to_numpy(dtype=float)
    return [
        {
            "feature": col, "readable_name": FEATURE_READABLE_NAMES.get(col, col),
            "vif": round(v := float(variance_inflation_factor(vals, i)), 4),
            "tolerance_1_over_vif": round(1.0 / v, 4) if v > 0 else np.nan,
        }
        for i, col in enumerate(Xc.columns) if col != "const"
    ]


def run_regression_analysis(
    df: pd.DataFrame | None = None, save_outputs: bool = True
) -> Dict[str, Any]:
    """Execute Phase 6 Multiple Linear Regression workflow and export tables and predictions."""
    if df is None:
        df, _ = load_and_validate_data(save_outputs=save_outputs)

    validate_feature_allowlist(PRIMARY_PREDICTOR_ALLOWLIST)
    train_df, test_df = chronological_train_test_split(df, train_fraction=0.80)
    X_tr, y_tr = train_df[PRIMARY_PREDICTOR_ALLOWLIST].copy(), train_df["cnt"].astype(float).to_numpy()
    X_te, y_te = test_df[PRIMARY_PREDICTOR_ALLOWLIST].copy(), test_df["cnt"].astype(float).to_numpy()

    base_pipe = Pipeline([("preprocess", build_preprocessing_transformer()), ("model", DummyRegressor(strategy="mean"))]).fit(X_tr, y_tr)
    ols_pipe = Pipeline([("preprocess", build_preprocessing_transformer()), ("model", LinearRegression())]).fit(X_tr, y_tr)

    col_cols = PRIMARY_PREDICTOR_ALLOWLIST + ["atemp"]
    validate_feature_allowlist(col_cols)
    col_pre = build_preprocessing_transformer(PRIMARY_CONTINUOUS_FEATURES + ["atemp"])
    col_pipe = Pipeline([("preprocess", col_pre), ("model", LinearRegression())]).fit(train_df[col_cols], y_tr)

    ridge_pipe = Pipeline([
        ("preprocess", build_preprocessing_transformer()), ("scaler", StandardScaler()),
        ("model", RidgeCV(alphas=np.logspace(-2, 3, 50), cv=TimeSeriesSplit(n_splits=5))),
    ]).fit(X_tr, y_tr)

    y_tr_base, y_te_base = base_pipe.predict(X_tr), base_pipe.predict(X_te)
    y_tr_ols, y_te_ols = ols_pipe.predict(X_tr), ols_pipe.predict(X_te)
    y_tr_col, y_te_col = col_pipe.predict(train_df[col_cols]), col_pipe.predict(test_df[col_cols])
    y_tr_rdg, y_te_rdg = ridge_pipe.predict(X_tr), ridge_pipe.predict(X_te)

    pre: ColumnTransformer = ols_pipe.named_steps["preprocess"]
    feat_names = list(pre.get_feature_names_out())
    p_feat = len(feat_names)

    m_base_tr, m_base_te = _compute_regression_metrics(y_tr, y_tr_base, 0), _compute_regression_metrics(y_te, y_te_base, 0)
    m_ols_tr, m_ols_te = _compute_regression_metrics(y_tr, y_tr_ols, p_feat), _compute_regression_metrics(y_te, y_te_ols, p_feat)
    m_col_tr, m_col_te = _compute_regression_metrics(y_tr, y_tr_col, p_feat + 1), _compute_regression_metrics(y_te, y_te_col, p_feat + 1)
    m_rdg_tr, m_rdg_te = _compute_regression_metrics(y_tr, y_tr_rdg, p_feat), _compute_regression_metrics(y_te, y_te_rdg, p_feat)

    X_tr_df = pd.DataFrame(pre.transform(X_tr), columns=feat_names)
    X_col_df = pd.DataFrame(col_pre.transform(train_df[col_cols]), columns=list(col_pre.get_feature_names_out()))
    vif_prim = _compute_vif_table(X_tr_df)
    vif_col_map = {r["feature"]: r["vif"] for r in _compute_vif_table(X_col_df)}
    for r in vif_prim:
        r["vif_when_atemp_included"] = vif_col_map.get(r["feature"], np.nan)
    vif_rows = vif_prim + [{
        "feature": "num__atemp", "readable_name": "Normalized Feeling Temp (atemp, dropped)",
        "vif": np.nan, "tolerance_1_over_vif": np.nan, "vif_when_atemp_included": vif_col_map.get("num__atemp", np.nan),
    }]

    X_sm = sm.add_constant(X_tr_df, has_constant="add")
    sm_iid = sm.OLS(y_tr, X_sm).fit()
    sm_hc3 = sm.OLS(y_tr, X_sm).fit(cov_type="HC3")
    sm_hac = sm.OLS(y_tr, X_sm).fit(cov_type="HAC", cov_kwds={"maxlags": 7})

    y_tr_sd = float(np.std(y_tr, ddof=1))
    coef_rows = []
    for i, col in enumerate(X_sm.columns):
        b = float(sm_iid.params.iloc[i])
        std_b = np.nan if col == "const" else round(b * float(np.std(X_sm[col].to_numpy(), ddof=1)) / y_tr_sd, 4)
        ci_i, ci_h, ci_n = sm_iid.conf_int().iloc[i], sm_hc3.conf_int().iloc[i], sm_hac.conf_int().iloc[i]
        coef_rows.append({
            "term": col, "readable_name": FEATURE_READABLE_NAMES.get(col, col),
            "coef_estimate": round(b, 4), "standardized_beta": std_b,
            "se_iid": round(float(sm_iid.bse.iloc[i]), 4), "t_iid": round(float(sm_iid.tvalues.iloc[i]), 4),
            "p_iid": float(sm_iid.pvalues.iloc[i]), "ci95_iid_low": round(float(ci_i[0]), 4), "ci95_iid_high": round(float(ci_i[1]), 4),
            "se_hc3": round(float(sm_hc3.bse.iloc[i]), 4), "t_hc3": round(float(sm_hc3.tvalues.iloc[i]), 4),
            "p_hc3": float(sm_hc3.pvalues.iloc[i]), "ci95_hc3_low": round(float(ci_h[0]), 4), "ci95_hc3_high": round(float(ci_h[1]), 4),
            "se_hac_lag7": round(float(sm_hac.bse.iloc[i]), 4), "t_hac_lag7": round(float(sm_hac.tvalues.iloc[i]), 4),
            "p_hac_lag7": float(sm_hac.pvalues.iloc[i]), "ci95_hac_low": round(float(ci_n[0]), 4), "ci95_hac_high": round(float(ci_n[1]), 4),
        })

    tr_res, te_res = y_tr - y_tr_ols, y_te - y_te_ols
    lb_df = acorr_ljungbox(tr_res, lags=[1, 7], return_df=True)
    bp_lm, bp_lm_p, bp_f, bp_f_p = het_breuschpagan(tr_res, X_sm.to_numpy())
    jb_s, jb_p, _, jb_k = jarque_bera(tr_res)
    sw_w, sw_p = stats.shapiro(tr_res)
    cooks_d = sm_iid.get_influence().cooks_distance[0]
    c_thr = 4.0 / len(y_tr)
    w_idx = int(np.argmax(np.abs(te_res)))

    resid_diag = {
        "train_n": int(len(y_tr)), "test_n": int(len(y_te)),
        "ols_f_statistic_iid": round(float(sm_iid.fvalue), 4), "ols_f_pvalue_iid": float(sm_iid.f_pvalue),
        "ols_aic": round(float(sm_iid.aic), 2), "ols_bic": round(float(sm_iid.bic), 2),
        "durbin_watson": round(float(durbin_watson(tr_res)), 4),
        "ljung_box_lag1_q": round(float(lb_df.loc[1, "lb_stat"]), 4), "ljung_box_lag1_p": float(lb_df.loc[1, "lb_pvalue"]),
        "ljung_box_lag7_q": round(float(lb_df.loc[7, "lb_stat"]), 4), "ljung_box_lag7_p": float(lb_df.loc[7, "lb_pvalue"]),
        "breusch_pagan_lm": round(float(bp_lm), 4), "breusch_pagan_lm_p": float(bp_lm_p),
        "breusch_pagan_f": round(float(bp_f), 4), "breusch_pagan_f_p": float(bp_f_p),
        "jarque_bera_stat": round(float(jb_s), 4), "jarque_bera_p": float(jb_p),
        "shapiro_wilk_w": round(float(sw_w), 4), "shapiro_wilk_p": float(sw_p),
        "residual_skewness": round(float(stats.skew(tr_res, bias=False)), 4),
        "residual_excess_kurtosis": round(float(stats.kurtosis(tr_res, fisher=True, bias=False)), 4),
        "residual_kurtosis": round(float(jb_k), 4),
        "cooks_d_threshold_4_over_n": round(c_thr, 6),
        "cooks_d_exceeding_4_over_n_count": int(np.sum(cooks_d > c_thr)),
        "cooks_d_max": round(float(np.max(cooks_d)), 6),
        "cooks_d_max_date": str(train_df.iloc[int(np.argmax(cooks_d))]["dteday"]),
        "worst_test_error_day": {
            "dteday": str(test_df.iloc[w_idx]["dteday"]), "actual_cnt": int(test_df.iloc[w_idx]["cnt"]),
            "predicted_cnt": round(float(y_te_ols[w_idx]), 2),
            "residual_actual_minus_pred": round(float(te_res[w_idx]), 2),
        },
    }

    def _comp_row(name: str, role: str, p: int, mtr: Dict[str, float], mte: Dict[str, float]) -> Dict[str, Any]:
        return {
            "model_name": name, "role": role, "n_predictors": p,
            "train_mae": mtr["mae"], "train_rmse": mtr["rmse"], "train_r2": mtr["r2"], "train_adj_r2": mtr["adj_r2"],
            "test_mae": mte["mae"], "test_rmse": mte["rmse"], "test_r2": mte["r2"],
            "test_bias_pred_minus_true": mte["mean_prediction_bias_pred_minus_true"],
        }

    comp_rows = [
        _comp_row("Mean Baseline (DummyRegressor)", f"Predicts Train Mean = { float(np.mean(y_tr)):,.2f}", 0, m_base_tr, m_base_te),
        _comp_row("Primary Multiple Linear Regression (OLS)", "Primary Specification (Drops Collinear atemp)", p_feat, m_ols_tr, m_ols_te),
        _comp_row("Supplemental Collinear OLS (With atemp)", "Demonstrates VIF Collinearity", p_feat + 1, m_col_tr, m_col_te),
        _comp_row(f"Supplemental Ridge (alpha={float(ridge_pipe.named_steps['model'].alpha_):.2f})", "L2 Regularized Comparison", p_feat, m_rdg_tr, m_rdg_te),
    ]

    if save_outputs:
        TABLES_DIR.mkdir(parents=True, exist_ok=True)
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(comp_rows).to_csv(TABLES_DIR / "regression_model_comparison.csv", index=False)
        pd.DataFrame(coef_rows).to_csv(TABLES_DIR / "regression_ols_coefficients.csv", index=False)
        pd.DataFrame(vif_rows).to_csv(TABLES_DIR / "regression_vif_diagnostics.csv", index=False)
        pd.DataFrame([resid_diag]).to_csv(TABLES_DIR / "regression_residual_diagnostics.csv", index=False)

        pd.DataFrame({
            "instant": train_df["instant"].to_numpy(), "dteday": train_df["dteday"].to_numpy(),
            "y_true": y_tr, "y_pred_baseline": np.round(y_tr_base, 6),
            "y_pred_ols": np.round(y_tr_ols, 6), "residual_ols": np.round(tr_res, 6),
            "cooks_distance": np.round(cooks_d, 6),
        }).to_csv(MODEL_DIR / "train_predictions.csv", index=False)
        pd.DataFrame({
            "instant": test_df["instant"].to_numpy(), "dteday": test_df["dteday"].to_numpy(),
            "y_true": y_te, "y_pred_baseline": np.round(y_te_base, 6),
            "y_pred_ols": np.round(y_te_ols, 6), "y_pred_ridge": np.round(y_te_rdg, 6),
            "residual_ols": np.round(te_res, 6),
        }).to_csv(MODEL_DIR / "test_predictions.csv", index=False)

    return {
        "split_info": {
            "train_n": int(len(train_df)), "train_start_date": str(train_df["dteday"].iloc[0]),
            "train_end_date": str(train_df["dteday"].iloc[-1]),
            "test_n": int(len(test_df)), "test_start_date": str(test_df["dteday"].iloc[0]),
            "test_end_date": str(test_df["dteday"].iloc[-1]),
            "chronological_order_verified": bool(train_df["dteday_parsed"].max() < test_df["dteday_parsed"].min()),
        },
        "allowlist_info": {
            "primary_predictors": PRIMARY_PREDICTOR_ALLOWLIST,
            "encoded_design_features": feat_names,
            "forbidden_features_excluded": sorted(FORBIDDEN_LEAKAGE_FEATURES),
        },
        "metrics": {
            "baseline_train": m_base_tr, "baseline_test": m_base_te,
            "ols_train": m_ols_tr, "ols_test": m_ols_te,
            "collinear_ols_train": m_col_tr, "collinear_ols_test": m_col_te,
            "ridge_train": m_rdg_tr, "ridge_test": m_rdg_te,
            "ols_vs_baseline_test_rmse_reduction_pct": round(100.0 * (m_base_te["rmse"] - m_ols_te["rmse"]) / m_base_te["rmse"], 2),
            "ols_vs_baseline_test_mae_reduction_pct": round(100.0 * (m_base_te["mae"] - m_ols_te["mae"]) / m_base_te["mae"], 2),
        },
        "model_comparison_table": comp_rows,
        "ols_coefficients": coef_rows,
        "vif_diagnostics": vif_rows,
        "residual_diagnostics": resid_diag,
    }
