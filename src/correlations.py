"""Phase 5: Pearson linear and Spearman rank correlation matrices and pairwise tests."""

from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

from src.load_validate import TABLES_DIR, load_and_validate_data

CORRELATION_CONTINUOUS_VARS = ["cnt", "temp", "atemp", "hum", "windspeed"]
CORRELATION_VAR_LABELS = {
    "cnt": "Total Rentals (cnt)",
    "temp": "Ambient Temp (temp)",
    "atemp": "Feeling Temp (atemp)",
    "hum": "Humidity (hum)",
    "windspeed": "Wind Speed (windspeed)",
}


def _fisher_z_ci(r: float, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Compute 95% confidence interval for correlation coefficient via Fisher's z-transform."""
    z = np.arctanh(float(np.clip(r, -0.999999, 0.999999)))
    hw = float(stats.norm.ppf(1.0 - alpha / 2.0)) / np.sqrt(n - 3)
    return float(np.tanh(z - hw)), float(np.tanh(z + hw))


def _effect_magnitude_label(abs_r: float) -> str:
    """Classify correlation magnitude using standard applied guidelines."""
    if abs_r >= 0.70:
        return "Very Strong / Collinear (>= 0.70)"
    if abs_r >= 0.50:
        return "Strong (0.50 - 0.69)"
    if abs_r >= 0.30:
        return "Moderate (0.30 - 0.49)"
    if abs_r >= 0.10:
        return "Weak (0.10 - 0.29)"
    return "Negligible (< 0.10)"


def run_correlation_analysis(
    df: pd.DataFrame | None = None, save_outputs: bool = True
) -> Dict[str, Any]:
    """Execute Phase 5 Pearson and Spearman correlation analysis on continuous variables."""
    if df is None:
        df, _ = load_and_validate_data(save_outputs=save_outputs)

    sub = df[CORRELATION_CONTINUOUS_VARS].astype(float)
    n = len(sub)
    pearson_mat = sub.corr(method="pearson")
    spearman_mat = sub.corr(method="spearman")

    pair_rows: List[Dict[str, Any]] = []
    p_pear_list, p_spear_list = [], []
    for v1, v2 in combinations(CORRELATION_CONTINUOUS_VARS, 2):
        x, y = sub[v1].to_numpy(), sub[v2].to_numpy()
        r_val, p_p = stats.pearsonr(x, y)
        rho_val, p_s = stats.spearmanr(x, y)
        r_lo, r_hi = _fisher_z_ci(float(r_val), n)
        s_lo, s_hi = _fisher_z_ci(float(rho_val), n)
        p_pear_list.append(float(p_p))
        p_spear_list.append(float(p_s))

        pair_rows.append({
            "var1": v1, "var2": v2, "pair_label": f"{v1} vs {v2}", "n": int(n),
            "pearson_r": round(float(r_val), 4), "pearson_r_squared": round(float(r_val**2), 4),
            "pearson_ci95_low": round(r_lo, 4), "pearson_ci95_high": round(r_hi, 4),
            "pearson_p_unadjusted": float(p_p),
            "spearman_rho": round(float(rho_val), 4),
            "spearman_ci95_low": round(s_lo, 4), "spearman_ci95_high": round(s_hi, 4),
            "spearman_p_unadjusted": float(p_s),
            "diff_rho_minus_r": round(float(rho_val - r_val), 4),
            "magnitude_interpretation": _effect_magnitude_label(abs(float(r_val))),
        })

    _, pear_holm, _, _ = multipletests(p_pear_list, alpha=0.05, method="holm")
    _, spear_holm, _, _ = multipletests(p_spear_list, alpha=0.05, method="holm")
    for row, hp_r, hp_s in zip(pair_rows, pear_holm, spear_holm):
        row["pearson_p_holm"] = float(hp_r)
        row["spearman_p_holm"] = float(hp_s)
        row["significant_at_0_05"] = bool(hp_r < 0.05 and hp_s < 0.05)

    df_clean_hum = df[df["hum"] > 0.0]
    r_hc, p_hc = stats.pearsonr(df_clean_hum["hum"].astype(float), df_clean_hum["cnt"].astype(float))
    rho_hc, sp_hc = stats.spearmanr(df_clean_hum["hum"].astype(float), df_clean_hum["cnt"].astype(float))

    if save_outputs:
        TABLES_DIR.mkdir(parents=True, exist_ok=True)
        pearson_mat.round(4).to_csv(TABLES_DIR / "pearson_correlation_matrix.csv")
        spearman_mat.round(4).to_csv(TABLES_DIR / "spearman_correlation_matrix.csv")
        pd.DataFrame(pair_rows).to_csv(TABLES_DIR / "correlation_pairwise_tests.csv", index=False)

    pair_lookup = {f"{r['var1']}_{r['var2']}": r for r in pair_rows}
    return {
        "variables": CORRELATION_CONTINUOUS_VARS,
        "pearson_matrix": pearson_mat.round(4).to_dict(),
        "spearman_matrix": spearman_mat.round(4).to_dict(),
        "pairwise_tests": pair_rows,
        "key_pairs": pair_lookup,
        "collinearity_diagnosis": {
            "pair": "temp vs atemp",
            "pearson_r": pair_lookup["temp_atemp"]["pearson_r"],
            "spearman_rho": pair_lookup["temp_atemp"]["spearman_rho"],
        },
        "zero_humidity_sensitivity": {
            "n_clean": int(len(df_clean_hum)),
            "pearson_r_full": pair_lookup["cnt_hum"]["pearson_r"],
            "pearson_r_no_zero_hum": round(float(r_hc), 4),
            "pearson_p_no_zero_hum": float(p_hc),
            "spearman_rho_full": pair_lookup["cnt_hum"]["spearman_rho"],
            "spearman_rho_no_zero_hum": round(float(rho_hc), 4),
            "spearman_p_no_zero_hum": float(sp_hc),
        },
    }
