"""Phases 5 & 6 Correlation and Multiple Linear Regression Plots (Figures 12–18)."""

from __future__ import annotations

from typing import Any, Dict

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
from statsmodels.nonparametric.smoothers_lowess import lowess

from src.correlations import CORRELATION_CONTINUOUS_VARS, CORRELATION_VAR_LABELS
from src.load_validate import OUTPUTS_DIR
from src.plots.style import PALETTE_MAIN, add_stat_box, plot_qq_panel, save_fig


def _plot_corr_heatmap(df: pd.DataFrame, method: str, fig_num: int, filename: str) -> str:
    """Render annotated Pearson or Spearman correlation heatmap with p-values."""
    sub = df[CORRELATION_CONTINUOUS_VARS].astype(float)
    corr_mat = sub.corr(method=method)
    cols, n_v = CORRELATION_CONTINUOUS_VARS, len(CORRELATION_CONTINUOUS_VARS)
    fn = stats.pearsonr if method == "pearson" else stats.spearmanr
    annot = np.empty((n_v, n_v), dtype=object)
    for i in range(n_v):
        for j in range(n_v):
            v = corr_mat.iloc[i, j]
            if i == j:
                annot[i, j] = f"{v:.2f}\n(diag)"
            else:
                _, p = fn(sub[cols[i]], sub[cols[j]])
                annot[i, j] = f"{v:+.4f}\n({'p<0.001' if p < 0.001 else f'p={p:.3f}'})"

    fig, ax = plt.subplots(figsize=(8.8, 7.0))
    lbls = [CORRELATION_VAR_LABELS[c] for c in cols]
    sns.heatmap(
        corr_mat, annot=annot, fmt="", cmap="RdBu_r", vmin=-1.0, vmax=1.0, center=0.0,
        square=True, linewidths=1.2, linecolor="white",
        cbar_kws={"label": f"{method.capitalize()} Correlation", "shrink": 0.82},
        xticklabels=lbls, yticklabels=lbls, annot_kws={"size": 8.8, "weight": "bold"}, ax=ax,
    )
    sym = "r (Linear)" if method == "pearson" else "ρ (Rank-Monotonic)"
    ax.set_title(f"Figure {fig_num}: {method.capitalize()} Correlation Matrix ({sym}) Across Continuous Variables (N = {len(sub)})", pad=14)
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    plt.setp(ax.get_yticklabels(), rotation=0)
    return save_fig(fig, filename)


def plot_fig12_pearson_heatmap(df: pd.DataFrame) -> str:
    """Fig 12: Annotated Pearson linear correlation matrix heatmap."""
    return _plot_corr_heatmap(df, "pearson", 12, "fig12_pearson_correlation_heatmap.png")


def plot_fig13_spearman_heatmap(df: pd.DataFrame) -> str:
    """Fig 13: Annotated Spearman rank correlation matrix heatmap."""
    return _plot_corr_heatmap(df, "spearman", 13, "fig13_spearman_correlation_heatmap.png")


def plot_fig14_scatter_grid(df: pd.DataFrame, corr_res: Dict[str, Any]) -> str:
    """Fig 14: 2x2 bivariate scatter grid for key continuous relationships and collinearity."""
    fig, axes = plt.subplots(2, 2, figsize=(12.4, 9.2))
    pairs = [
        ("temp", "cnt", "Normalized Temperature (temp)", "Daily Rentals (cnt)", "cnt_temp"),
        ("hum", "cnt", "Normalized Humidity (hum)", "Daily Rentals (cnt)", "cnt_hum"),
        ("windspeed", "cnt", "Normalized Wind Speed (windspeed)", "Daily Rentals (cnt)", "cnt_windspeed"),
        ("temp", "atemp", "Normalized Ambient Temp (temp)", "Normalized Feeling Temp (atemp)", "temp_atemp"),
    ]
    for i, (xc, yc, xl, yl, key) in enumerate(pairs):
        ax = axes[i // 2, i % 2]
        x, y, pi = df[xc].astype(float).to_numpy(), df[yc].astype(float).to_numpy(), corr_res["key_pairs"][key]
        ax.scatter(x, y, color=PALETTE_MAIN["blue"] if yc == "cnt" else PALETTE_MAIN["purple"], alpha=0.45, s=22, edgecolors="white", lw=0.3)
        sl, ic, _, _, _ = stats.linregress(x, y)
        xg = np.linspace(x.min(), x.max(), 150)
        ax.plot(xg, ic + sl * xg, color=PALETTE_MAIN["navy"], ls="--", lw=2.0, label="OLS Line")
        lw = lowess(y, x, frac=0.35)
        ax.plot(lw[:, 0], lw[:, 1], color=PALETTE_MAIN["red"], lw=2.0, label="LOWESS")
        if key == "temp_atemp":
            ai = int((df["temp"] - df["atemp"]).abs().idxmax())
            ax.annotate(f"{df.loc[ai, 'dteday']} Anomaly\n(temp={df.loc[ai,'temp']:.2f}, atemp={df.loc[ai,'atemp']:.2f})", xy=(float(df.loc[ai, "temp"]), float(df.loc[ai, "atemp"])), xytext=(0.35, 0.20), arrowprops=dict(arrowstyle="->", color=PALETTE_MAIN["red"], lw=1.2), fontsize=8.0, fontweight="bold", color=PALETTE_MAIN["red"], bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=PALETTE_MAIN["red"]))
        add_stat_box(ax, f"Pearson r = {pi['pearson_r']:+.4f} (p = {pi['pearson_p_unadjusted']:.2e})\nSpearman ρ = {pi['spearman_rho']:+.4f} (p = {pi['spearman_p_unadjusted']:.2e})\n95% CI (r): [{pi['pearson_ci95_low']:+.3f}, {pi['pearson_ci95_high']:+.3f}]")
        ax.set(title=f"({chr(65+i)}) {xc} vs. {yc} ({pi['magnitude_interpretation']})", xlabel=xl, ylabel=yl)
        ax.legend(loc="lower right", frameon=True, fontsize=8)
    fig.suptitle("Figure 14: Pairwise Scatter Plots, Linear/LOWESS Trends, and Collinearity Diagnosis", y=1.01)
    fig.tight_layout()
    return save_fig(fig, "fig14_continuous_predictors_scatter_grid.png")


def plot_fig15_actual_vs_predicted(reg_res: Dict[str, Any]) -> str:
    """Fig 15: Actual vs Predicted parity plot for Train and Hold-Out Test sets."""
    tr_df = pd.read_csv(OUTPUTS_DIR / "model" / "train_predictions.csv")
    te_df = pd.read_csv(OUTPUTS_DIR / "model" / "test_predictions.csv")
    m, sp = reg_res["metrics"], reg_res["split_info"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 5.4))
    lims = [0, 9200]

    ax1.scatter(tr_df["y_true"], tr_df["y_pred_ols"], color=PALETTE_MAIN["blue"], alpha=0.50, s=24, label=f"OLS Training Fit (n={sp['train_n']})")
    ax1.plot(lims, lims, color=PALETTE_MAIN["red"], ls="--", lw=2.0, label="45° Perfect Parity")
    add_stat_box(ax1, f"Training Set ({sp['train_start_date']} to {sp['train_end_date']}):\nR² = {m['ols_train']['r2']:.4f}, Adj R² = {m['ols_train']['adj_r2']:.4f}\nRMSE = {m['ols_train']['rmse']:.2f} bikes/day\nMAE = {m['ols_train']['mae']:.2f} bikes/day", ec=PALETTE_MAIN["navy"])
    ax1.set(xlim=lims, ylim=lims, title=f"(A) In-Sample Training Set Parity (n = {sp['train_n']})", xlabel="Actual Daily Bike Rentals (y)", ylabel="OLS Predicted Rentals (ŷ)")
    ax1.legend(loc="lower right", frameon=True)

    ax2.scatter(te_df["y_true"], te_df["y_pred_ols"], color=PALETTE_MAIN["teal"], alpha=0.70, s=30, label="Primary OLS Hold-Out Predictions")
    ax2.scatter(te_df["y_true"], te_df["y_pred_baseline"], color=PALETTE_MAIN["amber"], alpha=0.55, s=20, marker="x", label=f"Mean Baseline (ŷ = {te_df['y_pred_baseline'].iloc[0]:,.1f})")
    ax2.plot(lims, lims, color=PALETTE_MAIN["red"], ls="--", lw=2.0, label="45° Perfect Parity")
    add_stat_box(ax2, f"Hold-Out Test ({sp['test_start_date']} to {sp['test_end_date']}, n={sp['test_n']}):\nOLS R² = {m['ols_test']['r2']:.4f} vs Baseline R² = {m['baseline_test']['r2']:.4f}\nOLS RMSE = {m['ols_test']['rmse']:,.2f} (-{m['ols_vs_baseline_test_rmse_reduction_pct']:.1f}% vs Baseline)\nOLS MAE = {m['ols_test']['mae']:,.2f} (-{m['ols_vs_baseline_test_mae_reduction_pct']:.1f}% vs Baseline)", ec=PALETTE_MAIN["teal"])
    ax2.set(xlim=lims, ylim=lims, title=f"(B) Out-of-Sample Hold-Out Test Set Parity (n = {sp['test_n']})", xlabel="Actual Daily Bike Rentals (y)", ylabel="Predicted Daily Bike Rentals (ŷ)")
    ax2.legend(loc="lower right", frameon=True)
    fig.suptitle("Figure 15: Multiple Linear Regression (OLS) — Actual vs. Predicted Daily Bike Rentals", y=1.02)
    fig.tight_layout()
    return save_fig(fig, "fig15_regression_actual_vs_predicted.png")


def plot_fig16_residuals_vs_fitted(reg_res: Dict[str, Any]) -> str:
    """Fig 16: Residuals vs Fitted values for Training and Test sets."""
    tr_df = pd.read_csv(OUTPUTS_DIR / "model" / "train_predictions.csv")
    te_df = pd.read_csv(OUTPUTS_DIR / "model" / "test_predictions.csv")
    rd = reg_res["residual_diagnostics"]
    fig, ax = plt.subplots(figsize=(10.5, 5.3))
    ax.scatter(tr_df["y_pred_ols"], tr_df["residual_ols"], color=PALETTE_MAIN["blue"], alpha=0.52, s=26, label=f"Training Residuals (n={len(tr_df)})")
    ax.scatter(te_df["y_pred_ols"], te_df["residual_ols"], color=PALETTE_MAIN["orange"], alpha=0.72, s=32, marker="^", label=f"Hold-Out Test Residuals (n={len(te_df)})")
    sd = float(tr_df["residual_ols"].std(ddof=1))
    ax.axhline(0.0, color="black", lw=1.5, label="Zero Error Line")
    ax.axhline(2 * sd, color=PALETTE_MAIN["gray"], ls=":", lw=1.4, label=f"±2 SD Band (±{2*sd:,.0f})")
    ax.axhline(-2 * sd, color=PALETTE_MAIN["gray"], ls=":", lw=1.4)
    lw = lowess(tr_df["residual_ols"].to_numpy(), tr_df["y_pred_ols"].to_numpy(), frac=0.35)
    ax.plot(lw[:, 0], lw[:, 1], color=PALETTE_MAIN["red"], lw=2.2, label="Training Residual LOWESS")

    w = rd["worst_test_error_day"]
    ax.annotate(f"Worst Test Error ({w['dteday']})\nActual={w['actual_cnt']}, ŷ={w['predicted_cnt']:,.0f}", xy=(w["predicted_cnt"], w["residual_actual_minus_pred"]), xytext=(w["predicted_cnt"] - 2200, w["residual_actual_minus_pred"] + 450), arrowprops=dict(arrowstyle="->", color=PALETTE_MAIN["red"], lw=1.2), fontsize=8.2, fontweight="bold", color=PALETTE_MAIN["red"], bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=PALETTE_MAIN["red"]))
    add_stat_box(ax, f"Breusch-Pagan Heteroscedasticity Test:\nLM = {rd['breusch_pagan_lm']:.2f} (p = {rd['breusch_pagan_lm_p']:.2e}), F = {rd['breusch_pagan_f']:.2f} (p = {rd['breusch_pagan_f_p']:.2e})\nDurbin-Watson = {rd['durbin_watson']:.4f}\n→ Justifies White HC3 & Newey-West HAC Standard Errors", x=0.03, y=0.96, ec=PALETTE_MAIN["navy"])
    ax.set(ylim=(-4300, 3700), title="Figure 16: OLS Residuals vs. Fitted Values — Linearity and Heteroscedasticity Audit", xlabel="OLS Fitted / Predicted Daily Rentals (ŷ)", ylabel="Residual Error (e = y − ŷ)")
    ax.legend(loc="lower left", frameon=True)
    return save_fig(fig, "fig16_regression_residuals_vs_fitted.png")


def plot_fig17_residual_qq_hist(reg_res: Dict[str, Any]) -> str:
    """Fig 17: 2-panel OLS Training Residual Histogram/KDE + Normal Q-Q Plot."""
    tr_df = pd.read_csv(OUTPUTS_DIR / "model" / "train_predictions.csv")
    resids, rd = tr_df["residual_ols"].astype(float).to_numpy(), reg_res["residual_diagnostics"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 5.0))
    sns.histplot(resids, bins=28, stat="density", color=PALETTE_MAIN["blue"], alpha=0.38, edgecolor="white", ax=ax1, label="Residual Histogram")
    sns.kdeplot(resids, color=PALETTE_MAIN["navy"], lw=2.2, ax=ax1, label="Residual KDE")
    rg = np.linspace(resids.min(), resids.max(), 300)
    ax1.plot(rg, stats.norm.pdf(rg, 0.0, np.std(resids, ddof=1)), color=PALETTE_MAIN["red"], ls="--", lw=2.0, label=f"Normal(0, σ={np.std(resids, ddof=1):.1f})")
    ax1.set(title=f"(A) OLS Training Residual Distribution (n = {len(resids)})", xlabel="Residual Error (e = y − ŷ)", ylabel="Density")
    ax1.legend(loc="upper left", frameon=True)

    std_r = (resids - np.mean(resids)) / np.std(resids, ddof=1)
    box_txt = (
        f"Residual Normality & Influence:\nSkewness = {rd['residual_skewness']:.4f}\n"
        f"Excess Kurtosis = {rd['residual_excess_kurtosis']:+.4f} (Pearson = {rd['residual_kurtosis']:.4f})\n"
        f"Shapiro-Wilk W = {rd['shapiro_wilk_w']:.4f} (p = {rd['shapiro_wilk_p']:.2e})\n"
        f"Jarque-Bera = {rd['jarque_bera_stat']:.2f} (p = {rd['jarque_bera_p']:.2e})\n"
        f"Cook's D > 4/n ({rd['cooks_d_threshold_4_over_n']:.4f}): {rd['cooks_d_exceeding_4_over_n_count']} days"
    )
    plot_qq_panel(ax2, std_r, PALETTE_MAIN["blue"], "(B) Normal Q–Q Plot of Standardized Training Residuals", "Standardized Residual Quantiles", box_txt)
    fig.suptitle("Figure 17: Multiple Linear Regression Residual Normality and Tail-Behavior Diagnostics", y=1.02)
    fig.tight_layout()
    return save_fig(fig, "fig17_regression_residual_qq_hist.png")


def plot_fig18_temporal_test_errors(reg_res: Dict[str, Any]) -> str:
    """Fig 18: 2-panel chronological hold-out test predictions and daily errors over time."""
    te_df = pd.read_csv(OUTPUTS_DIR / "model" / "test_predictions.csv")
    dates, resids = pd.to_datetime(te_df["dteday"]), te_df["residual_ols"].to_numpy()
    m, sp = reg_res["metrics"], reg_res["split_info"]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12.2, 7.6), sharex=True)

    ax1.plot(dates, te_df["y_true"], color=PALETTE_MAIN["navy"], lw=2.0, marker="o", markersize=3.2, label="Actual Daily Rentals")
    ax1.plot(dates, te_df["y_pred_ols"], color=PALETTE_MAIN["teal"], lw=2.0, ls="--", label=f"Primary OLS (RMSE={m['ols_test']['rmse']:,.1f}, R²={m['ols_test']['r2']:.3f})")
    ax1.plot(dates, te_df["y_pred_baseline"], color=PALETTE_MAIN["amber"], lw=1.8, ls=":", label=f"Mean Baseline (RMSE={m['baseline_test']['rmse']:,.1f}, R²={m['baseline_test']['r2']:.3f})")
    ax1.set(title=f"(A) Chronological Hold-Out Test Forecast ({sp['test_start_date']} to {sp['test_end_date']})", ylabel="Daily Rentals (cnt)")
    ax1.legend(loc="lower left", frameon=True, facecolor="white")

    ax2.axhline(0.0, color="black", lw=1.3)
    ax2.bar(dates, resids, width=0.8, color=np.where(resids >= 0, PALETTE_MAIN["blue"], PALETTE_MAIN["orange"]), alpha=0.75, label="Daily OLS Error (e_t = y_t − ŷ_t)")
    si = int(te_df["y_true"].idxmin())
    ax2.annotate(f"Hurricane Sandy ({te_df.loc[si, 'dteday']})\nActual={int(te_df.loc[si, 'y_true'])}, Error={resids[si]:+.0f}", xy=(dates.iloc[si], resids[si]), xytext=(dates.iloc[si] - pd.Timedelta(days=38), resids[si] - 350), arrowprops=dict(arrowstyle="->", color=PALETTE_MAIN["red"], lw=1.2), fontsize=8.2, fontweight="bold", color=PALETTE_MAIN["red"], bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=PALETTE_MAIN["red"]))
    ax2.set(title="(B) Temporal Prediction Errors Across Hold-Out Horizon", xlabel="Hold-Out Test Date (dteday)", ylabel="Residual (y_t − ŷ_t)", ylim=(-4300, 3200))
    ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.setp(ax2.get_xticklabels(), rotation=30, ha="right")
    ax2.legend(loc="upper right", frameon=True)
    fig.suptitle("Figure 18: Out-of-Sample Temporal Tracking and Error Dynamics on the 20% Test Horizon", y=1.01)
    fig.tight_layout()
    return save_fig(fig, "fig18_regression_temporal_predictions_errors.png")
