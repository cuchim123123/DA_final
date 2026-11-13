"""
Automated Hypothesis Testing Verification Suite (Phase 4).

Verifies H1 (Welch t-test), H2 (One-Way & Welch ANOVA + post-hoc), and H3
(Chi-Square test of independence) for finite statistics, valid p-value bounds,
Cochran expected-frequency checks, effect sizes, and Holm adjustments.
"""

import numpy as np
from src.hypothesis_tests import run_all_hypothesis_tests


def test_statistical_output_validity() -> None:
    """Verify all three hypothesis tests produce valid statistics, p-values, and effect sizes."""
    res = run_all_hypothesis_tests(save_outputs=True)

    # H1 checks
    h1 = res["h1_ttest"]
    p1 = h1["primary_cnt_results"]
    assert p1["n1"] + p1["n0"] == 731
    assert np.isfinite(p1["t_welch"])
    assert 0.0 <= p1["p_value_welch"] <= 1.0
    assert p1["ci95_low"] < p1["mean_diff_1_minus_0"] < p1["ci95_high"]
    assert np.isfinite(p1["hedges_g"])

    # H2 checks
    h2 = res["h2_anova"]
    om2 = h2["omnibus_results"]
    assert sum(g["n"] for g in h2["group_summaries"]) == 731
    assert np.isfinite(om2["f_statistic_ordinary"]) and om2["f_statistic_ordinary"] > 0
    assert np.isfinite(om2["f_statistic_welch"]) and om2["f_statistic_welch"] > 0
    assert 0.0 <= om2["p_value_ordinary_anova"] <= 1.0
    assert 0.0 < om2["eta_squared"] < 1.0
    assert 0.0 < om2["omega_squared"] < 1.0
    assert len(h2["posthoc_comparisons"]) == 6

    # H3 checks
    h3 = res["h3_chisq"]
    om3 = h3["omnibus_results"]
    exp3 = h3["expected_frequency_diagnostics"]
    assert om3["n_total"] == 731
    assert np.isfinite(om3["pearson_chi2"]) and om3["pearson_chi2"] > 0
    assert 0.0 <= om3["p_value_chi2"] <= 1.0
    assert 0.0 < om3["cramers_v"] <= 1.0
    assert exp3["min_expected_cell_count"] >= 5.0
    assert exp3["cochran_criterion_satisfied"] is True

    # Family-wise Holm p-values
    for row in res["summary_table"]:
        assert 0.0 <= row["p_value_holm_adjusted"] <= 1.0
        assert row["p_value_holm_adjusted"] >= row["p_value_unadjusted"] - 1e-12
