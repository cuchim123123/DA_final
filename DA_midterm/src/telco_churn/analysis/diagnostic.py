"""Diagnostic analytics: bivariate tests, effect sizes, Holm correction, and multivariable confounding audit."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from telco_churn.analysis.descriptive import add_derived_analysis_columns
from telco_churn.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES, TABLES_DIR


def _holm_adjust(p_values: list[float]) -> list[float]:
    """Compute Holm-Bonferroni step-down adjusted p-values."""
    m = len(p_values)
    if m == 0:
        return []
    order = np.argsort(p_values)
    adjusted = np.empty(m, dtype=float)
    running_max = 0.0
    for rank, idx in enumerate(order):
        val = (m - rank) * p_values[idx]
        running_max = max(running_max, val)
        adjusted[idx] = min(1.0, running_max)
    return [float(v) for v in adjusted]


def compute_diagnostic_analytics(
    df: pd.DataFrame,
    tables_dir: Path = TABLES_DIR,
    save_tables: bool = True,
) -> dict[str, Any]:
    """Compute categorical Chi-square/Cramer's V tests, continuous comparisons, and confounding checks."""
    df_eda = add_derived_analysis_columns(df)
    y_bin = (df_eda["Churn"] == "Yes").astype(int)

    # 1. Categorical Chi-square tests & Cramer's V
    diag_cat_cols = ["tenure_tier", "SeniorCitizenLabel"] + list(CATEGORICAL_FEATURES)
    cat_rows = []
    for col in diag_cat_cols:
        ctab = pd.crosstab(df_eda[col], df_eda["Churn"])
        chi2, p_val, dof, expected = stats.chi2_contingency(ctab, correction=False)
        n = int(ctab.to_numpy().sum())
        r, c = ctab.shape
        min_dim = max(1, min(r - 1, c - 1))
        cramers_v = float(np.sqrt(chi2 / (n * min_dim))) if n > 0 else 0.0

        # Bias-corrected Cramer's V (Bergsma 2013)
        phi2 = chi2 / n
        phi2_corr = max(0.0, phi2 - ((c - 1) * (r - 1)) / max(1, n - 1))
        r_corr = r - ((r - 1) ** 2) / max(1, n - 1)
        c_corr = c - ((c - 1) ** 2) / max(1, n - 1)
        denom_corr = max(1e-12, min(r_corr - 1, c_corr - 1))
        cramers_v_corr = float(np.sqrt(phi2_corr / denom_corr))

        rates = (ctab["Yes"] / ctab.sum(axis=1) * 100.0).sort_values(ascending=False)
        top_cat = str(rates.index[0])
        top_rate = float(rates.iloc[0])
        low_cat = str(rates.index[-1])
        low_rate = float(rates.iloc[-1])

        strength = (
            "Strong (>= 0.30)"
            if cramers_v >= 0.30
            else "Moderate (0.15 - 0.29)"
            if cramers_v >= 0.15
            else "Weak (0.05 - 0.14)"
            if cramers_v >= 0.05
            else "Negligible (< 0.05)"
        )
        cat_rows.append(
            {
                "feature": col,
                "n_levels": int(r),
                "n_total": n,
                "chi2_stat": round(float(chi2), 4),
                "df": int(dof),
                "p_value": float(p_val),
                "cramers_v": round(cramers_v, 4),
                "cramers_v_corrected": round(cramers_v_corr, 4),
                "min_expected_cell": round(float(expected.min()), 2),
                "highest_churn_group": top_cat,
                "highest_churn_rate_pct": round(top_rate, 2),
                "lowest_churn_group": low_cat,
                "lowest_churn_rate_pct": round(low_rate, 2),
                "rate_spread_pp": round(top_rate - low_rate, 2),
                "association_strength": strength,
            }
        )

    cat_df = pd.DataFrame(cat_rows).sort_values("cramers_v", ascending=False).reset_index(drop=True)
    cat_df["p_value_holm"] = _holm_adjust(cat_df["p_value"].tolist())
    cat_df["significant_holm_0_05"] = cat_df["p_value_holm"] < 0.05

    # 2. Continuous feature group comparisons (Welch t + Mann-Whitney U + Rank-Biserial r)
    cont_rows = []
    for col in NUMERIC_FEATURES:
        x_yes = df_eda.loc[y_bin == 1, col].dropna().astype(float)
        x_no = df_eda.loc[y_bin == 0, col].dropna().astype(float)
        t_stat, t_p = stats.ttest_ind(x_yes, x_no, equal_var=False)
        u_stat, u_p = stats.mannwhitneyu(x_yes, x_no, alternative="two-sided")

        n1, n0 = len(x_yes), len(x_no)
        pooled_sd = float(
            np.sqrt(
                ((n1 - 1) * x_yes.var(ddof=1) + (n0 - 1) * x_no.var(ddof=1))
                / max(1, n1 + n0 - 2)
            )
        )
        cohens_d = float((x_yes.mean() - x_no.mean()) / pooled_sd) if pooled_sd > 0 else 0.0
        # Rank-biserial correlation: +1 if churners always higher, -1 if churners always lower
        rank_biserial = float((2.0 * u_stat) / (n1 * n0) - 1.0)

        cont_rows.append(
            {
                "feature": col,
                "n_churn_yes": n1,
                "n_churn_no": n0,
                "mean_churn_yes": round(float(x_yes.mean()), 2),
                "sd_churn_yes": round(float(x_yes.std(ddof=1)), 2),
                "median_churn_yes": round(float(x_yes.median()), 2),
                "iqr_churn_yes": round(float(x_yes.quantile(0.75) - x_yes.quantile(0.25)), 2),
                "mean_churn_no": round(float(x_no.mean()), 2),
                "sd_churn_no": round(float(x_no.std(ddof=1)), 2),
                "median_churn_no": round(float(x_no.median()), 2),
                "iqr_churn_no": round(float(x_no.quantile(0.75) - x_no.quantile(0.25)), 2),
                "mean_diff_yes_minus_no": round(float(x_yes.mean() - x_no.mean()), 2),
                "welch_t_stat": round(float(t_stat), 4),
                "welch_p_value": float(t_p),
                "mann_whitney_u": round(float(u_stat), 1),
                "mann_whitney_p_value": float(u_p),
                "cohens_d": round(cohens_d, 4),
                "rank_biserial_r": round(rank_biserial, 4),
            }
        )
    cont_df = pd.DataFrame(cont_rows)
    cont_df["mann_whitney_p_holm"] = _holm_adjust(cont_df["mann_whitney_p_value"].tolist())

    # 3. Multivariable confounding diagnostic: unadjusted vs adjusted odds ratios (associative only)
    # Using representative clean non-redundant design to demonstrate confounding on TotalCharges / SeniorCitizen / Streaming
    diag_features = NUMERIC_FEATURES + ["SeniorCitizen"] + list(CATEGORICAL_FEATURES)
    X_diag = df_eda[diag_features]
    preproc = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline([("imp", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]),
                NUMERIC_FEATURES,
            ),
            ("bin", "passthrough", ["SeniorCitizen"]),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), list(CATEGORICAL_FEATURES)),
        ]
    )
    logit_diag = Pipeline(
        [
            ("prep", preproc),
            ("clf", LogisticRegression(C=1.0, max_iter=2000, random_state=42)),
        ]
    )
    logit_diag.fit(X_diag, y_bin)
    feature_names = list(logit_diag.named_steps["prep"].get_feature_names_out())
    coefs = logit_diag.named_steps["clf"].coef_[0]

    # Compare adjusted odds ratios vs unadjusted (marginal) odds ratios on identical transformed columns
    X_mat = logit_diag.named_steps["prep"].transform(X_diag)
    if hasattr(X_mat, "toarray"):
        X_mat = X_mat.toarray()

    conf_rows = []
    for idx, fname in enumerate(feature_names):
        col_vec = X_mat[:, idx]
        adj_log_odds = float(coefs[idx])
        adj_or = float(np.exp(adj_log_odds))

        single_clf = LogisticRegression(C=10.0, max_iter=1000, random_state=42)
        single_clf.fit(col_vec.reshape(-1, 1), y_bin)
        unadj_log_odds = float(single_clf.coef_[0][0])
        unadj_or = float(np.exp(unadj_log_odds))

        sign_flipped = (unadj_log_odds * adj_log_odds) < 0
        conf_rows.append(
            {
                "encoded_term": fname.replace("num__", "").replace("bin__", "").replace("cat__", ""),
                "scale_note": "Per 1 SD increase" if fname.startswith("num__") else "Indicator (1 vs Reference 0)",
                "unadjusted_log_odds": round(unadj_log_odds, 4),
                "unadjusted_odds_ratio": round(unadj_or, 4),
                "adjusted_log_odds": round(adj_log_odds, 4),
                "adjusted_odds_ratio": round(adj_or, 4),
                "direction_reversed_after_control": bool(sign_flipped),
            }
        )
    conf_df = (
        pd.DataFrame(conf_rows)
        .assign(abs_adj=lambda d: d["adjusted_log_odds"].abs())
        .sort_values("abs_adj", ascending=False)
        .drop(columns=["abs_adj"])
        .reset_index(drop=True)
    )

    if save_tables:
        tables_dir.mkdir(parents=True, exist_ok=True)
        cat_df.to_csv(tables_dir / "diagnostic_categorical_associations.csv", index=False)
        cont_df.to_csv(tables_dir / "diagnostic_continuous_comparisons.csv", index=False)
        conf_df.to_csv(tables_dir / "diagnostic_confounding_adjusted_odds.csv", index=False)

    return {
        "categorical_associations": cat_df.to_dict(orient="records"),
        "continuous_comparisons": cont_df.to_dict(orient="records"),
        "confounding_adjusted_odds": conf_df.to_dict(orient="records"),
    }
