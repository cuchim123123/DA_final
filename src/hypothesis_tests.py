"""Phase 4: Parametric & non-parametric hypothesis tests (H1 t-test, H2 ANOVA, H3 Chi-square)."""

from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.oneway import anova_oneway

from src.load_validate import (
    SEASON_SHORT_LABELS,
    TABLES_DIR,
    WEATHERSIT_LABELS,
    load_and_validate_data,
)


def _compute_two_group_stats(
    g1: np.ndarray, g0: np.ndarray, n_perm: int = 10000, seed: int = 42
) -> Dict[str, Any]:
    """Compute Welch/Student t-tests, Levene, Hedges' g, Mann-Whitney U, and permutation test."""
    n1, n0 = len(g1), len(g0)
    m1, m0 = float(np.mean(g1)), float(np.mean(g0))
    sd1, sd0 = float(np.std(g1, ddof=1)), float(np.std(g0, ddof=1))
    var1, var0 = float(np.var(g1, ddof=1)), float(np.var(g0, ddof=1))
    diff = m1 - m0

    se_w = float(np.sqrt(var1 / n1 + var0 / n0))
    df_w = float((var1 / n1 + var0 / n0) ** 2 / ((var1 / n1) ** 2 / (n1 - 1) + (var0 / n0) ** 2 / (n0 - 1)))
    t_w = diff / se_w
    p_w = float(2.0 * stats.t.sf(abs(t_w), df=df_w))
    hw = float(stats.t.ppf(0.975, df=df_w) * se_w)

    df_p = n1 + n0 - 2
    s_p = float(np.sqrt(((n1 - 1) * var1 + (n0 - 1) * var0) / df_p))
    t_s = diff / (s_p * float(np.sqrt(1.0 / n1 + 1.0 / n0)))
    p_s = float(2.0 * stats.t.sf(abs(t_s), df=df_p))
    d = diff / s_p
    g = d * (1.0 - 3.0 / (4.0 * df_p - 1.0))

    lev_f, lev_p = stats.levene(g1, g0, center="mean")
    bf_f, bf_p = stats.levene(g1, g0, center="median")
    sw1_w, sw1_p = stats.shapiro(g1)
    sw0_w, sw0_p = stats.shapiro(g0)
    mwu = stats.mannwhitneyu(g1, g0, alternative="two-sided")
    u_stat = float(mwu.statistic)

    rng = np.random.default_rng(seed)
    comb = np.concatenate([g1, g0])
    perm_diffs = np.array([
        np.mean(p[:n1]) - np.mean(p[n1:]) for p in (rng.permutation(comb) for _ in range(n_perm))
    ])
    p_perm = float((np.sum(np.abs(perm_diffs) >= abs(diff)) + 1.0) / (n_perm + 1.0))

    return {
        "n1": int(n1), "n0": int(n0), "mean1": round(m1, 4), "sd1": round(sd1, 4),
        "median1": round(float(np.median(g1)), 4),
        "iqr1": round(float(np.percentile(g1, 75) - np.percentile(g1, 25)), 4),
        "mean0": round(m0, 4), "sd0": round(sd0, 4),
        "median0": round(float(np.median(g0)), 4),
        "iqr0": round(float(np.percentile(g0, 75) - np.percentile(g0, 25)), 4),
        "mean_diff_1_minus_0": round(diff, 4), "se_welch": round(se_w, 4),
        "t_welch": round(t_w, 4), "df_welch": round(df_w, 4), "p_value_welch": p_w,
        "ci95_low": round(diff - hw, 4), "ci95_high": round(diff + hw, 4),
        "t_student_pooled": round(t_s, 4), "df_pooled": int(df_p), "p_value_student_pooled": p_s,
        "cohens_d": round(d, 4), "hedges_g": round(g, 4),
        "levene_mean_f": round(float(lev_f), 4), "levene_mean_p": float(lev_p),
        "brown_forsythe_median_f": round(float(bf_f), 4), "brown_forsythe_median_p": float(bf_p),
        "shapiro_group1_w": round(float(sw1_w), 4), "shapiro_group1_p": float(sw1_p),
        "shapiro_group0_w": round(float(sw0_w), 4), "shapiro_group0_p": float(sw0_p),
        "mann_whitney_u": round(u_stat, 2), "p_value_mann_whitney": float(mwu.pvalue),
        "rank_biserial_r": round(float(2.0 * u_stat / (n1 * n0) - 1.0), 4),
        "p_value_permutation_10000": round(p_perm, 4),
    }


def run_h1_workingday_ttest(df: pd.DataFrame) -> Dict[str, Any]:
    """Execute H1: Working day (`workingday=1`) vs Non-working day (`workingday=0`) on `cnt`."""
    res = {}
    for col in ["cnt", "casual", "registered"]:
        g1 = df.loc[df["workingday"] == 1, col].astype(float).to_numpy()
        g0 = df.loc[df["workingday"] == 0, col].astype(float).to_numpy()
        res[col] = _compute_two_group_stats(g1, g0)

    c = res["cnt"]
    decision = "Reject H0" if c["p_value_welch"] < 0.05 else "Fail to Reject H0"
    return {
        "hypothesis_id": "H1",
        "primary_cnt_results": c,
        "component_offset_context": {
            "casual_welch": {k: res["casual"][k] for k in ["mean1", "mean0", "mean_diff_1_minus_0", "t_welch", "df_welch", "p_value_welch", "hedges_g"]},
            "registered_welch": {k: res["registered"][k] for k in ["mean1", "mean0", "mean_diff_1_minus_0", "t_welch", "df_welch", "p_value_welch", "hedges_g"]},
        },
        "decision_at_alpha_0_05": decision,
    }


def run_h2_season_anova(df: pd.DataFrame) -> Dict[str, Any]:
    """Execute H2: One-Way & Welch ANOVA across `season` (1..4) on `cnt` with Tukey HSD post-hoc."""
    groups = [df.loc[df["season"] == s, "cnt"].astype(float).to_numpy() for s in [1, 2, 3, 4]]
    n_tot, k = len(df), len(groups)
    f_ord, p_ord = stats.f_oneway(*groups)
    df_b, df_w = k - 1, n_tot - k

    gm = float(df["cnt"].mean())
    ss_tot = float(((df["cnt"] - gm) ** 2).sum())
    ss_b = float(sum(len(g) * ((np.mean(g) - gm) ** 2) for g in groups))
    ms_w = (ss_tot - ss_b) / df_w
    eta_sq = ss_b / ss_tot
    omega_sq = (ss_b - df_b * ms_w) / (ss_tot + ms_w)

    welch = anova_oneway(groups, use_var="unequal")
    df_wn, df_wd = [float(x) for x in welch.df]
    lev_f, lev_p = stats.levene(*groups, center="mean")
    bf_f, bf_p = stats.levene(*groups, center="median")
    kw_h, kw_p = stats.kruskal(*groups)

    group_summaries = []
    for s_code, g in zip([1, 2, 3, 4], groups):
        ng, mg, sdg = len(g), float(np.mean(g)), float(np.std(g, ddof=1))
        seg = sdg / np.sqrt(ng)
        hw = float(stats.t.ppf(0.975, df=ng - 1) * seg)
        sw_w, sw_p = stats.shapiro(g)
        group_summaries.append({
            "season": s_code, "season_label": SEASON_SHORT_LABELS[s_code], "n": int(ng),
            "mean_cnt": round(mg, 4), "sd_cnt": round(sdg, 4), "se_cnt": round(seg, 4),
            "ci95_low": round(mg - hw, 4), "ci95_high": round(mg + hw, 4),
            "median_cnt": round(float(np.median(g)), 4),
            "iqr_cnt": round(float(np.percentile(g, 75) - np.percentile(g, 25)), 4),
            "shapiro_w": round(float(sw_w), 4), "shapiro_p": float(sw_p),
        })

    tukey = pairwise_tukeyhsd(df["cnt"].astype(float).to_numpy(), df["season"].to_numpy(), alpha=0.05)
    t_df = pd.DataFrame(tukey._results_table.data[1:], columns=tukey._results_table.data[0])

    pair_records, raw_ps = [], []
    for (s1, g1), (s2, g2) in combinations(zip([1, 2, 3, 4], groups), 2):
        rp = _compute_two_group_stats(g2, g1, n_perm=2000)
        raw_ps.append(rp["p_value_welch"])
        tr = t_df[(t_df["group1"] == s1) & (t_df["group2"] == s2)].iloc[0]
        pair_records.append({
            "group1": int(s1), "group1_label": SEASON_SHORT_LABELS[s1],
            "group2": int(s2), "group2_label": SEASON_SHORT_LABELS[s2],
            "mean_group1": rp["mean0"], "mean_group2": rp["mean1"],
            "mean_diff_g2_minus_g1": rp["mean_diff_1_minus_0"],
            "tukey_ci95_low": round(float(tr["lower"]), 4),
            "tukey_ci95_high": round(float(tr["upper"]), 4),
            "tukey_p_adj": round(float(tr["p-adj"]), 6),
            "tukey_reject_0_05": bool(tr["reject"]),
            "welch_t_g2_minus_g1": rp["t_welch"], "welch_df": rp["df_welch"],
            "welch_p_unadjusted": rp["p_value_welch"], "hedges_g_g2_minus_g1": rp["hedges_g"],
        })

    _, p_holm, _, _ = multipletests(raw_ps, alpha=0.05, method="holm")
    for rec, ph in zip(pair_records, p_holm):
        rec["welch_p_holm_adjusted"] = float(ph)
        rec["welch_reject_0_05"] = bool(ph < 0.05)

    return {
        "hypothesis_id": "H2",
        "omnibus_results": {
            "f_statistic_ordinary": round(float(f_ord), 4), "df_between": int(df_b), "df_within": int(df_w),
            "p_value_ordinary_anova": float(p_ord), "f_statistic_welch": round(float(welch.statistic), 4),
            "df_welch_num": round(df_wn, 4), "df_welch_den": round(df_wd, 4),
            "p_value_welch_anova": float(welch.pvalue), "kruskal_wallis_h": round(float(kw_h), 4),
            "p_value_kruskal_wallis": float(kw_p), "eta_squared": round(eta_sq, 4),
            "omega_squared": round(omega_sq, 4),
            "kruskal_epsilon_squared": round(float(kw_h / ((n_tot**2 - 1.0) / (n_tot + 1.0))), 4),
            "levene_mean_f": round(float(lev_f), 4), "levene_mean_p": float(lev_p),
            "brown_forsythe_median_f": round(float(bf_f), 4), "brown_forsythe_median_p": float(bf_p),
        },
        "group_summaries": group_summaries,
        "posthoc_comparisons": pair_records,
        "decision_at_alpha_0_05": "Reject H0" if (p_ord < 0.05 and welch.pvalue < 0.05) else "Fail to Reject H0",
    }


def run_h3_weather_highdemand_chisq(df: pd.DataFrame) -> Dict[str, Any]:
    """Execute H3: Chi-Square test of independence between `weathersit` and `high_demand`."""
    med_cnt = float(df["cnt"].median())
    hd = (df["cnt"] > med_cnt).astype(int)
    obs = pd.crosstab(df["weathersit"], hd).reindex(index=[1, 2, 3], columns=[0, 1], fill_value=0).to_numpy(dtype=float)

    chi2, p_c, dof, exp = stats.chi2_contingency(obs, correction=False)
    g2, p_g, _, _ = stats.chi2_contingency(obs, correction=False, lambda_="log-likelihood")
    n_tot = int(obs.sum())
    cramers_v = float(np.sqrt(chi2 / (n_tot * min(obs.shape[0] - 1, obs.shape[1] - 1))))

    rt, ct = obs.sum(1, keepdims=True), obs.sum(0, keepdims=True)
    p_res = (obs - exp) / np.sqrt(exp)
    adj_res = (obs - exp) / np.sqrt(exp * (1.0 - rt / n_tot) * (1.0 - ct / n_tot))
    min_exp = float(exp.min())

    ct_rows = []
    for idx, w in enumerate([1, 2, 3]):
        r_t = int(rt[idx, 0])
        ol, oh = int(obs[idx, 0]), int(obs[idx, 1])
        ct_rows.append({
            "weathersit": w, "weathersit_label": WEATHERSIT_LABELS[w],
            "observed_low_demand": ol, "observed_high_demand": oh, "row_total": r_t,
            "expected_low_demand": round(float(exp[idx, 0]), 4),
            "expected_high_demand": round(float(exp[idx, 1]), 4),
            "pct_low_demand": round(100.0 * ol / r_t, 2),
            "pct_high_demand": round(100.0 * oh / r_t, 2),
            "pearson_residual_high_demand": round(float(p_res[idx, 1]), 4),
            "std_adjusted_residual_high_demand": round(float(adj_res[idx, 1]), 4),
        })

    cm = df["weathersit"] == 1
    tab2 = np.array([
        [int((cm & (hd == 1)).sum()), int((cm & (hd == 0)).sum())],
        [int((~cm & (hd == 1)).sum()), int((~cm & (hd == 0)).sum())],
    ])
    or_val, p_fish = stats.fisher_exact(tab2, alternative="two-sided")

    return {
        "hypothesis_id": "H3",
        "threshold_median_cnt": med_cnt,
        "omnibus_results": {
            "pearson_chi2": round(float(chi2), 4), "df": int(dof), "p_value_chi2": float(p_c),
            "likelihood_ratio_g2": round(float(g2), 4), "p_value_g2": float(p_g),
            "cramers_v": round(cramers_v, 4), "cohens_w": round(float(np.sqrt(chi2 / n_tot)), 4),
            "n_total": n_tot,
        },
        "expected_frequency_diagnostics": {
            "min_expected_cell_count": round(min_exp, 4),
            "cells_with_expected_lt_5": int((exp < 5.0).sum()),
            "cochran_criterion_satisfied": bool(min_exp >= 5.0),
        },
        "contingency_table": ct_rows,
        "collapsed_2x2_robustness_check": {
            "fisher_exact_odds_ratio": round(float(or_val), 4),
            "fisher_exact_pvalue": float(p_fish),
        },
        "decision_at_alpha_0_05": "Reject H0" if p_c < 0.05 else "Fail to Reject H0",
    }


def run_all_hypothesis_tests(
    df: pd.DataFrame | None = None, save_outputs: bool = True
) -> Dict[str, Any]:
    """Execute H1, H2, and H3, apply family-wise Holm correction, and export tables."""
    if df is None:
        df, _ = load_and_validate_data(save_outputs=save_outputs)

    h1 = run_h1_workingday_ttest(df)
    h2 = run_h2_season_anova(df)
    h3 = run_h3_weather_highdemand_chisq(df)

    p1, om2, om3 = h1["primary_cnt_results"], h2["omnibus_results"], h3["omnibus_results"]
    raw_ps = [p1["p_value_welch"], om2["p_value_ordinary_anova"], om3["p_value_chi2"]]
    _, holm_ps, _, _ = multipletests(raw_ps, alpha=0.05, method="holm")

    h1["p_value_holm_family"] = float(holm_ps[0])
    om2["p_value_holm_family"] = float(holm_ps[1])
    om3["p_value_holm_family"] = float(holm_ps[2])

    summary_rows: List[Dict[str, Any]] = [
        {
            "hypothesis_id": "H1", "test_family": "Welch Two-Sample t-Test",
            "variables": "workingday (0 vs 1) -> cnt",
            "test_statistic": f"t_Welch = {p1['t_welch']:.4f} (df = {p1['df_welch']:.2f})",
            "p_value_unadjusted": raw_ps[0], "p_value_holm_adjusted": float(holm_ps[0]),
            "effect_size": f"Hedges' g = {p1['hedges_g']:+.4f}",
            "decision_alpha_0_05": h1["decision_at_alpha_0_05"],
        },
        {
            "hypothesis_id": "H2", "test_family": "One-Way & Welch ANOVA",
            "variables": "season (1..4) -> cnt",
            "test_statistic": f"F({om2['df_between']}, {om2['df_within']}) = {om2['f_statistic_ordinary']:.4f}",
            "p_value_unadjusted": raw_ps[1], "p_value_holm_adjusted": float(holm_ps[1]),
            "effect_size": f"eta^2 = {om2['eta_squared']:.4f}, omega^2 = {om2['omega_squared']:.4f}",
            "decision_alpha_0_05": h2["decision_at_alpha_0_05"],
        },
        {
            "hypothesis_id": "H3", "test_family": "Pearson Chi-Square Independence",
            "variables": f"weathersit (1..3) x high_demand (cnt > {h3['threshold_median_cnt']:.0f})",
            "test_statistic": f"chi^2({om3['df']}) = {om3['pearson_chi2']:.4f}",
            "p_value_unadjusted": raw_ps[2], "p_value_holm_adjusted": float(holm_ps[2]),
            "effect_size": f"Cramer's V = {om3['cramers_v']:.4f}",
            "decision_alpha_0_05": h3["decision_at_alpha_0_05"],
        },
    ]

    if save_outputs:
        TABLES_DIR.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(summary_rows).to_csv(TABLES_DIR / "hypothesis_tests_summary.csv", index=False)
        pd.DataFrame([
            {"segment": "cnt", **p1},
            {"segment": "registered", **h1["component_offset_context"]["registered_welch"]},
            {"segment": "casual", **h1["component_offset_context"]["casual_welch"]},
        ]).to_csv(TABLES_DIR / "h1_ttest_workingday.csv", index=False)
        pd.DataFrame(h2["posthoc_comparisons"]).to_csv(TABLES_DIR / "h2_anova_season_posthoc.csv", index=False)
        pd.DataFrame(h3["contingency_table"]).to_csv(TABLES_DIR / "h3_chisq_contingency_table.csv", index=False)

    return {"summary_table": summary_rows, "h1_ttest": h1, "h2_anova": h2, "h3_chisq": h3}
