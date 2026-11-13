"""Modular scientific visualization package for Phases 2–6 (Figures 1–18)."""

from src.plots.style import FIGURES_DIR, configure_style
from src.plots.eda_plots import (
    plot_fig01_timeseries,
    plot_fig02_cnt_hist_kde,
    plot_fig03_season_boxplot,
    plot_fig04_temp_vs_cnt_scatter,
    plot_fig05_weather_workday_bars,
)
from src.plots.prob_hypos_plots import (
    plot_fig06_cnt_prob_diagnostics,
    plot_fig07_temp_prob_diagnostics,
    plot_fig08_hum_windspeed_diagnostics,
    plot_fig09_h1_ttest,
    plot_fig10_h2_anova,
    plot_fig11_h3_chisq,
)
from src.plots.corr_reg_plots import (
    plot_fig12_pearson_heatmap,
    plot_fig13_spearman_heatmap,
    plot_fig14_scatter_grid,
    plot_fig15_actual_vs_predicted,
    plot_fig16_residuals_vs_fitted,
    plot_fig17_residual_qq_hist,
    plot_fig18_temporal_test_errors,
)

__all__ = [
    "FIGURES_DIR",
    "configure_style",
    "plot_fig01_timeseries",
    "plot_fig02_cnt_hist_kde",
    "plot_fig03_season_boxplot",
    "plot_fig04_temp_vs_cnt_scatter",
    "plot_fig05_weather_workday_bars",
    "plot_fig06_cnt_prob_diagnostics",
    "plot_fig07_temp_prob_diagnostics",
    "plot_fig08_hum_windspeed_diagnostics",
    "plot_fig09_h1_ttest",
    "plot_fig10_h2_anova",
    "plot_fig11_h3_chisq",
    "plot_fig12_pearson_heatmap",
    "plot_fig13_spearman_heatmap",
    "plot_fig14_scatter_grid",
    "plot_fig15_actual_vs_predicted",
    "plot_fig16_residuals_vs_fitted",
    "plot_fig17_residual_qq_hist",
    "plot_fig18_temporal_test_errors",
]
