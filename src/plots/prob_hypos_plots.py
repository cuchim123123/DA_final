"""Phases 3 & 4 Probability Distribution and Hypothesis Testing Plots (Figures 6–11)."""

from __future__ import annotations

from typing import Any, Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns

from src.load_validate import SEASON_SHORT_LABELS
from src.plots.style import PALETTE_MAIN, SEASON_COLORS, add_stat_box, plot_qq_panel, save_fig


def plot_fig06_cnt_prob_diagnostics(df: pd.DataFrame, prob_res: Dict[str, Any]) -> str:
    """Fig 6: 2-panel probability diagnostics for `cnt` (Histogram/Fits + Normal Q-Q)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 5.0))
    y = df["cnt"].astype(float).to_numpy()
    my, sdy = float(np.mean(y)), float(np.std(y, ddof=1))
    disp = prob_res["cnt"]["poisson_diagnostics"]["variance_to_mean_ratio_index_of_dispersion"]
    nb = prob_res["cnt"]["negative_binomial_diagnostics"]
    nd = prob_res["cnt"]["normal_approximation_diagnostics"]

    sns.histplot(y, bins=28, stat="density", color=PALETTE_MAIN["lightgray"], alpha=0.55, edgecolor="white", ax=ax1, label="Observed Histogram")
    sns.kdeplot(y, color=PALETTE_MAIN["navy"], lw=2.2, ax=ax1, label="Empirical KDE")
    xg, xi = np.linspace(20, 8800, 400), np.arange(50, 8800, 25)
    ax1.plot(xg, stats.norm.pdf(xg, my, sdy), color=PALETTE_MAIN["blue"], ls="--", lw=2.2, label=f"Normal (μ={my:,.1f}, σ={sdy:,.1f})")
    ax1.plot(xi, stats.nbinom.pmf(xi, nb["r_dispersion_param"], nb["p_success_param"]), color=PALETTE_MAIN["orange"], ls="-.", lw=2.0, label=f"NegBin (r={nb['r_dispersion_param']:.2f}, Var/Mean={disp:.1f})")
    ax1.axvline(my, color=PALETTE_MAIN["red"], ls=":", lw=1.8, label=f"Poisson λ={my:,.1f} (SD={np.sqrt(my):.1f} vs {sdy:,.1f})")
    ax1.set(title="(A) Empirical Density vs. Parametric Candidate Families", xlabel="Total Daily Bike Rentals (cnt)", ylabel="Density")
    ax1.legend(loc="upper right", fontsize=8.0, frameon=True)

    box_txt = (
        f"Skewness = {prob_res['cnt']['skewness']:.4f}\n"
        f"Excess Kurtosis = {prob_res['cnt']['excess_kurtosis']:.4f} (Platykurtic)\n"
        f"Shapiro-Wilk W = {nd['shapiro_wilk_stat']:.4f} (p = {nd['shapiro_wilk_pvalue']:.2e})\n"
        f"D'Agostino K² = {nd['dagostino_k2_stat']:.2f} (p = {nd['dagostino_k2_pvalue']:.2e})\n"
        f"Lilliefors KS = {nd['lilliefors_ks_stat']:.4f} (boot p = {nd['lilliefors_bootstrap_pvalue']:.4f})"
    )
    plot_qq_panel(ax2, y, PALETTE_MAIN["blue"], "(B) Normal Q–Q Plot of Daily Bike Rentals (cnt)", "Sample Quantiles of cnt", box_txt)
    fig.suptitle("Figure 6: Probability Distribution Diagnostics for Daily Bike Rentals (cnt)", y=1.02)
    fig.tight_layout()
    return save_fig(fig, "fig06_cnt_distribution_diagnostics.png")


def plot_fig07_temp_prob_diagnostics(df: pd.DataFrame, prob_res: Dict[str, Any]) -> str:
    """Fig 7: 2-panel probability diagnostics for `temp` (Bimodal Mixture/Beta/Normal + Q-Q)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 5.0))
    x = df["temp"].astype(float).to_numpy()
    mx, sdx = float(np.mean(x)), float(np.std(x, ddof=1))
    bf, nf = prob_res["temp"]["beta_fit_0_1"], prob_res["temp"]["normal_fit"]

    sns.histplot(x, bins=26, stat="density", color=PALETTE_MAIN["lightgray"], alpha=0.50, edgecolor="white", ax=ax1, label="Observed Histogram")
    sns.kdeplot(x, color=PALETTE_MAIN["navy"], lw=2.3, ax=ax1, label="Pooled KDE (Bimodal Mixture)")
    g = np.linspace(0.02, 0.92, 300)
    ax1.plot(g, stats.norm.pdf(g, mx, sdx), color=PALETTE_MAIN["blue"], ls="--", lw=2.0, label=f"Normal (μ={mx:.3f}, σ={sdx:.3f})")
    ax1.plot(g, stats.beta.pdf(g, bf["alpha_mom"], bf["beta_mom"]), color=PALETTE_MAIN["orange"], ls="-.", lw=2.0, label=f"Beta(α={bf['alpha_mom']:.2f}, β={bf['beta_mom']:.2f})")
    sns.kdeplot(df.loc[df["season"] == 1, "temp"], color=SEASON_COLORS[1], ls=":", lw=1.5, ax=ax1, label="Season 1 (Cold) Sub-KDE")
    sns.kdeplot(df.loc[df["season"] == 3, "temp"], color=SEASON_COLORS[3], ls=":", lw=1.5, ax=ax1, label="Season 3 (Warm) Sub-KDE")
    ax1.set(title="(A) Normalized Temperature Density & Seasonal Sub-Regimes", xlabel="Normalized Temperature (temp, [0, 1])", ylabel="Density")
    ax1.legend(loc="upper right", fontsize=7.8, frameon=True)

    box_txt = (
        f"Support: Bounded in [0, 1]\nMean = {mx:.4f} ({mx*41:.2f}°C), SD = {sdx:.4f}\n"
        f"Skewness = {prob_res['temp']['skewness']:.4f}\n"
        f"Excess Kurtosis = {prob_res['temp']['excess_kurtosis']:.4f} (Platykurtic)\n"
        f"Shapiro-Wilk W = {nf['shapiro_wilk_stat']:.4f} (p = {nf['shapiro_wilk_pvalue']:.2e})\n"
        f"Lilliefors KS = {nf['lilliefors_ks_stat']:.4f} (boot p = {nf['lilliefors_bootstrap_pvalue']:.4f})"
    )
    plot_qq_panel(ax2, x, PALETTE_MAIN["teal"], "(B) Normal Q–Q Plot of Normalized Temperature (temp)", "Sample Quantiles of temp", box_txt)
    fig.suptitle("Figure 7: Probability Distribution Diagnostics for Ambient Temperature (temp)", y=1.02)
    fig.tight_layout()
    return save_fig(fig, "fig07_temp_distribution_diagnostics.png")


def plot_fig08_hum_windspeed_diagnostics(df: pd.DataFrame, prob_res: Dict[str, Any]) -> str:
    """Fig 8: 2x2 distribution diagnostic grid for `hum` and `windspeed`."""
    fig, axes = plt.subplots(2, 2, figsize=(12.2, 8.2))
    min_h = df.loc[df["hum"].idxmin()]
    for r_i, (col, color, lbl) in enumerate([
        ("hum", PALETTE_MAIN["blue"], "Normalized Humidity (hum, [0, 1])"),
        ("windspeed", PALETTE_MAIN["orange"], "Normalized Wind Speed (windspeed, [0, 1])"),
    ]):
        x, res = df[col].astype(float).to_numpy(), prob_res[col]
        ax_h, ax_q = axes[r_i, 0], axes[r_i, 1]
        sns.histplot(x, bins=25, stat="density", color=color, alpha=0.35, edgecolor="white", ax=ax_h, label="Histogram")
        sns.kdeplot(x, color=PALETTE_MAIN["navy"], lw=2.0, ax=ax_h, label="KDE")
        g = np.linspace(max(1e-3, x.min()), min(0.999, x.max() * 1.05), 250)
        bf, nf = res["beta_fit_0_1"], res["normal_fit"]
        ax_h.plot(g, stats.norm.pdf(g, res["mean"], res["sd"]), color=PALETTE_MAIN["red"], ls="--", lw=1.8, label=f"Normal(μ={res['mean']:.3f}, σ={res['sd']:.3f})")
        ax_h.plot(g, stats.beta.pdf(g, bf["alpha_mom"], bf["beta_mom"]), color=PALETTE_MAIN["teal"], ls="-.", lw=1.8, label=f"Beta(α={bf['alpha_mom']:.2f}, β={bf['beta_mom']:.2f})")
        if col == "hum":
            ax_h.annotate(f"Sensor Anomaly\n{min_h['dteday']} (hum={min_h['hum']:.1f})", xy=(float(min_h["hum"]), 0.2), xytext=(0.08, 1.8), arrowprops=dict(arrowstyle="->", color=PALETTE_MAIN["red"], lw=1.2), fontsize=8, fontweight="bold", color=PALETTE_MAIN["red"], bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=PALETTE_MAIN["red"]))
        ax_h.set(title=f"({chr(65+2*r_i)}) Density & Fits: {lbl}", xlabel=lbl, ylabel="Density")
        ax_h.legend(loc="upper right", fontsize=8)
        plot_qq_panel(ax_q, x, color, f"({chr(66+2*r_i)}) Normal Q–Q Plot: {col}", f"Sample Quantiles ({col})", f"Skewness = {res['skewness']:.4f}\nExcess Kurtosis = {res['excess_kurtosis']:.4f}\nShapiro W = {nf['shapiro_wilk_stat']:.4f} (p = {nf['shapiro_wilk_pvalue']:.2e})")
    fig.suptitle("Figure 8: Supplemental Distribution Diagnostics for Relative Humidity (hum) and Wind Speed (windspeed)", y=1.01)
    fig.tight_layout()
    return save_fig(fig, "fig08_hum_windspeed_distributions.png")


def plot_fig09_h1_ttest(df: pd.DataFrame, ht_res: Dict[str, Any]) -> str:
    """Fig 9: H1 Welch two-sample t-test visualization + casual/registered offset."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 5.2))
    h1, p1 = ht_res["h1_ttest"], ht_res["h1_ttest"]["primary_cnt_results"]
    pal = {0: PALETTE_MAIN["amber"], 1: PALETTE_MAIN["blue"]}
    sns.violinplot(data=df, x="workingday", y="cnt", hue="workingday", order=[0, 1], palette=pal, legend=False, inner=None, alpha=0.30, ax=ax1)
    sns.boxplot(data=df, x="workingday", y="cnt", hue="workingday", order=[0, 1], width=0.26, palette=pal, legend=False, boxprops=dict(alpha=0.75), showmeans=True, meanprops=dict(marker="D", markeredgecolor="black", markerfacecolor="gold", markersize=8), ax=ax1)
    ax1.set_xticks([0, 1])
    ax1.set_xticklabels([f"0: Non-Working Day\n(n={p1['n0']}, Mean={p1['mean0']:,.1f})", f"1: Working Day\n(n={p1['n1']}, Mean={p1['mean1']:,.1f})"])
    add_stat_box(ax1, f"H1: Welch Two-Sample t-Test on cnt\nΔ Mean = {p1['mean_diff_1_minus_0']:+.2f} bikes/day\n95% CI: [{p1['ci95_low']:+.2f}, {p1['ci95_high']:+.2f}]\nt_Welch = {p1['t_welch']:.4f}, df = {p1['df_welch']:.2f}\np = {p1['p_value_welch']:.4f} (Holm p = {h1['p_value_holm_family']:.4f})\nHedges' g = {p1['hedges_g']:+.4f} → {h1['decision_at_alpha_0_05']}", ec=PALETTE_MAIN["navy"])
    ax1.set(ylim=(-200, 10200), title="(A) H1 Primary Test: Total Rentals (cnt) by Working Day", xlabel="Working Day Indicator", ylabel="Total Daily Bike Rentals (cnt)")

    cas, reg = h1["component_offset_context"]["casual_welch"], h1["component_offset_context"]["registered_welch"]
    xp, w = np.arange(3), 0.34
    b0 = ax2.bar(xp - w / 2, [p1["mean0"], reg["mean0"], cas["mean0"]], width=w, color=PALETTE_MAIN["amber"], edgecolor="black", label="Non-Working Day")
    b1 = ax2.bar(xp + w / 2, [p1["mean1"], reg["mean1"], cas["mean1"]], width=w, color=PALETTE_MAIN["blue"], edgecolor="black", label="Working Day")
    for b in list(b0) + list(b1):
        ax2.text(b.get_x() + b.get_width() / 2.0, b.get_height() + 90, f"{b.get_height():,.0f}", ha="center", va="bottom", fontsize=8.2, fontweight="bold")
    ax2.set_xticks(xp)
    ax2.set_xticklabels([f"Total (cnt)\nΔ={p1['mean_diff_1_minus_0']:+.0f} (p={p1['p_value_welch']:.3f})", f"Registered\nΔ={reg['mean_diff_1_minus_0']:+,.0f} (p={reg['p_value_welch']:.1e})", f"Casual\nΔ={cas['mean_diff_1_minus_0']:+,.0f} (p={cas['p_value_welch']:.1e})"])
    ax2.set(ylim=(0, 5600), title="(B) Substantive Mechanism: Opposing Commuter vs. Leisure Shifts", xlabel="User Segment Component", ylabel="Group Mean Rentals")
    ax2.legend(loc="upper right", frameon=True)
    fig.suptitle("Figure 9: Hypothesis H1 — Welch Two-Sample t-Test on Working-Day Status and Compositional Offset", y=1.02)
    fig.tight_layout()
    return save_fig(fig, "fig09_h1_workingday_ttest.png")


def plot_fig10_h2_anova(df: pd.DataFrame, ht_res: Dict[str, Any]) -> str:
    """Fig 10: H2 One-Way & Welch ANOVA seasonal means + Tukey HSD pairwise forest plot."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.3))
    h2, om, groups = ht_res["h2_anova"], ht_res["h2_anova"]["omnibus_results"], ht_res["h2_anova"]["group_summaries"]
    bars = ax1.bar(range(4), [g["mean_cnt"] for g in groups], yerr=[g["mean_cnt"] - g["ci95_low"] for g in groups], capsize=6, color=[SEASON_COLORS[g["season"]] for g in groups], alpha=0.82, edgecolor="black", width=0.52)
    for b, g in zip(bars, groups):
        ax1.text(b.get_x() + b.get_width() / 2.0, g["ci95_high"] + 130, f"{g['mean_cnt']:,.1f}\n±{g['mean_cnt']-g['ci95_low']:.0f} (n={g['n']})", ha="center", va="bottom", fontsize=8.3, fontweight="bold")
    ax1.set_xticks(range(4))
    ax1.set_xticklabels([SEASON_SHORT_LABELS[g["season"]] for g in groups])
    add_stat_box(ax1, f"H2 Omnibus ANOVA Results:\nOrdinary F({om['df_between']}, {om['df_within']}) = {om['f_statistic_ordinary']:.2f}, p = {om['p_value_ordinary_anova']:.2e}\nWelch F({om['df_welch_num']:.0f}, {om['df_welch_den']:.1f}) = {om['f_statistic_welch']:.2f}, p = {om['p_value_welch_anova']:.2e}\nKruskal-Wallis H = {om['kruskal_wallis_h']:.2f}, p = {om['p_value_kruskal_wallis']:.2e}\nEffect Size: η² = {om['eta_squared']:.4f} ({om['eta_squared']*100:.1f}%), ω² = {om['omega_squared']:.4f}", x=0.03, y=0.96, ec=PALETTE_MAIN["navy"])
    ax1.set(ylim=(0, 8800), title="(A) Seasonal Group Means with 95% Confidence Intervals", xlabel="UCI Season Category", ylabel="Mean Daily Bike Rentals (cnt)")

    post = h2["posthoc_comparisons"]
    ax2.axvline(0.0, color=PALETTE_MAIN["red"], ls="--", lw=1.6, label="Zero Difference (H0)")
    for i, p in enumerate(post):
        d, lo, hi = p["mean_diff_g2_minus_g1"], p["tukey_ci95_low"], p["tukey_ci95_high"]
        col = PALETTE_MAIN["teal"] if p["tukey_reject_0_05"] else PALETTE_MAIN["gray"]
        ax2.errorbar(d, i, xerr=[[d - lo], [hi - d]], fmt="o", color=col, ecolor=col, elinewidth=2.2, capsize=5, markersize=7)
        ax2.text(d, i + 0.22, f"{d:+.0f} [{lo:+.0f}, {hi:+.0f}]", ha="center", va="bottom", fontsize=8.0, color=col, fontweight="bold")
    ytick_lbls = []
    for p in post:
        st = "Sig, p<0.01" if p["tukey_reject_0_05"] else f"NS, p={p['tukey_p_adj']:.3f}"
        ytick_lbls.append(f"Season {p['group2']} − Season {p['group1']}\n({st})")
    ax2.set_yticks(range(len(post)))
    ax2.set_yticklabels(ytick_lbls)
    ax2.set(ylim=(-0.6, len(post) - 0.3), xlim=(-3500, 3900), title=f"(B) Tukey HSD 95% Family-Wise Confidence Intervals ({len(post)} Pairs)", xlabel="Pairwise Mean Difference in cnt (Group 2 − Group 1)")
    ax2.legend(loc="lower left", frameon=True)
    fig.suptitle("Figure 10: Hypothesis H2 — One-Way & Welch ANOVA Across Seasons and Post-Hoc Comparisons", y=1.02)
    fig.tight_layout()
    return save_fig(fig, "fig10_h2_season_anova.png")


def plot_fig11_h3_chisq(ht_res: Dict[str, Any]) -> str:
    """Fig 11: H3 Chi-square stacked proportions + Observed vs Expected counts."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 5.1))
    h3, ct, om, ed = ht_res["h3_chisq"], ht_res["h3_chisq"]["contingency_table"], ht_res["h3_chisq"]["omnibus_results"], ht_res["h3_chisq"]["expected_frequency_diagnostics"]
    thr, xp = int(h3["threshold_median_cnt"]), np.arange(len(ct))
    pl, ph = [r["pct_low_demand"] for r in ct], [r["pct_high_demand"] for r in ct]
    labels = [f"{r['weathersit']}: {r['weathersit_label'].split(': ')[1]}\n(n={r['row_total']})" for r in ct]

    ax1.bar(xp, pl, width=0.52, color=PALETTE_MAIN["lightgray"], edgecolor="black", label=f"Low/Mod Demand (cnt ≤ {thr:,})")
    ax1.bar(xp, ph, bottom=pl, width=0.52, color=PALETTE_MAIN["blue"], edgecolor="black", label=f"High Demand (cnt > {thr:,})")
    for i, (l_v, h_v, r) in enumerate(zip(pl, ph, ct)):
        ax1.text(i, l_v / 2.0, f"{l_v:.1f}%\n({r['observed_low_demand']})", ha="center", va="center", fontsize=8.5, fontweight="bold")
        ax1.text(i, l_v + (h_v / 2.0 if h_v > 8 else h_v + 4.0), f"{h_v:.1f}% ({r['observed_high_demand']})", ha="center", va="center", fontsize=8.5, fontweight="bold", color="white" if h_v > 8 else PALETTE_MAIN["blue"])
    ax1.set_xticks(xp); ax1.set_xticklabels(labels)
    ax1.set(ylim=(0, 128), title="(A) Conditional Share of High-Demand Days by Weather", xlabel="Daily Weather Condition (weathersit)", ylabel="Percentage of Days (%)")
    ax1.legend(loc="upper right", frameon=True)

    w = 0.34
    bo = ax2.bar(xp - w / 2, [r["observed_high_demand"] for r in ct], width=w, color=PALETTE_MAIN["teal"], edgecolor="black", label="Observed High-Demand (O_ij)")
    be = ax2.bar(xp + w / 2, [r["expected_high_demand"] for r in ct], width=w, color=PALETTE_MAIN["amber"], edgecolor="black", label="Expected Under H0 (E_ij)")
    for b in list(bo) + list(be):
        ax2.text(b.get_x() + b.get_width() / 2.0, b.get_height() + 4, f"{b.get_height():.1f}", ha="center", va="bottom", fontsize=8.3, fontweight="bold")
    add_stat_box(ax2, f"H3 Chi-Square Independence Test:\nPearson χ²({om['df']}) = {om['pearson_chi2']:.2f}, p = {om['p_value_chi2']:.2e}\nLikelihood-Ratio G²({om['df']}) = {om['likelihood_ratio_g2']:.2f}, p = {om['p_value_g2']:.2e}\nCramér's V = {om['cramers_v']:.4f}\nMin Expected Count = {ed['min_expected_cell_count']:.2f} ≥ 5\n2×2 Fisher OR = {h3['collapsed_2x2_robustness_check']['fisher_exact_odds_ratio']:.2f} (p = {h3['collapsed_2x2_robustness_check']['fisher_exact_pvalue']:.2e})", x=0.34, y=0.78, ec=PALETTE_MAIN["navy"])
    ax2.set_xticks(xp); ax2.set_xticklabels(labels)
    ax2.set(ylim=(0, 350), title="(B) Observed vs. Expected High-Demand Counts under H0", xlabel="Daily Weather Condition (weathersit)", ylabel="Number of Days")
    ax2.legend(loc="upper right", frameon=True)
    fig.suptitle("Figure 11: Hypothesis H3 — Chi-Square Test of Independence Between Weather Condition and High Demand", y=1.02)
    fig.tight_layout()
    return save_fig(fig, "fig11_h3_weathersit_highdemand_chisq.png")
