# Final Handoff & Rubric Audit Report (Stopped After Phase 6 per User Directive)

**Project:** Statistical Analysis and Visualization of Daily Bike-Rental Demand (`day.csv`)  
**Execution Scope:** Phases 0 through 6 Completed & Verified (User instructed: *"stop after phase 6, i will do phase 7: academic report myself"* and *"i will do phase 8 myself"*).  
**Midterm Eligibility Gate:** `MIDTERM_DATASET_NOT_CONFIRMED` — Student must verify that the UCI Bike Sharing dataset was not used in their midterm project before submitting.

---

## 1. Official 100-Point Rubric Audit Table (Phases 1–6 + Python Implementation)

| Rubric Item | Weight | Code Location | Numerical Evidence (`outputs/tables/`) | Figure(s) (`outputs/figures/`) | Planned Report Section (User Phase 7) | Result |
|---|---:|---|---|---|---|---|
| **Exploratory Data Analysis (EDA) & Visualization** | **15** | `src/load_validate.py`<br>`src/descriptive_eda.py`<br>`src/plots/eda_plots.py` | `data_dictionary_summary.csv`<br>`eda_continuous_summary.csv`<br>`eda_group_by_year.csv`<br>`eda_group_by_season.csv`<br>`eda_group_by_weathersit.csv`<br>`eda_group_by_workingday.csv`<br>`eda_outlier_audit.csv`<br>`eda_outlier_handling_sensitivity.csv` | `fig01_daily_rentals_timeseries.png`<br>`fig02_cnt_distribution_hist_kde.png`<br>`fig03_cnt_boxplot_by_season.png`<br>`fig04_temp_vs_cnt_scatter.png`<br>`fig05_mean_cnt_by_weather_workday_ci.png` | Chapters 4 & 5 (Data Provenance, Quality & EDA) | **PASS** (Code, Tables & 5 Plot Types Complete) |
| **Probability Distributions** | **15** | `src/probability.py`<br>`src/plots/prob_hypos_plots.py` | `probability_distribution_summary.csv`<br>`cnt_overdispersion_and_fit.csv`<br>`temp_distribution_diagnostics.csv` | `fig06_cnt_distribution_diagnostics.png`<br>`fig07_temp_distribution_diagnostics.png`<br>`fig08_hum_windspeed_distributions.png` | Chapter 6 (Probability Distribution Analysis) | **PASS** (Code, Overdispersion & Mixture Diagnostics Complete) |
| **Hypothesis Testing** | **15** | `src/hypothesis_tests.py`<br>`src/plots/prob_hypos_plots.py` | `hypothesis_tests_summary.csv`<br>`h1_ttest_workingday.csv`<br>`h2_anova_season_posthoc.csv`<br>`h3_chisq_contingency_table.csv` | `fig09_h1_workingday_ttest.png`<br>`fig10_h2_season_anova.png`<br>`fig11_h3_weathersit_highdemand_chisq.png` | Chapter 7 (Hypothesis Testing: t-test, ANOVA, Chi-Square) | **PASS** (H1, H2, H3 Executed with Robustness & Holm Checks) |
| **Correlations (Pearson & Spearman)** | **15** | `src/correlations.py`<br>`src/plots/corr_reg_plots.py` | `pearson_correlation_matrix.csv`<br>`spearman_correlation_matrix.csv`<br>`correlation_pairwise_tests.csv` | `fig12_pearson_correlation_heatmap.png`<br>`fig13_spearman_correlation_heatmap.png`<br>`fig14_continuous_predictors_scatter_grid.png` | Chapter 8 (Linear & Monotonic Correlation Analysis) | **PASS** (Pearson $r$, Spearman $\rho$, CIs & Heatmaps Complete) |
| **Multiple Linear Regression** | **20** | `src/regression.py`<br>`src/plots/corr_reg_plots.py` | `regression_model_comparison.csv`<br>`regression_ols_coefficients.csv`<br>`regression_vif_diagnostics.csv`<br>`regression_residual_diagnostics.csv`<br>`outputs/model/test_predictions.csv` | `fig15_regression_actual_vs_predicted.png`<br>`fig16_regression_residuals_vs_fitted.png`<br>`fig17_regression_residual_qq_hist.png`<br>`fig18_regression_temporal_predictions_errors.png` | Chapters 9 & 10 (OLS Regression, Diagnostics & Implications) | **PASS** (Chronological 80/20 Split, Anti-Leakage, VIF & HC3/HAC Complete) |
| **Python Quality & Reproducibility** | **20** | `src/run_all.py`<br>`src/artifact_generation.py`<br>`notebooks/analysis.ipynb`<br>`tests/test_*.py` | `outputs/results.json`<br>`outputs/dataset_audit.json` | All 18 figures generated deterministically at 300 DPI | Chapter 12 & Appendix A (Reproducibility Architecture) | **PASS** (`15 passed` in `pytest` suite) |

---

## 2. Executive Reference Sheet of Computed Numbers (For Your Phase 7 Report)

All values below come directly from `outputs/results.json` and the CSV tables in `outputs/tables/`:

### A. Dataset Provenance & Quality (Phase 1)
- **Dimensions:** $N = 731$ days (`2011-01-01` to `2012-12-31`), $p = 16$ columns.
- **Cryptographic Checksum:** `data/raw/day.csv` (57,569 bytes, SHA-256: `a6bcf826782d3c0fbfdcbeead17cd0884185a0dafe8ff10cd48a874ee7ba18be`).
- **Missingness & Duplicates:** $0$ missing cells across $11,696$ values; $0$ duplicate rows or dates; $0$ date gaps.
- **Target Accounting Identity:** `cnt == casual + registered` holds exactly on all 731 rows ($0$ violations).

### B. Exploratory Data Analysis & Outliers (Phase 2)
- **Total Daily Rentals (`cnt`):** Mean $= 4,504.35$, SD $= 1,937.21$, Median $= 4,548.00$, IQR $= 2,803.00$ ($Q_1 = 3,152.00$, $Q_3 = 5,955.00$), Min $= 22$ (`2012-10-29`, Hurricane Sandy), Max $= 8,714$ (`2012-09-15`), Skewness $= -0.0474$, Excess Kurtosis $= -0.8608$.
- **Year-over-Year System Expansion:**
  - `2011` ($n = 365$): Mean $= 3,405.76$ ($\text{SD} = 1,378.76$, Median $= 3,740.00$).
  - `2012` ($n = 366$): Mean $= 5,599.93$ ($\text{SD} = 1,788.67$, Median $= 5,927.00$) $\rightarrow$ **$+64.43\%$ growth**.
- **Seasonal Breakdown (`cnt`):**
  - `1: Spring (UCI 1: Dec–Mar)` ($n = 181$): Mean $= 2,604.13$ ($\text{SD} = 1,399.94$, Median $= 2,209.00$, Mean Temp $= 12.21^\circ\text{C}$).
  - `2: Summer (UCI 2: Mar–Jun)` ($n = 184$): Mean $= 4,992.33$ ($\text{SD} = 1,695.98$, Median $= 4,941.50$, Mean Temp $= 22.32^\circ\text{C}$).
  - `3: Fall (UCI 3: Jun–Sep)` ($n = 188$): Mean $= 5,644.30$ ($\text{SD} = 1,459.80$, Median $= 5,353.50$, Mean Temp $= 28.96^\circ\text{C}$).
  - `4: Winter (UCI 4: Sep–Dec)` ($n = 178$): Mean $= 4,728.16$ ($\text{SD} = 1,699.62$, Median $= 4,634.50$, Mean Temp $= 17.34^\circ\text{C}$).
- **Weather Breakdown (`cnt`):**
  - `1: Clear / Partly Cloudy` ($n = 463$, $63.34\%$): Mean $= 4,876.79$ ($\text{SD} = 1,879.48$).
  - `2: Mist / Cloudy` ($n = 247$, $33.79\%$): Mean $= 4,035.86$ ($\text{SD} = 1,809.11$).
  - `3: Light Snow / Light Rain` ($n = 21$, $2.87\%$): Mean $= 1,803.29$ ($\text{SD} = 1,240.28$).
  - `4: Heavy Rain / Ice Pellets`: $0$ occurrences at the daily aggregated level in `day.csv`.
- **Notable Physical Anomalies Retained & Audited:**
  - `2011-03-10` (`instant=69`): `hum = 0.0` (weather sensor dropout during rainy day, `cnt = 623`).
  - `2011-08-17` (`instant=229`): `temp = 0.7233` vs `atemp = 0.2424` (apparent temperature logging anomaly).
  - `2012-10-29` & `2012-10-30` (`instant=668, 669`): Hurricane Sandy landfall (`cnt = 22` and `cnt = 1,096`).

### C. Probability Distribution Diagnostics (Phase 3)
1. **`cnt` (Discrete Daily Counts):**
   - **Poisson Overdispersion Check:** Observed variance $s^2 = 3,752,788.21$ vs. mean $\bar{y} = 4,504.35 \implies$ Index of Dispersion $D = s^2/\bar{y} = \mathbf{833.15}$ ($\chi^2_{730} = 608,199.14$, $p < 10^{-300}$). Homogeneous Poisson is overwhelmingly rejected.
   - **Negative Binomial Fit:** $r = 5.4128$, $p = 0.001200$, Log-Likelihood $= -6,584.33$, $\text{AIC} = 13,172.67$.
   - **Normal Fit:** $\mu = 4,504.35$, $\sigma = 1,937.21$, Log-Likelihood $= -6,569.61$, $\text{AIC} = 13,143.22$; Shapiro-Wilk $W = 0.9801$ ($p = 2.08 \times 10^{-8}$), D'Agostino $K^2 = 62.71$ ($p = 2.42 \times 10^{-14}$), Lilliefors KS $= 0.0471$ (bootstrap $p = 0.0010$). Symmetric ($\text{skew} = -0.0474$) but platykurtic ($\text{kurtosis} = -0.8608$) due to multi-year and multi-season regime mixing.
2. **`temp` (Bounded Normalized Temperature $[0, 1]$):**
   - Mean $= 0.4954$ ($20.31^\circ\text{C}$), SD $= 0.1830$, Skewness $= -0.0545$, Excess Kurtosis $= \mathbf{-1.1189}$ (strongly platykurtic).
   - Shapiro-Wilk $W = 0.9659$ ($p = 5.15 \times 10^{-12}$), Lilliefors KS $= 0.0727$ (bootstrap $p = 0.0005$). Driven by a **bimodal seasonal mixture** between cold winter-spring days (`season=1` mean $= 0.2977$) and warm summer-fall days (`season=3` mean $= 0.7063$).

### D. Hypothesis Testing Summary (Phase 4)
1. **H1 — Welch Two-Sample $t$-Test (`cnt` by `workingday`):**
   - Working day ($n_1 = 500$): Mean $= 4,584.82$ ($\text{SD} = 1,878.42$); Non-working day ($n_0 = 231$): Mean $= 4,330.17$ ($\text{SD} = 2,052.14$).
   - Difference $= +254.65$ bikes/day, $95\%\text{ CI } [-57.94, +567.24]$, $t_{\text{Welch}} = \mathbf{1.6014}$, $\text{df} = 413.94$, $p = \mathbf{0.1101}$ (Holm $p = 0.1101$), Hedges' $g = 0.1315$ $\rightarrow$ **Fail to reject $H_0$**.
   - *Mechanism:* Registered commuter trips jump by $+1,019.01$ bikes/day on working days ($p = 5.81 \times 10^{-19}$), while casual recreational trips drop by $-764.36$ bikes/day on working days ($p = 1.80 \times 10^{-29}$), offsetting each other in aggregate `cnt`.
2. **H2 — One-Way & Welch ANOVA (`cnt` across `season` $1..4$):**
   - Ordinary $F(3, 727) = \mathbf{128.7696}$, $p = \mathbf{6.72 \times 10^{-67}}$ (Holm $p = 2.02 \times 10^{-66}$); Welch $F(3, 401.81) = \mathbf{153.9912}$, $p = 1.95 \times 10^{-66}$; Kruskal-Wallis $H = 250.93$, $p = 4.11 \times 10^{-54}$.
   - Effect sizes: $\eta^2 = \mathbf{0.3470}$ ($34.70\%$ of variance explained), $\omega^2 = \mathbf{0.3440}$ $\rightarrow$ **Reject $H_0$**.
   - Tukey HSD post-hoc: 5 of 6 seasonal pairs are statistically significant ($p < 0.001$); only `Summer (2)` vs `Winter (4)` ($\Delta = -264.17$, Tukey $p = 0.378$) is non-significant.
3. **H3 — Pearson Chi-Square Test of Independence (`weathersit` vs `high_demand` $[\text{cnt} > 4,548]$):**
   - $\chi^2(2) = \mathbf{44.0879}$, $p = \mathbf{2.67 \times 10^{-10}}$ (Holm $p = 5.34 \times 10^{-10}$), Likelihood-Ratio $G^2 = 48.17$ ($p = 3.47 \times 10^{-11}$), Cramér's $V = \mathbf{0.2456}$ $\rightarrow$ **Reject $H_0$**.
   - High-demand share drops from $58.32\%$ ($270/463$) in Clear weather (`1`) to $38.06\%$ ($94/247$) in Mist/Cloudy (`2`) and $4.76\%$ ($1/21$) in Light Snow/Rain (`3`). Minimum expected cell count $= 10.49 \ge 5$ (Cochran's rule satisfied).

### E. Correlation Analysis (Phase 5)
- `cnt` vs `temp`: Pearson $r = \mathbf{+0.6275}$ ($p = 2.81 \times 10^{-81}$), Spearman $\rho = \mathbf{+0.6220}$ ($p = 1.67 \times 10^{-79}$).
- `cnt` vs `atemp`: Pearson $r = \mathbf{+0.6311}$ ($p = 1.85 \times 10^{-82}$), Spearman $\rho = \mathbf{+0.6228}$ ($p = 9.62 \times 10^{-80}$).
- `cnt` vs `windspeed`: Pearson $r = \mathbf{-0.2345}$ ($p = 1.36 \times 10^{-10}$), Spearman $\rho = \mathbf{-0.2172}$ ($p = 2.97 \times 10^{-9}$).
- `cnt` vs `hum`: Pearson $r = \mathbf{-0.1007}$ ($p = 0.00645$), Spearman $\rho = \mathbf{-0.0981}$ ($p = 0.00793$).
- `temp` vs `atemp` (Collinearity): Pearson $r = \mathbf{+0.9917}$, Spearman $\rho = \mathbf{+0.9926}$ $\rightarrow$ justifies dropping `atemp` in primary OLS.

### F. Multiple Linear Regression (Phase 6)
- **Chronological 80/20 Split:**
  - Training Set ($80\%, n = 584$): `2011-01-01` to `2012-08-06`.
  - Hold-Out Test Set ($20\%, n = 147$): `2012-08-07` to `2012-12-31`.
- **VIF Multicollinearity Audit:** Including both `temp` and `atemp` inflates $\text{VIF}(\text{temp}) = 63.03$ and $\text{VIF}(\text{atemp}) = 63.61$; dropping `atemp` reduces $\text{VIF}(\text{temp})$ to $\mathbf{3.19}$ (all predictors $\text{VIF} \le 3.45$).
- **Model Performance Comparison:**
  - **Training OLS ($n=584$):** $R^2 = \mathbf{0.8387}$, Adjusted $R^2 = \mathbf{0.8356}$, $\text{RMSE} = \mathbf{717.85}$ bikes/day, $\text{MAE} = \mathbf{539.45}$ bikes/day.
  - **Hold-Out Test Mean Baseline ($n=147$):** $R^2 = \mathbf{-0.8657}$, $\text{RMSE} = \mathbf{2,560.56}$ bikes/day, $\text{MAE} = \mathbf{2,290.41}$ bikes/day.
  - **Hold-Out Test Primary OLS ($n=147$):** $R^2 = \mathbf{0.6139}$, $\text{RMSE} = \mathbf{1,164.87}$ bikes/day (**$-54.51\%$ error reduction** vs. baseline), $\text{MAE} = \mathbf{891.69}$ bikes/day (**$-61.07\%$ error reduction** vs. baseline).
- **Residual Diagnostics:** Durbin-Watson $= 1.2253$ (Ljung-Box lag-7 $Q = 141.78, p = 2.09 \times 10^{-27}$), Breusch-Pagan $\text{LM} = 62.57$ ($p = 3.08 \times 10^{-9}$), Shapiro-Wilk $W = 0.9764$ ($p = 4.32 \times 10^{-8}$). Full OLS coefficients with Classical IID, White HC3, and Newey-West HAC (lag=7) standard errors are saved in `outputs/tables/regression_ols_coefficients.csv`.

---

## 3. Remaining User Actions (`NEEDS_USER`)

1. **Author Phase 7 Academic Report (`report/Final_Report.docx` & `report/Final_Report.pdf`):**
   - Use the tables in `outputs/tables/`, the 18 figures in `outputs/figures/`, and the exact numbers in `outputs/results.json` (summarized above).
2. **Author Phase 8 Presentation Slides, Video & Submission Archive:**
   - Build `presentation/Final_Presentation.pptx` and `presentation/SPEAKER_SCRIPT.md`.
   - Record the 7–15 minute presentation video, upload to YouTube, and place the public/unlisted URL on **Slide 2**.
   - Package the final submission archive once your Student ID and portal naming convention are verified.
3. **Verify Administrative & Eligibility Items:**
   - Confirm that the UCI Bike Sharing dataset was **not** used in your midterm project (`MIDTERM_DATASET_NOT_CONFIRMED`).
   - Confirm the active submission deadline with your instructor (handout lists October 13, 2026).
   - Fill in your actual Student Name, Student ID, and group contribution table.
