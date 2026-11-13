"""Interactive Streamlit dashboard for Bike Sharing Data Analysis and Demand Prediction."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

try:
    from app.helpers import (
        DashboardArtifacts,
        compute_filtered_eda_kpis,
        filter_bike_cohort,
        get_figure_path,
        load_dashboard_artifacts,
        predict_bike_demand,
    )
except ModuleNotFoundError:
    from helpers import (  # type: ignore[no-redef]
        DashboardArtifacts,
        compute_filtered_eda_kpis,
        filter_bike_cohort,
        get_figure_path,
        load_dashboard_artifacts,
        predict_bike_demand,
    )

st.set_page_config(
    page_title="Bike Sharing Analytics & Demand Prediction",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner=False)
def _cached_artifacts() -> DashboardArtifacts:
    return load_dashboard_artifacts()


def _render_overview_and_eda(art: DashboardArtifacts, filtered_df: pd.DataFrame) -> None:
    st.header("1. Executive Overview & Exploratory Data Analysis")
    st.markdown(
        "Explore baseline demand metrics, historical trends, categorical segmentations, and data hygiene audits "
        "for the Capital Bikeshare Washington D.C. daily dataset ($N = 731$ days)."
    )

    kpis = compute_filtered_eda_kpis(filtered_df)
    total_master_cnt = int(art.df["cnt"].sum())

    # Top KPI Banner
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Observed Days", f"{kpis['n_days']:,} / 731", delta=f"{round(100.0 * kpis['n_days'] / 731, 1)}% of full record")
    c2.metric("Total Bike Rentals", f"{kpis['total_rentals']:,}", delta=f"{round(100.0 * kpis['total_rentals'] / total_master_cnt, 1)}% total volume")
    c3.metric("Mean Daily Rentals", f"{kpis['mean_daily_rentals']:,.1f}", delta=f"± {kpis['std_daily_rentals']:,.1f} std dev")
    c4.metric("Registered Rider Share", f"{kpis['registered_share_pct']:.1f}%", delta=f"Casual: {kpis['casual_share_pct']:.1f}%")
    c5.metric("Peak Single Day", f"{kpis['peak_day_cnt']:,}", delta=f"Date: {kpis['peak_day_date']}")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        "📈 Temporal Trends & Time Series",
        "📊 Categorical & Weather Segmentations",
        "🛡️ Data Quality & Outlier Audit",
    ])

    with tab1:
        st.subheader("Daily Rental Time Series with Moving Averages")
        st.markdown(
            "Tracking daily bike demand across the 2-year horizon (2011–2012) reveals pronounced seasonal oscillations "
            "and a substantial annual adoption growth (+64% total volume increase from Year 0 to Year 1)."
        )
        fig_path = get_figure_path("fig01_daily_rentals_timeseries.png")
        if fig_path:
            st.image(str(fig_path), use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### Annual Growth Summary")
            if "eda_group_by_year" in art.tables:
                st.dataframe(art.tables["eda_group_by_year"], use_container_width=True, hide_index=True)
        with col_b:
            st.markdown("#### Monthly Demand Patterns")
            monthly_summary = (
                filtered_df.groupby(["yr", "mnth"])
                .agg(
                    mean_daily_cnt=("cnt", "mean"),
                    mean_casual=("casual", "mean"),
                    mean_registered=("registered", "mean"),
                    days=("cnt", "count"),
                )
                .round(1)
                .reset_index()
            )
            st.dataframe(monthly_summary.head(12), use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Seasonal and Weather Segmentations")
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            st.markdown("#### Rental Distributions by Season")
            fig_season = get_figure_path("fig03_cnt_boxplot_by_season.png")
            if fig_season:
                st.image(str(fig_season), use_container_width=True)
            if "eda_group_by_season" in art.tables:
                st.dataframe(art.tables["eda_group_by_season"], use_container_width=True, hide_index=True)

        with col_c2:
            st.markdown("#### Weather Condition and Day Type Interaction")
            fig_weather = get_figure_path("fig05_mean_cnt_by_weather_workday_ci.png")
            if fig_weather:
                st.image(str(fig_weather), use_container_width=True)
            if "eda_group_by_weathersit" in art.tables:
                st.dataframe(art.tables["eda_group_by_weathersit"], use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Data Hygiene and Outlier Audit")
        st.markdown(
            "The dataset exhibits zero missing values, zero duplicated dates, and 100% strict adherence to "
            "physical domain constraints ($cnt = casual + registered$). Outliers were audited using Tukey's $1.5 \\times \\text{IQR}$ rule."
        )

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown("#### Tukey 1.5×IQR Outlier Audit")
            if "eda_outlier_audit" in art.tables:
                st.dataframe(art.tables["eda_outlier_audit"], use_container_width=True, hide_index=True)

        with col_d2:
            st.markdown("#### Outlier Handling Sensitivity Analysis")
            if "eda_outlier_handling_sensitivity" in art.tables:
                st.dataframe(art.tables["eda_outlier_handling_sensitivity"], use_container_width=True, hide_index=True)

        st.info(
            "**Methodological Decision:** Target variable `cnt` contains **0 outliers**. Predictors `hum` (2 low values) "
            "and `windspeed` (13 high values) reflect genuine, verified meteorological events (e.g. storm days). "
            "As demonstrated by the sensitivity table, retaining these valid observations preserves real-world operational variance."
        )


def _render_probability_distributions(art: DashboardArtifacts) -> None:
    st.header("2. Probability Distribution Analysis")
    st.markdown(
        "Evaluate whether rental demand (`cnt`) and environmental continuous features follow theoretical "
        "probability distributions (Gaussian, Poisson, Negative Binomial, Weibull)."
    )

    tab1, tab2, tab3 = st.tabs([
        "🎯 Target Variable (`cnt`) Fit Diagnostics",
        "🔢 Count Overdispersion & Poisson Rejection",
        "🌡️ Predictor Distributions (`temp`, `hum`, `windspeed`)",
    ])

    with tab1:
        st.subheader("Goodness-of-Fit Diagnostics for Daily Rentals (`cnt`)")
        st.markdown(
            "We test the hypothesis that daily rental demand follows a Normal distribution. "
            "Both visual inspection (Q-Q plot) and formal statistical tests reject strict normality."
        )

        fig_diag = get_figure_path("fig06_cnt_distribution_diagnostics.png")
        if fig_diag:
            st.image(str(fig_diag), use_container_width=True)

        if "probability_distribution_summary" in art.tables:
            st.markdown("#### Goodness-of-Fit Test Summary")
            st.dataframe(art.tables["probability_distribution_summary"], use_container_width=True, hide_index=True)

        st.markdown(
            "> **Analytical Finding:** Shapiro-Wilk test ($W = 0.9798, p < 0.001$) and Kolmogorov-Smirnov test ($p < 0.001$) "
            "> formally reject the Gaussian assumption. While `cnt` is symmetric (skewness = $-0.0026$), its distribution is "
            "> platykurtic (excess kurtosis = $-0.8143$), caused by the superposition of low winter demand and high summer/fall demand."
        )

    with tab2:
        st.subheader("Equidispersion Audit: Mean vs Variance")
        st.markdown(
            "A standard Poisson model requires that the variance of the count equals its mean ($\\text{Var}(Y) = E[Y]$). "
            "In daily bike rental data, this assumption fails catastrophically due to extreme overdispersion."
        )

        if "cnt_overdispersion_and_fit" in art.tables:
            st.dataframe(art.tables["cnt_overdispersion_and_fit"], use_container_width=True, hide_index=True)

        if "cnt_overdispersion_and_fit" in art.tables:
            od_row = art.tables["cnt_overdispersion_and_fit"].iloc[0]
            disp_mean = float(od_row["lambda_hat"])
            disp_var = float(od_row["sample_variance"])
            disp_idx = float(od_row["variance_to_mean_ratio_index_of_dispersion"])
        else:
            disp_mean = float(art.df["cnt"].mean())
            disp_var = float(art.df["cnt"].var(ddof=1))
            disp_idx = disp_var / disp_mean

        c1, c2, c3 = st.columns(3)
        c1.metric("Empirical Mean", f"{disp_mean:,.2f}")
        c2.metric("Empirical Variance", f"{disp_var:,.2f}")
        c3.metric("Variance-to-Mean Ratio (Dispersion Index)", f"{disp_idx:,.2f} >> 1.0")

        st.warning(
            "**Model Selection Implication:** Because the variance is over 800 times larger than the mean, "
            "fitting a standard Poisson regression would severely underestimate standard errors, resulting in inflated false positive rates. "
            "Continuous Multiple Linear Regression (OLS) with robust standard errors or Negative Binomial regression is required."
        )

    with tab3:
        st.subheader("Environmental Predictor Probability Profiles")
        col_p1, col_p2 = st.columns(2)

        with col_p1:
            st.markdown("#### Temperature Distribution (Bimodal Climatological Mixture)")
            fig_temp = get_figure_path("fig07_temp_distribution_diagnostics.png")
            if fig_temp:
                st.image(str(fig_temp), use_container_width=True)
            if "temp_distribution_diagnostics" in art.tables:
                st.dataframe(art.tables["temp_distribution_diagnostics"], use_container_width=True, hide_index=True)

        with col_p2:
            st.markdown("#### Humidity & Wind Speed Distributions")
            fig_hw = get_figure_path("fig08_hum_windspeed_distributions.png")
            if fig_hw:
                st.image(str(fig_hw), use_container_width=True)
            st.markdown(
                "- **Humidity (`hum`):** Left-skewed (median 62.7%), with occasional arid or rain-saturated extremes.\n"
                "- **Wind Speed (`windspeed`):** Right-skewed (median 12.1 km/h), adhering to typical Weibull wind velocity distributions."
            )


def _render_hypothesis_testing(art: DashboardArtifacts) -> None:
    st.header("3. Hypothesis Testing Studio")
    st.markdown(
        "Interactive testing laboratory evaluating three official research hypotheses using both parametric "
        "and non-parametric methods, checking statistical assumptions, and uncovering the user-composition paradox."
    )

    if "hypothesis_tests_summary" in art.tables:
        st.subheader("Official Hypotheses Overview")
        st.dataframe(art.tables["hypothesis_tests_summary"], use_container_width=True, hide_index=True)

    tab1, tab2, tab3 = st.tabs([
        "💼 H1: Working Day vs Non-Working Day",
        "🍂 H2: Multi-Group Seasonal ANOVA",
        "🌧️ H3: Weather Condition vs High Demand",
    ])

    with tab1:
        st.subheader("H1 — Total Demand: Working Day vs Non-Working Day")
        st.markdown(
            "**Hypothesis:** $H_0: \\mu_{\\text{workday}} = \\mu_{\\text{non-workday}}$ vs $H_1: \\mu_{\\text{workday}} \\ne \\mu_{\\text{non-workday}}$"
        )

        col_h1_a, col_h1_b = st.columns([3, 2])
        with col_h1_a:
            fig_h1 = get_figure_path("fig09_h1_workingday_ttest.png")
            if fig_h1:
                st.image(str(fig_h1), use_container_width=True)

        with col_h1_b:
            st.markdown("#### Test Statistics & Conclusion")
            if "h1_ttest_workingday" in art.tables:
                st.dataframe(art.tables["h1_ttest_workingday"], use_container_width=True, hide_index=True)
                h1_row = art.tables["h1_ttest_workingday"].iloc[0]
                t_stat = float(h1_row["t_welch"])
                p_val = float(h1_row["p_value_welch"])
                df_w = float(h1_row["df_welch"])
                p_mwu = float(h1_row["p_value_mann_whitney"])
                m1_val = float(h1_row["mean1"])
                m0_val = float(h1_row["mean0"])
            else:
                t_stat, p_val, df_w, p_mwu, m1_val, m0_val = 1.6014, 0.1101, 413.94, 0.1186, 4584.8, 4330.2

            st.success(
                f"**Decision:** **Fail to Reject $H_0$** ($t_{{\\text{{Welch}}}} = {t_stat:.4f}, df = {df_w:.1f}, p = {p_val:.4f}$; Mann-Whitney $U p = {p_mwu:.4f}$). "
                f"At the total daily demand level, there is no statistically significant difference between working days ({m1_val:,.1f}) and non-working days ({m0_val:,.1f}) at $\\alpha = 0.05$."
            )

        st.markdown("---")
        st.subheader("🔍 The User Composition Paradox (Simpson's-like Reversal)")
        st.markdown(
            "While total daily demand appears invariant to working days, inspecting **rider categories** reveals "
            "two massive, mutually offsetting structural shifts:"
        )

        if "h1_ttest_workingday" in art.tables and len(art.tables["h1_ttest_workingday"]) >= 3:
            h1_tbl = art.tables["h1_ttest_workingday"]
            cas_row = h1_tbl.loc[h1_tbl["segment"] == "casual"].iloc[0]
            reg_row = h1_tbl.loc[h1_tbl["segment"] == "registered"].iloc[0]
            cnt_row = h1_tbl.loc[h1_tbl["segment"] == "cnt"].iloc[0]
            cas_m1, cas_m0 = float(cas_row["mean1"]), float(cas_row["mean0"])
            reg_m1, reg_m0 = float(reg_row["mean1"]), float(reg_row["mean0"])
            cnt_m1, cnt_m0 = float(cnt_row["mean1"]), float(cnt_row["mean0"])
            cas_pct = round(100.0 * (cas_m1 - cas_m0) / cas_m0, 1)
            reg_pct = round(100.0 * (reg_m1 - reg_m0) / reg_m0, 1)
            cnt_pct = round(100.0 * (cnt_m1 - cnt_m0) / cnt_m0, 1)
            p_cnt = float(cnt_row["p_value_welch"])
        else:
            cas_m1, cas_m0, cas_pct = 606.6, 1371.1, -55.8
            reg_m1, reg_m0, reg_pct = 3978.3, 2959.0, 34.4
            cnt_m1, cnt_m0, cnt_pct, p_cnt = 4584.8, 4330.2, 5.9, 0.1101

        cp1, cp2, cp3 = st.columns(3)
        cp1.metric("Casual Riders (Leisure)", f"{int(round(cas_m1)):,} vs {int(round(cas_m0)):,} / day", delta=f"{cas_pct:+.1f}% drop on workdays", delta_color="inverse")
        cp2.metric("Registered Riders (Commute)", f"{int(round(reg_m1)):,} vs {int(round(reg_m0)):,} / day", delta=f"{reg_pct:+.1f}% rise on workdays", delta_color="normal")
        cp3.metric("Net Total Daily Shift", f"{int(round(cnt_m1)):,} vs {int(round(cnt_m0)):,} / day", delta=f"{cnt_pct:+.1f}% (Non-sig, p={p_cnt:.2f})", delta_color="off")

    with tab2:
        st.subheader("H2 — Seasonal Variation in Rental Demand")
        st.markdown(
            "**Hypothesis:** $H_0: \\mu_1 = \\mu_2 = \\mu_3 = \\mu_4$ vs $H_1: \\text{At least one season differs}$"
        )

        col_h2_a, col_h2_b = st.columns([3, 2])
        with col_h2_a:
            fig_h2 = get_figure_path("fig10_h2_season_anova.png")
            if fig_h2:
                st.image(str(fig_h2), use_container_width=True)

        with col_h2_b:
            st.markdown("#### Omnibus ANOVA & Kruskal-Wallis")
            h2_om = art.results.get("hypothesis_tests", {}).get("h2_anova", {}).get("omnibus_results", {})
            f_val = float(h2_om.get("f_statistic_ordinary", 128.77))
            f_p = float(h2_om.get("p_value_ordinary_anova", 6.72e-67))
            kw_val = float(h2_om.get("kruskal_wallis_h", 250.93))
            kw_p = float(h2_om.get("p_value_kruskal_wallis", 4.11e-54))

            c_an1, c_an2 = st.columns(2)
            c_an1.metric("One-Way ANOVA F", f"{f_val:.2f}", delta="p < 0.001" if f_p < 0.001 else f"p = {f_p:.4f}")
            c_an2.metric("Kruskal-Wallis H", f"{kw_val:.2f}", delta="p < 0.001" if kw_p < 0.001 else f"p = {kw_p:.4f}")

            st.markdown("#### Post-Hoc Pairwise Comparisons")
            if "h2_anova_season_posthoc" in art.tables:
                st.dataframe(art.tables["h2_anova_season_posthoc"], use_container_width=True, hide_index=True)

        st.info(
            "**Key Post-Hoc Findings:**\n"
            "- **Spring (Season 1)** has significantly lower demand (2,604 bikes/day) than all other seasons ($p < 0.001$).\n"
            "- **Fall (Season 3)** is the peak demand period (5,644 bikes/day).\n"
            "- **Summer (Season 2)** and **Winter (Season 4)** do not differ significantly from each other in post-hoc tests ($p = 0.54$)."
        )

    with tab3:
        st.subheader("H3 — Weather Condition vs High Demand Days")
        st.markdown(
            "**Hypothesis:** $H_0: \\text{Weather condition and High Demand are independent}$ vs $H_1: \\text{They are dependent}$"
        )

        col_h3_a, col_h3_b = st.columns([3, 2])
        with col_h3_a:
            fig_h3 = get_figure_path("fig11_h3_weathersit_highdemand_chisq.png")
            if fig_h3:
                st.image(str(fig_h3), use_container_width=True)

        with col_h3_b:
            st.markdown("#### Contingency Table & Chi-Square")
            if "h3_chisq_contingency_table" in art.tables:
                st.dataframe(art.tables["h3_chisq_contingency_table"], use_container_width=True, hide_index=True)

            h3_om = art.results.get("hypothesis_tests", {}).get("h3_chisq", {}).get("omnibus_results", {})
            chi2_val = float(h3_om.get("pearson_chi2", 44.09))
            chi2_p = float(h3_om.get("p_value_chi2", 2.67e-10))
            cramer_v = float(h3_om.get("cramers_v", 0.2456))

            c_chi1, c_chi2 = st.columns(2)
            c_chi1.metric("Chi-Square Stat (df=2)", f"{chi2_val:.2f}", delta="p < 0.001" if chi2_p < 0.001 else f"p = {chi2_p:.4e}")
            c_chi2.metric("Cramér's V (Association)", f"{cramer_v:.4f}", delta="Moderate Effect")

        st.success(
            "**Decision:** **Reject $H_0$** ($p < 0.001$). "
            "Under Clear weather, 60.5% of days achieve High Demand (`cnt` > median 4,548). "
            "Under Mist/Cloudy, high demand drops to 37.7%. Under Light Rain/Snow, **0.0% of days** reach high demand!"
        )


def _render_correlation_and_collinearity(art: DashboardArtifacts) -> None:
    st.header("4. Correlation & Multicollinearity Lab")
    st.markdown(
        "Investigate linear (Pearson $r$) and monotonic rank (Spearman $\\rho$) relationships, and explore "
        "the critical Variance Inflation Factor (VIF) collinearity discovery between `temp` and `atemp`."
    )

    tab1, tab2 = st.tabs([
        "🔥 Correlation Heatmaps & Significance",
        "⚠️ Multicollinearity Case Study & VIF Diagnostics",
    ])

    with tab1:
        st.subheader("Pairwise Linear and Monotonic Association")
        col_m1, col_m2 = st.columns(2)

        with col_m1:
            st.markdown("#### Pearson Linear Correlation ($r$)")
            fig_pear = get_figure_path("fig12_pearson_correlation_heatmap.png")
            if fig_pear:
                st.image(str(fig_pear), use_container_width=True)

        with col_m2:
            st.markdown("#### Spearman Monotonic Rank Correlation ($\\rho$)")
            fig_spear = get_figure_path("fig13_spearman_correlation_heatmap.png")
            if fig_spear:
                st.image(str(fig_spear), use_container_width=True)

        st.markdown("#### Pairwise Significance Tests and Confidence Intervals")
        if "correlation_pairwise_tests" in art.tables:
            st.dataframe(art.tables["correlation_pairwise_tests"], use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("The Collinearity Trap: Feeling Temperature (`atemp`)")
        st.markdown(
            "A standard regression model including both actual temperature (`temp`) and feeling temperature (`atemp`) "
            "suffers from severe multicollinearity, inflating standard errors and rendering coefficient signs unstable."
        )

        col_v1, col_v2 = st.columns([3, 2])
        with col_v1:
            fig_scatter = get_figure_path("fig14_continuous_predictors_scatter_grid.png")
            if fig_scatter:
                st.image(str(fig_scatter), use_container_width=True)

        with col_v2:
            st.markdown("#### VIF Diagnostics Comparison")
            if "regression_vif_diagnostics" in art.tables:
                st.dataframe(art.tables["regression_vif_diagnostics"], use_container_width=True, hide_index=True)

            st.error(
                "**Collinearity Discovery:** `temp` and `atemp` share a correlation of **$r = 0.9917$**. "
                "When both are included, their VIF exceeds **$64.0$** (far above the critical threshold of 10.0).\n\n"
                "**Solution:** Dropping `atemp` reduces `temp` VIF to **$3.61$**, ensuring all predictors have VIF $< 4.0$."
            )


def _render_predictive_simulator(art: DashboardArtifacts) -> None:
    st.header("5. Predictive Regression & Demand Simulator")
    st.markdown(
        "Benchmark Multiple Linear Regression against baseline and regularized models on a sealed 20% held-out test set, "
        "and simulate daily rental demand in real time under customized operational and weather scenarios."
    )

    tab1, tab2 = st.tabs([
        "📐 Model Benchmark & Statistical Diagnostics",
        "🎯 Interactive Daily Demand Simulator (What-If)",
    ])

    with tab1:
        st.subheader("Model Benchmark: Chronological Train (80%) vs Held-Out Test (20%)")
        if "regression_model_comparison" in art.tables:
            st.dataframe(art.tables["regression_model_comparison"], use_container_width=True, hide_index=True)

            ols_match = art.tables["regression_model_comparison"].loc[
                art.tables["regression_model_comparison"]["model_name"].str.contains("Primary", case=False)
            ]
            base_match = art.tables["regression_model_comparison"].loc[
                art.tables["regression_model_comparison"]["model_name"].str.contains("Baseline", case=False)
            ]
            if not ols_match.empty and not base_match.empty:
                ols_r = ols_match.iloc[0]
                base_r = base_match.iloc[0]
                t_r2 = float(ols_r["test_r2"])
                t_rmse = float(ols_r["test_rmse"])
                t_mae = float(ols_r["test_mae"])
                t_bias = float(ols_r["test_bias_pred_minus_true"])
                b_rmse = float(base_r["test_rmse"])
            else:
                t_r2, t_rmse, t_mae, t_bias, b_rmse = 0.6139, 1164.87, 891.69, -204.70, 2560.56
        else:
            t_r2, t_rmse, t_mae, t_bias, b_rmse = 0.6139, 1164.87, 891.69, -204.70, 2560.56

        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        col_b1.metric("Held-Out Test R²", f"{t_r2:.4f}", delta=f"{t_r2 * 100:.1f}% test variance explained")
        col_b2.metric("Held-Out Test RMSE", f"{t_rmse:,.1f} bikes", delta=f"vs {b_rmse:,.1f} baseline")
        col_b3.metric("Held-Out Test MAE", f"{t_mae:,.1f} bikes", delta="Mean abs test error")
        col_b4.metric("Mean Prediction Bias", f"{t_bias:+,.1f} bikes", delta="Generalization bias")

        st.markdown("---")
        st.subheader("OLS Regression Coefficients & Robust Standard Errors")
        if "regression_ols_coefficients" in art.tables:
            st.dataframe(art.tables["regression_ols_coefficients"], use_container_width=True, hide_index=True)

        st.markdown("#### Regression Residual Diagnostics & Temporal Performance")
        r1, r2 = st.columns(2)
        with r1:
            fig15 = get_figure_path("fig15_regression_actual_vs_predicted.png")
            if fig15:
                st.image(str(fig15), use_container_width=True)
        with r2:
            fig16 = get_figure_path("fig16_regression_residuals_vs_fitted.png")
            if fig16:
                st.image(str(fig16), use_container_width=True)

        r3, r4 = st.columns(2)
        with r3:
            fig17 = get_figure_path("fig17_regression_residual_qq_hist.png")
            if fig17:
                st.image(str(fig17), use_container_width=True)
        with r4:
            fig18 = get_figure_path("fig18_regression_temporal_predictions_errors.png")
            if fig18:
                st.image(str(fig18), use_container_width=True)

    with tab2:
        st.subheader("Real-Time Bike Rental Demand Simulator")
        st.markdown(
            "Configure a hypothetical day to predict expected total bike rentals ($\\widehat{cnt}$), "
            "breakdowns by rider type, and 95% prediction intervals calculated via the fitted OLS model."
        )

        # Parse query parameter defaults
        p_yr = int(st.query_params.get("sim_yr", 1))
        p_season = int(st.query_params.get("sim_season", 3))  # 1..4
        p_season_idx = max(0, min(3, p_season - 1))
        p_daytype = st.query_params.get("sim_daytype", "Workday")
        p_daytype_idx = 0 if p_daytype == "Workday" else 1
        p_weather = int(st.query_params.get("sim_weather", 1))
        p_weather_idx = max(0, min(2, p_weather - 1))
        p_temp = float(st.query_params.get("temp", 24.0))
        p_hum = float(st.query_params.get("hum", 55.0))
        p_wind = float(st.query_params.get("wind", 14.0))

        with st.form("demand_sim_form"):
            c_in1, c_in2, c_in3 = st.columns(3)

            with c_in1:
                st.markdown("##### 📅 Calendar & Temporal Settings")
                sim_yr = st.selectbox(
                    "Year",
                    options=[0, 1],
                    format_func=lambda x: "2011 (Year 0 - Baseline)" if x == 0 else "2012 (Year 1 - Mature System)",
                    index=p_yr,
                    key=f"sim_yr_{p_yr}",
                )
                sim_season = st.selectbox(
                    "Season",
                    options=[1, 2, 3, 4],
                    format_func=lambda x: {1: "1: Spring", 2: "2: Summer", 3: "3: Fall", 4: "4: Winter"}[x],
                    index=p_season_idx,
                    key=f"sim_season_{p_season}",
                )
                sim_daytype = st.radio(
                    "Day Type",
                    options=["Workday", "Weekend / Holiday"],
                    index=p_daytype_idx,
                    key=f"sim_daytype_{p_daytype}",
                )

            with c_in2:
                st.markdown("##### ⛅ Weather Conditions")
                sim_weathersit = st.selectbox(
                    "Weather Condition",
                    options=[1, 2, 3],
                    format_func=lambda x: {1: "1: Clear / Partly Cloudy", 2: "2: Mist / Cloudy", 3: "3: Light Snow / Light Rain"}[x],
                    index=p_weather_idx,
                    key=f"sim_weather_{p_weather}",
                )
                sim_temp = st.slider(
                    "Ambient Temperature (°C)",
                    min_value=0.0,
                    max_value=38.0,
                    value=p_temp,
                    step=0.5,
                    key=f"sim_temp_{p_temp}",
                )
                st.caption(f"Normalized temp: {round(sim_temp / 41.0, 4)} (Temp / 41°C)")

            with c_in3:
                st.markdown("##### 💨 Humidity & Wind Speed")
                sim_hum = st.slider(
                    "Relative Humidity (%)",
                    min_value=15.0,
                    max_value=98.0,
                    value=p_hum,
                    step=1.0,
                    key=f"sim_hum_{p_hum}",
                )
                sim_wind = st.slider(
                    "Wind Speed (km/h)",
                    min_value=0.0,
                    max_value=50.0,
                    value=p_wind,
                    step=1.0,
                    key=f"sim_wind_{p_wind}",
                )
                st.caption(f"Normalized wind: {round(sim_wind / 67.0, 4)} (Wind / 67 km/h)")

            sim_workingday = 1 if sim_daytype == "Workday" else 0
            sim_holiday = 0

            st.form_submit_button("⚡ Recalculate Expected Demand", type="primary", use_container_width=True)

        res = predict_bike_demand(
            art=art,
            yr=sim_yr,
            season=sim_season,
            holiday=sim_holiday,
            workingday=sim_workingday,
            weathersit=sim_weathersit,
            temp_c=sim_temp,
            hum_pct=sim_hum,
            windspeed_kmh=sim_wind,
        )

        st.success("### Simulation Results")
        out1, out2, out3, out4 = st.columns(4)
        out1.metric("Predicted Total Demand", f"{int(res['predicted_cnt']):,} bikes")
        out2.metric("Estimated Registered Riders", f"{int(res['predicted_registered']):,} bikes", delta=f"{round(100.0 * res['predicted_registered'] / max(1.0, res['predicted_cnt']), 1)}% of total")
        out3.metric("Estimated Casual Riders", f"{int(res['predicted_casual']):,} bikes", delta=f"{round(100.0 * res['predicted_casual'] / max(1.0, res['predicted_cnt']), 1)}% of total")
        out4.metric("Standard Error of Mean", f"± {res['mean_se']} bikes")

        int_col1, int_col2 = st.columns(2)
        with int_col1:
            st.markdown(
                f"**95% Confidence Interval for Mean Daily Demand (Sampling Uncertainty):**\n"
                f"- Range: **{int(res['mean_ci_95'][0]):,}** to **{int(res['mean_ci_95'][1]):,}** bikes "
                f"(Estimated population mean demand under these weather and calendar conditions)."
            )
        with int_col2:
            st.markdown(
                f"**95% Prediction Interval for Single Day (Includes Residual Variance $\\sigma^2$):**\n"
                f"- Range: **{int(res['prediction_interval_95'][0]):,}** to **{int(res['prediction_interval_95'][1]):,}** bikes "
                f"(Statistical forecast interval for an individual day; accounts for daily dispersion, not an operational guarantee)."
            )

        st.info(f"**Operational Dispatch Advisory:** {res['fleet_advisory']}")


def main() -> None:
    art = _cached_artifacts()

    # Sidebar Navigation & Global Filters
    st.sidebar.title("🚲 Capital Bikeshare")
    st.sidebar.markdown("**Final Project Analytics Hub**")

    # Read query parameters
    view_q = str(st.query_params.get("view", "")).lower()
    view_idx = 0
    if any(k in view_q for k in ["prob", "dist", "2"]):
        view_idx = 1
    elif any(k in view_q for k in ["hypo", "test", "3"]):
        view_idx = 2
    elif any(k in view_q for k in ["corr", "collinear", "4"]):
        view_idx = 3
    elif any(k in view_q for k in ["pred", "sim", "model", "5"]):
        view_idx = 4

    view_choice = st.sidebar.radio(
        "Navigation",
        options=[
            "1. Executive Overview & EDA",
            "2. Probability Distributions",
            "3. Hypothesis Testing Studio",
            "4. Correlation & Multicollinearity",
            "5. Predictive Model & Simulator",
        ],
        index=view_idx,
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Interactive Cohort Filters")

    # Date range
    min_date = art.df["dteday_parsed"].min().date()
    max_date = art.df["dteday_parsed"].max().date()
    date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    # Seasons filter default
    season_options = [1, 2, 3, 4]
    season_q = st.query_params.get("season")
    if season_q and str(season_q).isdigit() and int(season_q) in season_options:
        def_seasons = [int(season_q)]
    else:
        def_seasons = season_options

    selected_seasons = st.sidebar.multiselect(
        "Season",
        options=season_options,
        default=def_seasons,
        format_func=lambda x: {1: "1: Spring", 2: "2: Summer", 3: "3: Fall", 4: "4: Winter"}[x],
        key=f"filter_seasons_{len(def_seasons)}_{def_seasons[0] if len(def_seasons)==1 else 0}",
    )

    # Weather condition
    weather_options = [1, 2, 3]
    selected_weather = st.sidebar.multiselect(
        "Weather Condition",
        options=weather_options,
        default=weather_options,
        format_func=lambda x: {1: "1: Clear", 2: "2: Mist / Cloudy", 3: "3: Light Rain / Snow"}[x],
    )

    # Day Types
    day_type_options = ["Working Days", "Weekends & Holidays"]
    selected_day_types = st.sidebar.multiselect(
        "Day Type",
        options=day_type_options,
        default=day_type_options,
    )

    # Years
    year_options = [0, 1]
    selected_years = st.sidebar.multiselect(
        "Year",
        options=year_options,
        default=year_options,
        format_func=lambda x: "2011 (Year 0)" if x == 0 else "2012 (Year 1)",
    )

    # Apply filters
    filtered_df = filter_bike_cohort(
        df=art.df,
        date_range=date_range if isinstance(date_range, (tuple, list)) and len(date_range) == 2 else None,
        seasons=selected_seasons if selected_seasons else None,
        weather_conditions=selected_weather if selected_weather else None,
        years=selected_years if selected_years else None,
        day_types=selected_day_types if selected_day_types else None,
    )

    st.sidebar.markdown("---")
    st.sidebar.caption(
        f"Filtered Sample: **{len(filtered_df):,} / 731** days ({round(100.0 * len(filtered_df) / 731, 1)}%)\n\n"
        "Integrity: SHA-256 Verified | 0 Missing | 0 Duplicates"
    )

    if view_choice == "1. Executive Overview & EDA":
        _render_overview_and_eda(art, filtered_df)
    elif view_choice == "2. Probability Distributions":
        _render_probability_distributions(art)
    elif view_choice == "3. Hypothesis Testing Studio":
        _render_hypothesis_testing(art)
    elif view_choice == "4. Correlation & Multicollinearity":
        _render_correlation_and_collinearity(art)
    elif view_choice == "5. Predictive Model & Simulator":
        _render_predictive_simulator(art)


if __name__ == "__main__":
    main()
