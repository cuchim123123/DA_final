"""Phase 3: Probability distribution analysis for discrete counts (`cnt`) and bounded weather variables."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import special, stats

from src.load_validate import TABLES_DIR, compute_series_stats, load_and_validate_data


def _lilliefors_normal_bootstrap(
    x: np.ndarray, n_boot: int = 2000, seed: int = 42
) -> Tuple[float, float]:
    """Compute Lilliefors KS statistic for normality and Monte Carlo parametric bootstrap p-value."""
    n = len(x)
    z_obs = np.sort((x - np.mean(x)) / np.std(x, ddof=1))
    eh, el = np.arange(1, n + 1) / n, np.arange(0, n) / n
    cdf_obs = stats.norm.cdf(z_obs)
    d_obs = float(np.max(np.maximum(np.abs(eh - cdf_obs), np.abs(cdf_obs - el))))

    rng = np.random.default_rng(seed)
    sims = rng.standard_normal((n_boot, n))
    z_sims = np.sort((sims - sims.mean(1, keepdims=True)) / sims.std(1, ddof=1, keepdims=True), axis=1)
    cdf_s = stats.norm.cdf(z_sims)
    d_sims = np.maximum(np.max(np.abs(eh[None, :] - cdf_s), axis=1), np.max(np.abs(cdf_s - el[None, :]), axis=1))
    return round(d_obs, 4), round(float((np.sum(d_sims >= d_obs) + 1.0) / (n_boot + 1.0)), 4)


def _normal_gof(x: np.ndarray) -> Dict[str, Any]:
    """Compute Normal MLE parameters, AIC, and formal normality test statistics."""
    mu, sd = float(np.mean(x)), float(np.std(x, ddof=1))
    ll = float(np.sum(stats.norm.logpdf(x, loc=mu, scale=sd)))
    sw_w, sw_p = stats.shapiro(x)
    k2_s, k2_p = stats.normaltest(x)
    jb_s, jb_p = stats.jarque_bera(x)
    ad = stats.anderson(x, dist="norm", method="interpolate")
    lf_ks, lf_p = _lilliefors_normal_bootstrap(x)
    return {
        "mu_hat": round(mu, 4), "sigma_hat": round(sd, 4),
        "log_likelihood": round(ll, 2), "aic": round(4.0 - 2.0 * ll, 2),
        "shapiro_wilk_stat": round(float(sw_w), 4), "shapiro_wilk_pvalue": float(sw_p),
        "dagostino_k2_stat": round(float(k2_s), 4), "dagostino_k2_pvalue": float(k2_p),
        "jarque_bera_stat": round(float(jb_s), 4), "jarque_bera_pvalue": float(jb_p),
        "anderson_darling_stat": round(float(ad.statistic), 4),
        "anderson_darling_pvalue": round(float(ad.pvalue), 6),
        "lilliefors_ks_stat": lf_ks, "lilliefors_bootstrap_pvalue": lf_p,
    }


def _fit_beta_0_1(x: np.ndarray) -> Dict[str, Any]:
    """Fit Beta(alpha, beta) on [0, 1] via Method of Moments and MLE."""
    xc = np.clip(x, 1e-4, 1.0 - 1e-4)
    m, v = float(np.mean(xc)), float(np.var(xc, ddof=1))
    c = max((m * (1.0 - m) / v) - 1.0, 1e-3)
    a_mle, b_mle, _, _ = stats.beta.fit(xc, floc=0.0, fscale=1.0)
    ll = float(np.sum(stats.beta.logpdf(xc, a=a_mle, b=b_mle, loc=0.0, scale=1.0)))
    ks, _ = stats.ks_1samp(xc, lambda u: stats.beta.cdf(u, a=a_mle, b=b_mle, loc=0.0, scale=1.0))
    return {
        "alpha_mom": round(m * c, 4), "beta_mom": round((1.0 - m) * c, 4),
        "alpha_mle": round(float(a_mle), 4), "beta_mle": round(float(b_mle), 4),
        "log_likelihood": round(ll, 2), "aic": round(4.0 - 2.0 * ll, 2),
        "ks_distance": round(float(ks), 4),
    }


def analyze_cnt_distribution(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze discrete daily count target `cnt` across Poisson, NegBin, Exponential, Gamma, and Normal."""
    st = compute_series_stats(df["cnt"])
    y = df["cnt"].astype(float).to_numpy()
    n, mean_y, var_y = st["n"], float(np.mean(y)), float(np.var(y, ddof=1))
    disp_ratio = var_y / mean_y
    p_chi2 = (n - 1) * disp_ratio

    ct_aux = ((y - mean_y) ** 2 - y) / mean_y
    ct_t = float(np.mean(ct_aux) / (np.std(ct_aux, ddof=1) / np.sqrt(n)))
    p_ll = float(np.sum(stats.poisson.logpmf(np.round(y).astype(int), mu=mean_y)))
    p_ks, _ = stats.ks_1samp(y, lambda u: stats.poisson.cdf(u, mu=mean_y))

    p_nb, r_nb = mean_y / var_y, (mean_y**2) / (var_y - mean_y)
    nb_ll = float(np.sum(
        special.gammaln(y + r_nb) - special.gammaln(r_nb) - special.gammaln(y + 1.0)
        + r_nb * np.log(p_nb) + y * np.log(1.0 - p_nb)
    ))
    nb_ks, _ = stats.ks_1samp(y, lambda u: stats.nbinom.cdf(u, n=r_nb, p=p_nb))

    exp_ll = float(np.sum(stats.expon.logpdf(y, loc=0.0, scale=mean_y)))
    exp_ks, _ = stats.ks_1samp(y, lambda u: stats.expon.cdf(u, loc=0.0, scale=mean_y))

    g_a, _, g_s = stats.gamma.fit(y, floc=0.0)
    gam_ll = float(np.sum(stats.gamma.logpdf(y, a=g_a, loc=0.0, scale=g_s)))
    gam_ks, _ = stats.ks_1samp(y, lambda u: stats.gamma.cdf(u, a=g_a, loc=0.0, scale=g_s))

    norm_diag = _normal_gof(y)
    return {
        "variable": "cnt", "n": n, "mean": st["mean"], "variance": st["variance"],
        "sd": st["sd"], "skewness": st["skewness"], "excess_kurtosis": st["excess_kurtosis"],
        "poisson_diagnostics": {
            "lambda_hat": round(mean_y, 4), "sample_variance": round(var_y, 4),
            "variance_to_mean_ratio_index_of_dispersion": round(disp_ratio, 4),
            "dispersion_chi2_stat": round(p_chi2, 2),
            "dispersion_chi2_pvalue": float(stats.chi2.sf(p_chi2, df=n - 1)),
            "cameron_trivedi_t_stat": round(ct_t, 4),
            "cameron_trivedi_pvalue": float(stats.t.sf(ct_t, df=n - 1)),
            "log_likelihood": round(p_ll, 2), "aic": round(2.0 - 2.0 * p_ll, 2),
            "ks_distance": round(float(p_ks), 4),
        },
        "negative_binomial_diagnostics": {
            "r_dispersion_param": round(r_nb, 4), "p_success_param": round(p_nb, 6),
            "log_likelihood": round(nb_ll, 2), "aic": round(4.0 - 2.0 * nb_ll, 2),
            "ks_distance": round(float(nb_ks), 4),
        },
        "exponential_diagnostics": {
            "scale_mean_param": round(mean_y, 4), "log_likelihood": round(exp_ll, 2),
            "aic": round(2.0 - 2.0 * exp_ll, 2), "ks_distance": round(float(exp_ks), 4),
        },
        "gamma_diagnostics": {
            "shape_alpha": round(float(g_a), 4), "scale_theta": round(float(g_s), 4),
            "log_likelihood": round(gam_ll, 2), "aic": round(4.0 - 2.0 * gam_ll, 2),
            "ks_distance": round(float(gam_ks), 4),
        },
        "normal_approximation_diagnostics": norm_diag,
    }


def analyze_continuous_weather_distribution(df: pd.DataFrame, col: str) -> Dict[str, Any]:
    """Analyze continuous normalized weather variable (`temp`, `hum`, `windspeed`)."""
    st = compute_series_stats(df[col])
    x = df[col].astype(float).to_numpy()
    xp = np.clip(x, 1e-4, None)
    g_a, _, g_s = stats.gamma.fit(xp, floc=0.0)
    gam_ll = float(np.sum(stats.gamma.logpdf(xp, a=g_a, loc=0.0, scale=g_s)))
    gam_ks, _ = stats.ks_1samp(xp, lambda u: stats.gamma.cdf(u, a=g_a, loc=0.0, scale=g_s))

    seasonal_means = {}
    if col == "temp":
        for s in [1, 2, 3, 4]:
            sub = df.loc[df["season"] == s, col].astype(float)
            seasonal_means[f"season_{s}_mean"] = round(float(sub.mean()), 4)
            seasonal_means[f"season_{s}_sd"] = round(float(sub.std(ddof=1)), 4)

    return {
        "variable": col, "n": st["n"], "mean": st["mean"], "sd": st["sd"],
        "variance": st["variance"], "skewness": st["skewness"], "excess_kurtosis": st["excess_kurtosis"],
        "normal_fit": _normal_gof(x),
        "beta_fit_0_1": _fit_beta_0_1(x),
        "gamma_fit": {
            "shape_alpha": round(float(g_a), 4), "scale_theta": round(float(g_s), 4),
            "log_likelihood": round(gam_ll, 2), "aic": round(4.0 - 2.0 * gam_ll, 2),
            "ks_distance": round(float(gam_ks), 4),
        },
        "seasonal_subregimes": seasonal_means,
    }


def run_probability_analysis(
    df: pd.DataFrame | None = None, save_outputs: bool = True
) -> Dict[str, Any]:
    """Execute Phase 3 probability distribution analysis and export summary tables."""
    if df is None:
        df, _ = load_and_validate_data(save_outputs=save_outputs)

    cnt_res = analyze_cnt_distribution(df)
    temp_res = analyze_continuous_weather_distribution(df, "temp")
    hum_res = analyze_continuous_weather_distribution(df, "hum")
    wind_res = analyze_continuous_weather_distribution(df, "windspeed")

    p_d, nb_d, n_d = (
        cnt_res["poisson_diagnostics"],
        cnt_res["negative_binomial_diagnostics"],
        cnt_res["normal_approximation_diagnostics"],
    )
    summary_rows: List[Dict[str, Any]] = [{
        "variable": "cnt", "mean": cnt_res["mean"], "sd": cnt_res["sd"],
        "variance": cnt_res["variance"], "var_to_mean_ratio": p_d["variance_to_mean_ratio_index_of_dispersion"],
        "skewness": cnt_res["skewness"], "excess_kurtosis": cnt_res["excess_kurtosis"],
        "shapiro_w": n_d["shapiro_wilk_stat"], "shapiro_p": n_d["shapiro_wilk_pvalue"],
        "dagostino_k2": n_d["dagostino_k2_stat"], "dagostino_p": n_d["dagostino_k2_pvalue"],
        "lilliefors_ks": n_d["lilliefors_ks_stat"], "lilliefors_boot_p": n_d["lilliefors_bootstrap_pvalue"],
    }]
    for w_res in [temp_res, hum_res, wind_res]:
        nf = w_res["normal_fit"]
        summary_rows.append({
            "variable": w_res["variable"], "mean": w_res["mean"], "sd": w_res["sd"],
            "variance": w_res["variance"], "var_to_mean_ratio": round(w_res["variance"] / w_res["mean"], 4),
            "skewness": w_res["skewness"], "excess_kurtosis": w_res["excess_kurtosis"],
            "shapiro_w": nf["shapiro_wilk_stat"], "shapiro_p": nf["shapiro_wilk_pvalue"],
            "dagostino_k2": nf["dagostino_k2_stat"], "dagostino_p": nf["dagostino_k2_pvalue"],
            "lilliefors_ks": nf["lilliefors_ks_stat"], "lilliefors_boot_p": nf["lilliefors_bootstrap_pvalue"],
        })

    if save_outputs:
        TABLES_DIR.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(summary_rows).to_csv(TABLES_DIR / "probability_distribution_summary.csv", index=False)
        pd.DataFrame([{
            **p_d, "negbin_r": nb_d["r_dispersion_param"], "negbin_p": nb_d["p_success_param"],
            "negbin_loglik": nb_d["log_likelihood"], "negbin_aic": nb_d["aic"],
            "normal_loglik": n_d["log_likelihood"], "normal_aic": n_d["aic"],
        }]).to_csv(TABLES_DIR / "cnt_overdispersion_and_fit.csv", index=False)
        pd.DataFrame([{
            "variable": "temp", "mean": temp_res["mean"], "sd": temp_res["sd"],
            "skewness": temp_res["skewness"], "excess_kurtosis": temp_res["excess_kurtosis"],
            **temp_res["normal_fit"], **{f"beta_{k}": v for k, v in temp_res["beta_fit_0_1"].items()},
            **temp_res["seasonal_subregimes"],
        }]).to_csv(TABLES_DIR / "temp_distribution_diagnostics.csv", index=False)

    return {
        "cnt": cnt_res, "temp": temp_res, "hum": hum_res, "windspeed": wind_res,
        "summary_table": summary_rows,
    }
