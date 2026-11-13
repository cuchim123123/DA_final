"""Phase 2 Exploratory Data Analysis Visualizations (Figures 1–5)."""

from __future__ import annotations

from typing import Any, Dict

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
from statsmodels.nonparametric.smoothers_lowess import lowess

from src.load_validate import SEASON_SHORT_LABELS, WORKINGDAY_LABELS
from src.plots.style import PALETTE_MAIN, SEASON_CALENDAR_RANGES, SEASON_COLORS, save_fig


def plot_fig01_timeseries(df: pd.DataFrame, reg_res: Dict[str, Any]) -> str:
    """Fig 1: Daily bike rentals time series (2011-2012) with 30-day rolling mean and split."""
    fig, ax = plt.subplots(figsize=(12, 5.2))
    dates, cnt = df["dteday_parsed"], df["cnt"].astype(float)
    sp = reg_res["split_info"]
    split_dt = pd.to_datetime(sp["test_start_date"])

    ax.plot(dates, cnt, color=PALETTE_MAIN["blue"], alpha=0.45, lw=1.0, label="Daily Rental Count (cnt)")
    ax.plot(dates, cnt.rolling(30, center=True, min_periods=7).mean(), color=PALETTE_MAIN["navy"], lw=2.3, label="30-Day Rolling Mean")
    ax.axvline(split_dt, color=PALETTE_MAIN["red"], ls="--", lw=1.8, label=f"80/20 Split ({sp['test_start_date']})")
    ax.axvspan(split_dt, dates.max(), color=PALETTE_MAIN["amber"], alpha=0.10, label=f"Hold-Out Test (n={sp['test_n']})")

    min_i, max_i = int(cnt.idxmin()), int(cnt.idxmax())
    ax.scatter([dates.iloc[min_i], dates.iloc[max_i]], [cnt.iloc[min_i], cnt.iloc[max_i]], color=[PALETTE_MAIN["red"], PALETTE_MAIN["teal"]], s=55, zorder=5)
    for idx, label, col, dx, dy in [
        (min_i, "Hurricane Sandy", PALETTE_MAIN["red"], -140, 850),
        (max_i, "System Peak", PALETTE_MAIN["teal"], -145, -600),
    ]:
        ax.annotate(
            f"{label}\n{df.loc[idx, 'dteday']} (cnt = {int(cnt.iloc[idx]):,})",
            xy=(dates.iloc[idx], cnt.iloc[idx]), xytext=(dates.iloc[idx] + pd.Timedelta(days=dx), cnt.iloc[idx] + dy),
            arrowprops=dict(arrowstyle="->", color=col, lw=1.2), fontsize=8.5, fontweight="bold", color=col,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=col, alpha=0.9),
        )

    ax.set(title="Figure 1: Daily Bike-Rental Demand Time Series, Seasonal Regimes, and 80/20 Split (2011–2012)", xlabel="Calendar Date (dteday)", ylabel="Total Daily Bike Rentals (cnt, bikes/day)", ylim=(-200, 9600))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.9)
    return save_fig(fig, "fig01_daily_rentals_timeseries.png")


def plot_fig02_cnt_hist_kde(df: pd.DataFrame) -> str:
    """Fig 2: Histogram + KDE of `cnt` overall and stratified by operational year (2011 vs 2012)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.8))
    cnt = df["cnt"].astype(float)
    sns.histplot(cnt, bins=28, stat="density", color=PALETTE_MAIN["blue"], alpha=0.35, edgecolor="white", ax=ax1, label="Histogram (28 bins)")
    sns.kdeplot(cnt, color=PALETTE_MAIN["navy"], lw=2.2, ax=ax1, label="Empirical KDE")
    ax1.axvline(float(cnt.mean()), color=PALETTE_MAIN["red"], ls="--", lw=1.8, label=f"Mean = {cnt.mean():,.1f}")
    ax1.axvline(float(cnt.median()), color=PALETTE_MAIN["teal"], ls=":", lw=2.0, label=f"Median = {cnt.median():,.1f}")
    ax1.set(title=f"(A) Overall Distribution of Daily Rentals (N = {len(cnt)})", xlabel="Total Daily Bike Rentals (cnt)", ylabel="Density")
    ax1.legend(loc="upper right", frameon=True)

    c0, c1 = df.loc[df["yr"] == 0, "cnt"].astype(float), df.loc[df["yr"] == 1, "cnt"].astype(float)
    yoy = 100.0 * (float(c1.mean()) - float(c0.mean())) / float(c0.mean())
    for s, col, lbl in [
        (c0, PALETTE_MAIN["blue"], f"2011 (n={len(c0)}, Mean={c0.mean():,.0f})"),
        (c1, PALETTE_MAIN["orange"], f"2012 (n={len(c1)}, Mean={c1.mean():,.0f}, {yoy:+.1f}%)"),
    ]:
        sns.histplot(s, bins=22, stat="density", color=col, alpha=0.30, ax=ax2, label=lbl)
        sns.kdeplot(s, color=col, lw=2.0, ax=ax2)
    ax2.set(title="(B) Structural Shift Between 2011 and 2012 Regimes", xlabel="Total Daily Bike Rentals (cnt)", ylabel="Density")
    ax2.legend(loc="upper right", frameon=True)
    fig.suptitle("Figure 2: Empirical Distribution of Daily Bike Rentals — Overall vs. Year-by-Year Expansion", y=1.02)
    fig.tight_layout()
    return save_fig(fig, "fig02_cnt_distribution_hist_kde.png")


def plot_fig03_season_boxplot(df: pd.DataFrame) -> str:
    """Fig 3: Boxplot + jittered strip plot of `cnt` across the four seasons."""
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    order = [1, 2, 3, 4]
    sns.boxplot(
        data=df, x="season", y="cnt", hue="season", order=order, palette=SEASON_COLORS, legend=False,
        width=0.48, boxprops=dict(alpha=0.45), showmeans=True,
        meanprops=dict(marker="D", markeredgecolor="black", markerfacecolor="gold", markersize=8), ax=ax,
    )
    sns.stripplot(data=df, x="season", y="cnt", hue="season", order=order, palette=SEASON_COLORS, legend=False, size=4.2, jitter=0.18, alpha=0.55, ax=ax)
    for i, s in enumerate(order):
        sub = df.loc[df["season"] == s, "cnt"]
        ax.text(i, 8950, f"Mean: {sub.mean():,.0f}\nMedian: {sub.median():,.0f}", ha="center", va="top", fontsize=8.5, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#CCCCCC", alpha=0.9))
    ax.set_xticks(range(4))
    ax.set_xticklabels([f"{SEASON_SHORT_LABELS[s]}\n[{SEASON_CALENDAR_RANGES[s]}]\n(n={int((df['season']==s).sum())})" for s in order])
    ax.set(ylim=(-100, 9400), title="Figure 3: Distribution of Daily Bike Rentals Across Seasons (Boxplots, Means [◆], and Observations)", xlabel="UCI Season Category", ylabel="Total Daily Bike Rentals (cnt, bikes/day)")
    return save_fig(fig, "fig03_cnt_boxplot_by_season.png")


def plot_fig04_temp_vs_cnt_scatter(df: pd.DataFrame) -> str:
    """Fig 4: Scatter plot of `temp` vs `cnt` colored by season with OLS and LOWESS trends."""
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    for s in [1, 2, 3, 4]:
        sub = df[df["season"] == s]
        ax.scatter(sub["temp"], sub["cnt"], color=SEASON_COLORS[s], label=SEASON_SHORT_LABELS[s], alpha=0.68, s=32, edgecolors="white", lw=0.4)
    xt, yc = df["temp"].astype(float).to_numpy(), df["cnt"].astype(float).to_numpy()
    sl, ic, r_v, p_v, _ = stats.linregress(xt, yc)
    xg = np.linspace(xt.min(), xt.max(), 200)
    ax.plot(xg, ic + sl * xg, color=PALETTE_MAIN["navy"], ls="--", lw=2.2, label=f"Linear OLS Fit (r = {r_v:.3f}, p = {p_v:.1e})")
    lw = lowess(yc, xt, frac=0.35)
    ax.plot(lw[:, 0], lw[:, 1], color=PALETTE_MAIN["red"], lw=2.4, label="Non-Parametric LOWESS Curve")
    ax_top = ax.twiny()
    ax_top.set_xlim(ax.get_xlim()[0] * 41.0, ax.get_xlim()[1] * 41.0)
    ax_top.set_xlabel("Approximate Ambient Temperature (°C = 41 × temp)", fontsize=9.5)
    ax_top.grid(False)
    ax.set_title("Figure 4: Daily Bike Rentals vs. Ambient Temperature by Season with Linear and LOWESS Fits", pad=14)
    ax.set(xlabel="Normalized Ambient Temperature (temp, [0, 1])", ylabel="Total Daily Bike Rentals (cnt, bikes/day)")
    ax.legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.92)
    return save_fig(fig, "fig04_temp_vs_cnt_scatter.png")


def plot_fig05_weather_workday_bars(df: pd.DataFrame) -> str:
    """Fig 5: Grouped bar chart of mean `cnt` by `weathersit` and `workingday` with 95% CIs."""
    fig, ax = plt.subplots(figsize=(10.2, 5.2))
    x_pos, width = np.arange(3), 0.35
    for offset, wd, col in [(-width / 2, 0, PALETTE_MAIN["amber"]), (width / 2, 1, PALETTE_MAIN["blue"])]:
        means, cis, ns = [], [], []
        for w in [1, 2, 3]:
            sub = df[(df["weathersit"] == w) & (df["workingday"] == wd)]["cnt"].astype(float)
            n, m = len(sub), float(sub.mean())
            ci = float(stats.t.ppf(0.975, df=n - 1) * float(sub.std(ddof=1)) / np.sqrt(n))
            means.append(m); cis.append(ci); ns.append(n)
        bars = ax.bar(x_pos + offset, means, width=width, yerr=cis, capsize=5, color=col, alpha=0.85, edgecolor="black", lw=0.7, label=WORKINGDAY_LABELS[wd])
        for b, m_v, ci_v, n_v in zip(bars, means, cis, ns):
            ax.text(b.get_x() + b.get_width() / 2.0, m_v + ci_v + 140, f"{m_v:,.0f}\n(n={n_v})", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f"{w}: {lbl}\n(Total n = {int((df['weathersit']==w).sum())})" for w, lbl in [(1, "Clear / Partly Cloudy"), (2, "Mist / Cloudy"), (3, "Light Snow / Rain")]])
    ax.set(ylim=(0, 6200), title="Figure 5: Subgroup Mean Daily Bike Rentals by Weather Condition and Working-Day Status (±95% CI)", xlabel="Daily Weather Condition Category (weathersit)", ylabel="Mean Daily Bike Rentals (cnt, bikes/day)")
    ax.legend(loc="upper right", frameon=True, facecolor="white")
    return save_fig(fig, "fig05_mean_cnt_by_weather_workday_ci.png")
