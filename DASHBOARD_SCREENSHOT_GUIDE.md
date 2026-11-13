# Capital Bikeshare Demand Analytics — Dashboard Screenshot & Evidence Guide
**Project:** Capital Bikeshare Demand Analytics and Predictive Simulator (Final Assignment)  
**Application File:** `app/streamlit_app.py`  
**Helper Library:** `app/helpers.py`  
**Server URL:** `http://localhost:8502`  
**Evidence Package Directory:** `dashboard_demonstration_package/` and `report_evidence_package/06_dashboard/`  
**Total Screenshots Captured:** 19 Unmocked, High-Resolution PNG Demonstrations  

---

## 1. Executive Purpose & Quality Standards

This guide provides an academic catalog and figure-by-figure placement guide for all 19 demonstration screenshots captured from the running Streamlit dashboard. Each entry documents:
1. **Screenshot File & Path**: Exact filename in the demonstration directory tree.
2. **Dashboard View & Interaction State**: Deep-linked URL query parameters, active sidebar filters, selected tabs, and viewport scroll offsets.
3. **Observed Visual Evidence**: Precise numerical values, chart components, statistical tables, and dynamic responses rendered in the user interface.
4. **Empirical & Theoretical Interpretation**: Grounding in the underlying dataset ($N = 731$ days) and verified analytical outputs.
5. **Academic Integration Mapping**: Recommended section and figure placement in the university Word report (`.docx`) and PowerPoint presentation (`.pptx`).

### Screenshot Quality Standards
- **Real Application Execution:** Captured directly from the running headless Microsoft Edge browser connected via Chrome DevTools Protocol (CDP) to `http://localhost:8502`. Zero synthetic mockups or simulated illustrations.
- **Consistent High Resolution:** Standard analytical views rendered at $1440 \times 1100\text{px}$; panoramic executive overview captured at $1440 \times 1450\text{px}$.
- **Zero Artifact Errors:** Clean UI state free of loading skeletons, unrendered widgets, truncated dataframes, or browser chrome overlays.
- **Single Source of Truth:** 100% numerical consistency with the analytical tables in `report_evidence_package/` and `outputs/tables/`.

---

## 2. Directory Structure Overview

```
dashboard_demonstration_package/
├── 01_overview_and_eda/
│   ├── 01_executive_kpis_and_summary.png
│   ├── 02_cohort_filter_spring_season.png
│   ├── 03_temporal_trends_timeseries_tab.png
│   ├── 04_categorical_weather_segmentations_tab.png
│   ├── 05_data_quality_and_outlier_audit_tab.png
│   └── 06_overview_panoramic_full_view.png
├── 02_probability_distributions/
│   ├── 01_cnt_distribution_and_qq_diagnostics_tab.png
│   ├── 02_poisson_overdispersion_and_models_tab.png
│   └── 03_environmental_predictors_distributions_tab.png
├── 03_hypothesis_testing/
│   ├── 01_h1_workingday_ttest_and_paradox_tab.png
│   ├── 02_h2_seasonal_anova_and_tukey_hsd_tab.png
│   └── 03_h3_weather_vs_high_demand_chisq_tab.png
├── 04_correlation_and_collinearity/
│   ├── 01_correlation_heatmaps_pearson_spearman.png
│   ├── 02_pairwise_correlation_tests_table.png
│   └── 03_multicollinearity_case_study_and_vif_tab.png
└── 05_predictive_simulator/
    ├── 01_model_benchmark_and_eval_metrics_tab.png
    ├── 02_regression_residual_diagnostics_grid.png
    ├── 03_realtime_demand_simulator_baseline_workday.png
    └── 04_realtime_demand_simulator_adverse_weather.png
```

---

## 3. Comprehensive Screenshot Catalog & Academic Integration

### Group 1: Executive Overview & EDA (`01_overview_and_eda/`)

#### 1. `01_executive_kpis_and_summary.png`
- **Application View:** View 1 (`1. Executive Overview & EDA`) — Top Metric Strip
- **Interactive State / Query:** `http://localhost:8502/?view=overview` (Baseline default landing state)
- **Visual Elements Rendered:**
  - Header: Capital Bikeshare Washington D.C. Daily Analytics ($N = 731$ days).
  - Five macro KPI cards:
    - **Observed Days:** `731 / 731` (`100.0% of full record`)
    - **Total Bike Rentals:** `3,292,679` (`100.0% total volume`)
    - **Mean Daily Rentals:** `4,504.3` (`± 1,937.2 std dev`)
    - **Registered Rider Share:** `81.2%` (`Casual: 18.8%`)
    - **Peak Single Day:** `8,714` (`Date: 2012-09-15`)
- **Empirical Findings:** The system operates with substantial registered commuter dominance ($81.17\%$). Across the two-year period, volume reached nearly $3.3\text{M}$ rentals, with notable daily dispersion ($\sigma = 1,937.21$). The all-time peak demand occurred on September 15, 2012 ($8,714$ rentals).
- **Word Report Placement:** **Section 1.1 (Dataset Information Summary)** / **Section 1.2 (Descriptive Statistical Analysis Baseline)**.
- **PowerPoint Slide Placement:** **Slide 2 (Executive Overview & Baseline KPIs)**.

---

#### 2. `02_cohort_filter_spring_season.png`
- **Application View:** View 1 (`1. Executive Overview & EDA`) — Dynamic Cohort Filter
- **Interactive State / Query:** `http://localhost:8502/?view=overview&season=1` (Sidebar multi-select: Season = Spring only)
- **Visual Elements Rendered:**
  - Active Sidebar Filter: Season `1: Spring` checked exclusively.
  - Dynamically recalculated KPI strip:
    - **Observed Days:** `181 / 731` (`24.8% of full record`)
    - **Total Bike Rentals:** `471,348` (`14.3% total volume`)
    - **Mean Daily Rentals:** `2,604.1` (`± 1,399.9 std dev` — **a $42.2\%$ drop below full-year average**)
    - **Registered Rider Share:** `87.1%` (`Casual: 12.9%`)
    - **Peak Single Day:** `7,836` (`Date: 2012-03-17`)
- **Empirical Findings:** Spring exhibits the lowest mean volume across all seasons ($2,604.1$ vs overall mean $4,504.3$), capturing only $14.3\%$ of total two-year rentals despite comprising $24.8\%$ of days. Registered commuter share rises to $87.14\%$ due to colder, less leisure-friendly weather.
- **Word Report Placement:** **Section 1.2 (Subgroup Descriptive Analysis)** / **Section 1.4 (Dataset Characteristics)**.
- **PowerPoint Slide Placement:** **Slide 4 (Seasonal Disparities & Cohort Filtering)**.

---

#### 3. `03_temporal_trends_timeseries_tab.png`
- **Application View:** View 1 (`1. Executive Overview & EDA`) — Tab 0: Temporal Trends & Time Series
- **Interactive State / Query:** `http://localhost:8502/?view=overview` $\rightarrow$ Click Tab 0 (Scroll $y = 250\text{px}$)
- **Visual Elements Rendered:**
  - 2-year daily rental time series chart (`fig01`) displaying raw daily demand alongside 7-day and 30-day moving averages.
  - Two statistical summary dataframes:
    - **Annual Growth Summary Table:** Year 0 (2011: $1,243,103$ rentals, mean $3,405.8$) vs Year 1 (2012: $2,049,576$ rentals, mean $5,599.9$), verifying a $+64.43\%$ total adoption increase.
    - **Monthly Demand Patterns Table:** Detailing progression across calendar months.
- **Word Report Placement:** **Section 1.3 (Temporal Trends, Seasonality & Annual Growth)**.
- **PowerPoint Slide Placement:** **Slide 5 (Temporal Trends: Adoption Growth & Seasonal Waves)**.

---

#### 4. `04_categorical_weather_segmentations_tab.png`
- **Application View:** View 1 (`1. Executive Overview & EDA`) — Tab 1: Categorical & Weather Segmentations
- **Interactive State / Query:** `http://localhost:8502/?view=overview` $\rightarrow$ Click Tab 1 (Scroll $y = 250\text{px}$)
- **Visual Elements Rendered:**
  - Season boxplot (`fig03`) displaying median, IQR, whiskers, and distribution spread across all four seasons.
  - Weather condition vs day type grouped bar chart with 95% bootstrap confidence intervals (`fig05`).
  - Underlying tables: `eda_group_by_season` and `eda_group_by_weathersit`.
- **Word Report Placement:** **Section 1.4 (Categorical Segmentations & Weather Interactions)**.
- **PowerPoint Slide Placement:** **Slide 6 (Categorical Segmentations: Weather & Calendar Factors)**.

---

#### 5. `05_data_quality_and_outlier_audit_tab.png`
- **Application View:** View 1 (`1. Executive Overview & EDA`) — Tab 2: Data Quality & Outlier Audit
- **Interactive State / Query:** `http://localhost:8502/?view=overview` $\rightarrow$ Click Tab 2 (Scroll $y = 250\text{px}$)
- **Visual Elements Rendered:**
  - Zero missing values, zero duplicated timestamps, and identity constraint audit ($cnt = casual + registered$).
  - **Tukey 1.5×IQR Outlier Audit Table:** Documenting $0$ outliers on `cnt`, $2$ low outliers on humidity (`hum`), and $13$ high outliers on wind speed (`windspeed`).
  - **Outlier Handling Sensitivity Table:** Demonstrating that retaining meteorological extremes preserves genuine operational variance without distorting mean metrics.
- **Word Report Placement:** **Section 1.1 (Data Hygiene, Verification & Outlier Analysis)**.
- **PowerPoint Slide Placement:** **Slide 3 (Data Hygiene, Outlier Sensitivity & Verification)**.

---

#### 6. `06_overview_panoramic_full_view.png`
- **Application View:** View 1 (`1. Executive Overview & EDA`) — Full Panoramic Capture
- **Interactive State / Query:** `http://localhost:8502/?view=overview` (Extended viewport $1440 \times 1450\text{px}$)
- **Visual Elements Rendered:**
  - Comprehensive overview capturing the sidebar filters, complete KPI banner, and Tab 0 layout on a single canvas.
- **Word Report Placement:** **Appendix A (Dashboard User Interface Architecture)**.
- **PowerPoint Slide Placement:** **Slide 2 (Application Architecture & UI Overview)**.

---

### Group 2: Probability Distribution Analysis (`02_probability_distributions/`)

#### 7. `01_cnt_distribution_and_qq_diagnostics_tab.png`
- **Application View:** View 2 (`2. Probability Distributions`) — Tab 0: Target Variable (`cnt`) Fit Diagnostics
- **Interactive State / Query:** `http://localhost:8502/?view=prob` $\rightarrow$ Click Tab 0 (Scroll $y = 120\text{px}$)
- **Visual Elements Rendered:**
  - 4-panel diagnostic plot (`fig06`): Histogram with KDE overlay, Empirical vs Normal CDF, Normal Q-Q plot, and Boxplot.
  - Goodness-of-Fit test summary table: Shapiro-Wilk ($W = 0.9798, p < 0.001$), Kolmogorov-Smirnov ($p < 0.001$), Skewness ($-0.0474$), and Excess Kurtosis ($-0.8119$).
  - Interpretation: Rental demand is symmetric but distinctly platykurtic, rejecting strict normality.
- **Word Report Placement:** **Section 2.1 (Target Variable Distribution & Goodness-of-Fit Tests)**.
- **PowerPoint Slide Placement:** **Slide 7 (Target Variable Distribution: Normality Rejection)**.

---

#### 8. `02_poisson_overdispersion_and_models_tab.png`
- **Application View:** View 2 (`2. Probability Distributions`) — Tab 1: Count Overdispersion & Poisson Rejection
- **Interactive State / Query:** `http://localhost:8502/?view=prob` $\rightarrow$ Click Tab 1 (Scroll $y = 120\text{px}$)
- **Visual Elements Rendered:**
  - **Equidispersion Audit Table & Metric Strip:**
    - Empirical Mean: `4,504.35`
    - Empirical Sample Variance: `3,752,788.21`
    - Dispersion Index ($D = \text{Var}/\text{Mean}$): **`833.15 >> 1.0`**
  - Warning callout explaining why standard Poisson regression fails and continuous OLS with robust standard errors or Negative Binomial regression is required.
- **Word Report Placement:** **Section 2.2 (Discrete Count Distribution Models & Overdispersion Analysis)**.
- **PowerPoint Slide Placement:** **Slide 8 (Poisson Rejection & Extreme Overdispersion)**.

---

#### 9. `03_environmental_predictors_distributions_tab.png`
- **Application View:** View 2 (`2. Probability Distributions`) — Tab 2: Environmental Predictors
- **Interactive State / Query:** `http://localhost:8502/?view=prob` $\rightarrow$ Click Tab 2 (Scroll $y = 120\text{px}$)
- **Visual Elements Rendered:**
  - Temperature distribution diagnostics (`fig07`) showing bimodal climatological mixture (seasonal modes).
  - Humidity and wind speed distributions (`fig08`): Left-skewed humidity (median 62.7%) and right-skewed Weibull-distributed wind speed (median 12.1 km/h).
- **Word Report Placement:** **Section 2.3 (Environmental Predictor Probability Profiles)**.
- **PowerPoint Slide Placement:** **Slide 9 (Environmental Variable Climatological Profiles)**.

---

### Group 3: Hypothesis Testing Studio (`03_hypothesis_testing/`)

#### 10. `01_h1_workingday_ttest_and_paradox_tab.png`
- **Application View:** View 3 (`3. Hypothesis Testing Studio`) — Tab 0: H1 Working Day Welch t-test
- **Interactive State / Query:** `http://localhost:8502/?view=hypos` $\rightarrow$ Click Tab 0 (Scroll $y = 150\text{px}$)
- **Visual Elements Rendered:**
  - Master hypothesis overview table summarizing H1, H2, and H3 test statistics.
  - Welch Two-Sample t-test bar chart with 95% error bars (`fig09`).
  - Test statistics table: $t_{\text{Welch}} = 1.6014$, $df = 413.9$, $p = 0.1101$, Mann-Whitney $U = 61,893.0, p = 0.1186$. Decision: **Fail to Reject $H_0$** at $\alpha = 0.05$.
  - **The User Composition Paradox:**
    - Casual Riders: `607 vs 1,371 / day` ($-55.8\%$ drop on workdays)
    - Registered Riders: `3,978 vs 2,959 / day` ($+34.4\%$ rise on workdays)
    - Net Total Daily Shift: `4,585 vs 4,330 / day` ($+5.9\%$, non-significant $p = 0.11$)
- **Empirical Findings:** Aggregate total demand is statistically indistinguishable between workdays and non-workdays, but rider category decomposition reveals two large, opposing behavioral shifts.
- **Word Report Placement:** **Section 3.1 (Hypothesis 1: Working Day Impact & User Composition Paradox)**.
- **PowerPoint Slide Placement:** **Slide 10 (Hypothesis 1: The Commuter Compensation Paradox)**.

---

#### 11. `02_h2_seasonal_anova_and_tukey_hsd_tab.png`
- **Application View:** View 3 (`3. Hypothesis Testing Studio`) — Tab 1: H2 Seasonal ANOVA
- **Interactive State / Query:** `http://localhost:8502/?view=hypos` $\rightarrow$ Click Tab 1 (Scroll $y = 150\text{px}$)
- **Visual Elements Rendered:**
  - Seasonal strip plot (`fig10`).
  - Omnibus metrics: One-Way ANOVA $F(3, 727) = 128.77, p < 0.001$; Kruskal-Wallis $H = 250.93, p < 0.001$. Decision: **Reject $H_0$**.
  - **Tukey HSD Post-Hoc Pairwise Comparisons Table:** Spring is significantly lower than all others ($p < 0.001$); Fall is peak ($5,644$ bikes/day); Summer vs Winter difference is not statistically significant ($p = 0.5401$).
- **Word Report Placement:** **Section 3.2 (Hypothesis 2: Multi-Group Seasonal ANOVA & Tukey HSD)**.
- **PowerPoint Slide Placement:** **Slide 11 (Hypothesis 2: Seasonal Demand Variance & Post-Hoc Tests)**.

---

#### 12. `03_h3_weather_vs_high_demand_chisq_tab.png`
- **Application View:** View 3 (`3. Hypothesis Testing Studio`) — Tab 2: H3 Weather vs Demand Chi-Square
- **Interactive State / Query:** `http://localhost:8502/?view=hypos` $\rightarrow$ Click Tab 2 (Scroll $y = 150\text{px}$)
- **Visual Elements Rendered:**
  - 2×3 grouped bar chart (`fig11`) showing proportion of high demand days ($> 4,548$ median) across weather categories.
  - **$2 \times 3$ Contingency Table:** Clear ($60.5\%$ high demand), Mist ($37.7\%$), Light Rain/Snow (**$0.0\%$ high demand**).
  - Test metrics: Pearson $\chi^2(2) = 44.09, p < 0.001$; Cramér's $V = 0.2456$ (Moderate Association). Decision: **Reject $H_0$**.
- **Word Report Placement:** **Section 3.3 (Hypothesis 3: Weather Independence & Contingency Analysis)**.
- **PowerPoint Slide Placement:** **Slide 12 (Hypothesis 3: Weather Sensitivity & Rain Aversion)**.

---

### Group 4: Correlation & Multicollinearity Lab (`04_correlation_and_collinearity/`)

#### 13. `01_correlation_heatmaps_pearson_spearman.png`
- **Application View:** View 4 (`4. Correlation & Multicollinearity Lab`) — Tab 0: Heatmaps
- **Interactive State / Query:** `http://localhost:8502/?view=corr` $\rightarrow$ Click Tab 0 (Top viewport)
- **Visual Elements Rendered:**
  - Dual annotated heatmaps: Pearson linear correlation ($r$) (`fig12`) vs Spearman monotonic rank correlation ($\rho$) (`fig13`).
  - Key coefficients: Temperature shows strongest positive association ($r = 0.6275, \rho = 0.6220$), humidity negative ($r = -0.1014, \rho = -0.0981$), windspeed negative ($r = -0.2345, \rho = -0.2172$).
- **Word Report Placement:** **Section 4.1 (Bivariate Linear & Monotonic Correlation Analysis)**.
- **PowerPoint Slide Placement:** **Slide 13 (Correlation Matrix: Pearson vs Spearman Diagnostics)**.

---

#### 14. `02_pairwise_correlation_tests_table.png`
- **Application View:** View 4 (`4. Correlation & Multicollinearity Lab`) — Tab 0: Significance & Confidence Intervals
- **Interactive State / Query:** `http://localhost:8502/?view=corr` $\rightarrow$ Click Tab 0 (Scroll $y = 520\text{px}$)
- **Visual Elements Rendered:**
  - Full pairwise statistical tests table listing: Pearson $r$, Spearman $\rho$, Student t-statistic, unadjusted $p$-values, Holm-Bonferroni adjusted $p$-values, and Fisher z-transformed 95% confidence intervals across all continuous pairs.
- **Word Report Placement:** **Section 4.2 (Pairwise Correlation Significance & Confidence Intervals)**.
- **PowerPoint Slide Placement:** **Slide 13 (Correlation Significance & Inferential Intervals)**.

---

#### 15. `03_multicollinearity_case_study_and_vif_tab.png`
- **Application View:** View 4 (`4. Correlation & Multicollinearity Lab`) — Tab 1: VIF & Collinearity Trap
- **Interactive State / Query:** `http://localhost:8502/?view=corr` $\rightarrow$ Click Tab 1 (Scroll $y = 120\text{px}$)
- **Visual Elements Rendered:**
  - Continuous predictors scatter plot grid with LOWESS smoothers (`fig14`).
  - **VIF Diagnostics Comparison Table:** Demonstrating extreme collinearity between `temp` and `atemp` ($r = 0.9917$, $\text{VIF} = 184.86$) and showing that dropping `atemp` eliminates variance inflation ($\text{VIF} = 3.61$ for `temp`, and $< 4.0$ for all remaining predictors).
- **Word Report Placement:** **Section 4.3 (Multicollinearity Diagnosis & VIF Remediation)**.
- **PowerPoint Slide Placement:** **Slide 14 (The Multicollinearity Trap: temp vs atemp)**.

---

### Group 5: Predictive Regression & Demand Simulator (`05_predictive_simulator/`)

#### 16. `01_model_benchmark_and_eval_metrics_tab.png`
- **Application View:** View 5 (`5. Predictive Regression & Simulator`) — Tab 0: Benchmark & Coefficients
- **Interactive State / Query:** `http://localhost:8502/?view=pred` $\rightarrow$ Click Tab 0 (Top viewport)
- **Visual Elements Rendered:**
  - Chronological 80/20 train/test benchmark table (Baseline vs OLS vs Ridge vs Collinear OLS).
  - Metric cards: **Held-Out Test $R^2 = 0.6139$**, **Held-Out Test $\text{RMSE} = 1,164.9$ bikes** (vs $2,560.6$ baseline), **Held-Out Test $\text{MAE} = 891.7$ bikes**, **Mean Bias = $-204.7$ bikes**.
  - OLS Regression Coefficients table with HAC robust standard errors.
  - In-sample training context: Train $R^2 = 0.8387$, Train $\text{RMSE} = 717.8$ bikes.
- **Word Report Placement:** **Section 5.1 (Model Training, Specification & Benchmark Evaluation)**.
- **PowerPoint Slide Placement:** **Slide 15 (Predictive Modeling: Chronological Holdout Benchmark)**.

---

#### 17. `02_regression_residual_diagnostics_grid.png`
- **Application View:** View 5 (`5. Predictive Regression & Simulator`) — Tab 0: Residual Diagnostics Grid
- **Interactive State / Query:** `http://localhost:8502/?view=pred` $\rightarrow$ Click Tab 0 (Scroll $y = 560\text{px}$)
- **Visual Elements Rendered:**
  - Four regression diagnostic plots:
    - *Actual vs Predicted (`fig15`):* Displays model tracking against true rental counts.
    - *Residuals vs Fitted (`fig16`):* Evaluates heteroscedasticity across demand levels.
    - *Residual Q-Q Plot and Histogram (`fig17`):* Gauges residual symmetry and tail behavior.
    - *Temporal Residuals (`fig18`):* Tracks forecast stability across chronological time.
  - Diagnostic note: Breusch-Pagan test ($p < 0.001$) and Shapiro-Wilk test ($p < 0.001$) indicate mild heteroscedasticity, confirming the necessity of HAC robust inference rather than naive OLS standard errors.
- **Word Report Placement:** **Section 5.2 (Regression Diagnostics & Gauss-Markov Validation)**.
- **PowerPoint Slide Placement:** **Slide 16 (Model Diagnostics: Residuals & Gauss-Markov Checks)**.

---

#### 18. `03_realtime_demand_simulator_baseline_workday.png`
- **Application View:** View 5 (`5. Predictive Regression & Simulator`) — Tab 1: Demand Simulator (Baseline Workday)
- **Interactive State / Query:** `?view=pred&sim_yr=1&sim_season=3&sim_daytype=Workday&sim_weather=1&temp=24.0&hum=55.0&wind=14.0`
- **Visual Elements Rendered:**
  - Simulator inputs: Mature Year 2012, Fall (season 3), Workday (`workingday=1`, `holiday=0`), Clear weather, 24°C, 55% humidity, 14 km/h wind.
  - Calculated Output Cards:
    - **Predicted Total Demand:** `6,019` bikes
    - **Estimated Registered Riders:** `5,149` bikes (`85.5%`)
    - **Estimated Casual Riders:** `870` bikes (`14.5%`)
    - **Standard Error of Mean:** `± 95.1` bikes
  - **95% Confidence Interval for Mean Daily Demand:** `[5,832, 6,206]` bikes (Sampling uncertainty of expected mean demand; not an operational guarantee).
  - **95% Prediction Interval for Single Day:** `[4,582, 7,456]` bikes (Statistical forecast interval for an individual day accounting for residual dispersion $\sigma^2$).
  - **Fleet Advisory Banner:** *"Standard Fleet Operations"*
- **Word Report Placement:** **Section 5.3 (Interactive Decision Support & Scenario Simulation)**.
- **PowerPoint Slide Placement:** **Slide 17 (Operational Simulator: Baseline Commuter Scenario)**.

---

#### 19. `04_realtime_demand_simulator_adverse_weather.png`
- **Application View:** View 5 (`5. Predictive Regression & Simulator`) — Tab 1: Demand Simulator (Adverse Weather)
- **Interactive State / Query:** `?view=pred&sim_yr=1&sim_season=4&sim_daytype=Weekend+%2F+Holiday&sim_weather=3&temp=4.0&hum=85.0&wind=28.0`
- **Visual Elements Rendered:**
  - Simulator inputs: Mature Year 2012, Winter (season 4), Weekend / Holiday (`workingday=0`, `holiday=0`), Light Snow/Rain, 4°C, 85% humidity, 28 km/h wind.
  - Calculated Output Cards:
    - **Predicted Total Demand:** `1,781` bikes (a severe $70.4\%$ reduction relative to baseline)
    - **Estimated Registered Riders:** `1,530` bikes (`85.9%`)
    - **Estimated Casual Riders:** `250` bikes (`14.1%`)
    - **Standard Error of Mean:** `± 233.5` bikes
  - **95% Confidence Interval for Mean Daily Demand:** `[1,322, 2,239]` bikes (Sampling uncertainty of expected mean demand; not an operational guarantee).
  - **95% Prediction Interval for Single Day:** `[284, 3,277]` bikes (Statistical forecast interval for an individual day accounting for residual dispersion $\sigma^2$).
  - **Fleet Advisory Banner:** *"Low Demand Notice: Opportunity window for bike maintenance and station rebalancing."*
- **Word Report Placement:** **Section 5.3 (Interactive Decision Support & Scenario Simulation)**.
- **PowerPoint Slide Placement:** **Slide 18 (Operational Simulator: Adverse Weather Stress-Testing)**.

---

## 4. Verification Checklist

- [x] **19 Real Screenshots Captured:** Zero mocked or placeholder images. Verified resolutions at $1440 \times 1100\text{px}$ and $1440 \times 1450\text{px}$ with file sizes ranging between $166\text{ KB}$ and $363\text{ KB}$.
- [x] **Automated Test Suite Verified:** All 26 automated tests passed (`pytest tests -v` completed with zero failures).
- [x] **Complete Traceability Matrix:** Every user-facing view, tab, filter, and simulation state is documented.
- [x] **100% Statistical Invariant Alignment:** All KPI cards, hypothesis statistics, correlation coefficients, model metrics, and simulator predictions agree with the verified evidence package.
