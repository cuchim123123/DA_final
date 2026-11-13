"""Visualization entry-point delegating to modular `src.plots` subpackage."""

from __future__ import annotations

from typing import Any, Dict, List
import pandas as pd

from src.plots import (
    FIGURES_DIR,
    configure_style,
    plot_fig01_timeseries,
    plot_fig02_cnt_hist_kde,
    plot_fig03_season_boxplot,
    plot_fig04_temp_vs_cnt_scatter,
    plot_fig05_weather_workday_bars,
    plot_fig06_cnt_prob_diagnostics,
    plot_fig07_temp_prob_diagnostics,
    plot_fig08_hum_windspeed_diagnostics,
    plot_fig09_h1_ttest,
    plot_fig10_h2_anova,
    plot_fig11_h3_chisq,
    plot_fig12_pearson_heatmap,
    plot_fig13_spearman_heatmap,
    plot_fig14_scatter_grid,
    plot_fig15_actual_vs_predicted,
    plot_fig16_residuals_vs_fitted,
    plot_fig17_residual_qq_hist,
    plot_fig18_temporal_test_errors,
)


def generate_all_visualizations(
    df: pd.DataFrame,
    prob_res: Dict[str, Any],
    ht_res: Dict[str, Any],
    corr_res: Dict[str, Any],
    reg_res: Dict[str, Any],
) -> List[Dict[str, str]]:
    """Generate all 18 figures (300 DPI) and return their metadata list."""
    configure_style()
    specs = [
        ("Fig 1", "Phase 2 (EDA)", plot_fig01_timeseries(df, reg_res)),
        ("Fig 2", "Phase 2 (EDA)", plot_fig02_cnt_hist_kde(df)),
        ("Fig 3", "Phase 2 (EDA)", plot_fig03_season_boxplot(df)),
        ("Fig 4", "Phase 2 (EDA)", plot_fig04_temp_vs_cnt_scatter(df)),
        ("Fig 5", "Phase 2 (EDA)", plot_fig05_weather_workday_bars(df)),
        ("Fig 6", "Phase 3 (Probability)", plot_fig06_cnt_prob_diagnostics(df, prob_res)),
        ("Fig 7", "Phase 3 (Probability)", plot_fig07_temp_prob_diagnostics(df, prob_res)),
        ("Fig 8", "Phase 3 (Probability)", plot_fig08_hum_windspeed_diagnostics(df, prob_res)),
        ("Fig 9", "Phase 4 (Hypothesis H1)", plot_fig09_h1_ttest(df, ht_res)),
        ("Fig 10", "Phase 4 (Hypothesis H2)", plot_fig10_h2_anova(df, ht_res)),
        ("Fig 11", "Phase 4 (Hypothesis H3)", plot_fig11_h3_chisq(ht_res)),
        ("Fig 12", "Phase 5 (Correlations)", plot_fig12_pearson_heatmap(df)),
        ("Fig 13", "Phase 5 (Correlations)", plot_fig13_spearman_heatmap(df)),
        ("Fig 14", "Phase 5 (Correlations)", plot_fig14_scatter_grid(df, corr_res)),
        ("Fig 15", "Phase 6 (Regression)", plot_fig15_actual_vs_predicted(reg_res)),
        ("Fig 16", "Phase 6 (Regression)", plot_fig16_residuals_vs_fitted(reg_res)),
        ("Fig 17", "Phase 6 (Regression)", plot_fig17_residual_qq_hist(reg_res)),
        ("Fig 18", "Phase 6 (Regression)", plot_fig18_temporal_test_errors(reg_res)),
    ]
    return [
        {"id": fid, "filename": path.split("/")[-1], "path": path, "phase": phase}
        for fid, phase, path in specs
    ]
