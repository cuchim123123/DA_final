# Evidence Manifest (`EVIDENCE_MANIFEST.md`)

## Purpose
This manifest maps **every official requirement and subrequirement** in `REPORT_ASSIGNMENTS.md` to its exact supporting tables, figures, and methodological documentation inside `report_evidence_package/`. All file paths are relative to the root of `report_evidence_package/`.

---

## 1. Master Subrequirement-to-File Mapping Table

| Requirement ID | Official Assignment Subrequirement (`REPORT_ASSIGNMENTS.md`) | Supporting Tables (CSV / JSON) | Supporting Figures (300-DPI PNG) | Relevant Explanations & Documentation | Verification Status | Missing Evidence |
|---|---|---|---|---|---|---|
| **GEN-1** | **General Requirements:**<br>Select one real-world dataset ($\ge 500$ rows, $\ge 5$ variables) from an open source (UCI / Kaggle), distinct from midterm, and use consistently across all sections. | `00_dataset_and_documentation/day.csv`<br>`00_dataset_and_documentation/dataset_audit.json`<br>`00_dataset_and_documentation/results.json`<br>`01_exploratory_data_analysis/tables/data_dictionary_summary.csv` | — | `REPORT_EVIDENCE_GUIDE.md` (§0)<br>`00_dataset_and_documentation/Readme.txt`<br>`00_dataset_and_documentation/DATA_DICTIONARY.md`<br>`00_dataset_and_documentation/REFERENCES.md` | **VERIFIED** ($N = 731$ rows, $p = 16$ variables; SHA-256 checksum verified) | None *(Student must confirm dataset was not used in their midterm)* |
| **REQ-1.1** | **1.1. Summarize Dataset Information:**<br>- Examine number of records, number of variables, and data type of each variable.<br>- Handle missing data and duplicate records (if any). | `01_exploratory_data_analysis/tables/data_dictionary_summary.csv`<br>`01_exploratory_data_analysis/tables/eda_categorical_frequencies.csv`<br>`01_exploratory_data_analysis/tables/eda_data_quality_anomalies.csv`<br>`00_dataset_and_documentation/dataset_audit.json` | — | `REPORT_EVIDENCE_GUIDE.md` (§1.1)<br>`00_dataset_and_documentation/DATA_DICTIONARY.md`<br>`00_dataset_and_documentation/STATISTICAL_DECISIONS.md` (§1) | **VERIFIED** ($0$ missing cells across $11,696$ values; $0$ duplicate rows/dates; `cnt == casual + registered` verified on all $731$ rows) | None |
| **REQ-1.2** | **1.2. Descriptive Statistical Analysis:**<br>- Calculate descriptive statistics (mean, median, SD, quartiles, etc.).<br>- Visualize data using $\ge 3$ different chart types to identify trends.<br>- Explain reasons for selecting each chart type. | `01_exploratory_data_analysis/tables/eda_continuous_summary.csv`<br>`01_exploratory_data_analysis/tables/eda_categorical_frequencies.csv`<br>`01_exploratory_data_analysis/tables/eda_group_by_season.csv`<br>`01_exploratory_data_analysis/tables/eda_group_by_weathersit.csv`<br>`01_exploratory_data_analysis/tables/eda_group_by_workingday.csv`<br>`01_exploratory_data_analysis/tables/eda_group_by_year.csv`<br>`01_exploratory_data_analysis/tables/eda_group_by_holiday.csv`<br>`01_exploratory_data_analysis/tables/eda_weather_by_workingday.csv` | `01_exploratory_data_analysis/figures/fig01_daily_rentals_timeseries.png` (Line chart)<br>`01_exploratory_data_analysis/figures/fig02_cnt_distribution_hist_kde.png` (Histogram + KDE)<br>`01_exploratory_data_analysis/figures/fig03_cnt_boxplot_by_season.png` (Boxplot + Strip)<br>`01_exploratory_data_analysis/figures/fig04_temp_vs_cnt_scatter.png` (Scatter + LOWESS)<br>`01_exploratory_data_analysis/figures/fig05_mean_cnt_by_weather_workday_ci.png` (Grouped Bar + 95% CI) | `REPORT_EVIDENCE_GUIDE.md` (§1.2)<br>`00_dataset_and_documentation/FIGURE_REGISTER.md` (Figs 1–5) | **VERIFIED** (All $7$ continuous variables & $7$ categorical variables summarized; $5$ distinct chart types exported with selection rationale) | None |
| **REQ-1.3** | **1.3. Outlier Detection:**<br>- Present methods for identifying outliers (Tukey $1.5\times\text{IQR}$ & Z-score $|z|>3$).<br>- Propose appropriate methods for handling outliers. | `01_exploratory_data_analysis/tables/eda_outlier_audit.csv`<br>`01_exploratory_data_analysis/tables/eda_outlier_handling_sensitivity.csv`<br>`01_exploratory_data_analysis/tables/eda_data_quality_anomalies.csv` | `01_exploratory_data_analysis/figures/fig01_daily_rentals_timeseries.png`<br>`01_exploratory_data_analysis/figures/fig03_cnt_boxplot_by_season.png`<br>`02_probability_distributions/figures/fig08_hum_windspeed_distributions.png` | `REPORT_EVIDENCE_GUIDE.md` (§1.3)<br>`00_dataset_and_documentation/STATISTICAL_DECISIONS.md` (§1.3) | **VERIFIED** (IQR and Z-score counts, fences, sample dates, and sensitivity check for `hum = 0.0` exported) | None |
| **REQ-1.4** | **1.4. Overall Dataset Assessment:**<br>- Identify and discuss notable characteristics of the dataset based on the analyses above. | `01_exploratory_data_analysis/tables/eda_continuous_summary.csv`<br>`01_exploratory_data_analysis/tables/eda_group_by_year.csv`<br>`01_exploratory_data_analysis/tables/eda_group_by_season.csv`<br>`01_exploratory_data_analysis/tables/eda_group_by_weathersit.csv`<br>`01_exploratory_data_analysis/tables/eda_group_by_workingday.csv` | `01_exploratory_data_analysis/figures/fig01_daily_rentals_timeseries.png` through `fig05_mean_cnt_by_weather_workday_ci.png` | `REPORT_EVIDENCE_GUIDE.md` (§1.4)<br>`00_dataset_and_documentation/DATA_DICTIONARY.md` (§3: `season` coding vs. astronomical dates) | **VERIFIED** (Synthesizes $+64.43\%$ YoY expansion, $81.17\%$ registered vs. $18.83\%$ casual split, weekday/weekend offset, and weather sensitivity) | None |
| **REQ-2** | **2. Probability Distribution Analysis:**<br>- Select $\ge 2$ important variables (`cnt` and `temp`, plus `hum` and `windspeed` context) and examine whether they follow probability distributions (Normal, Poisson, Negative Binomial, Exponential, Gamma, Beta).<br>- Use appropriate charts to illustrate distributions.<br>- Provide observations on data characteristics. | `02_probability_distributions/tables/probability_distribution_summary.csv`<br>`02_probability_distributions/tables/cnt_overdispersion_and_fit.csv`<br>`02_probability_distributions/tables/cnt_candidate_distributions_comparison.csv`<br>`02_probability_distributions/tables/temp_distribution_diagnostics.csv`<br>`02_probability_distributions/tables/weather_variables_candidate_fits.csv` | `02_probability_distributions/figures/fig06_cnt_distribution_diagnostics.png`<br>`02_probability_distributions/figures/fig07_temp_distribution_diagnostics.png`<br>`02_probability_distributions/figures/fig08_hum_windspeed_distributions.png` | `REPORT_EVIDENCE_GUIDE.md` (§2)<br>`00_dataset_and_documentation/STATISTICAL_DECISIONS.md` (§2) | **VERIFIED** (Poisson overdispersion $D=833.15$, Negative Binomial, Normal, Gamma, Exponential, and Beta fits with AIC, LL, KS, Shapiro-Wilk, D'Agostino $K^2$, and Q-Q plots exported) | None |
| **REQ-3a** | **3a. Hypothesis Testing — Statistical Test Theory:**<br>- Study and explain `t-test`, `Chi-square test`, and `ANOVA`. | — | — | `REPORT_EVIDENCE_GUIDE.md` (§3.1)<br>`00_dataset_and_documentation/RESEARCH_DESIGN.md` (§3)<br>`00_dataset_and_documentation/STATISTICAL_DECISIONS.md` (§3) | **VERIFIED** (Formulas, $H_0/H_1$, degrees of freedom, assumptions, and robust alternatives documented) | None |
| **REQ-3b** | **3b. Hypothesis Testing — Research Questions and Statistical Testing:**<br>- Propose $\ge 2$ research questions (3 complete tests provided: H1 Welch $t$-test on `workingday`, H2 One-Way/Welch ANOVA on `season`, H3 Chi-square on `weathersit` vs. `high_demand`).<br>- Apply statistical hypothesis testing to answer them. | `03_hypothesis_testing/tables/hypothesis_tests_summary.csv`<br>`03_hypothesis_testing/tables/h1_ttest_workingday.csv`<br>`03_hypothesis_testing/tables/h2_anova_omnibus_and_groups.csv`<br>`03_hypothesis_testing/tables/h2_anova_season_posthoc.csv`<br>`03_hypothesis_testing/tables/h3_chisq_contingency_table.csv`<br>`03_hypothesis_testing/tables/h3_chisq_omnibus_and_robustness.csv` | `03_hypothesis_testing/figures/fig09_h1_workingday_ttest.png`<br>`03_hypothesis_testing/figures/fig10_h2_season_anova.png`<br>`03_hypothesis_testing/figures/fig11_h3_weathersit_highdemand_chisq.png` | `REPORT_EVIDENCE_GUIDE.md` (§3.2)<br>`00_dataset_and_documentation/RESEARCH_DESIGN.md` (§3) | **VERIFIED** (Exact test statistics, unadjusted & Holm $p$-values, Levene/Shapiro/Cochran assumption checks, Tukey/Welch post-hoc tests, and effect sizes exported) | None |
| **REQ-3c** | **3c. Hypothesis Testing — Interpretation:**<br>- Explain the results of the statistical hypothesis tests. | `03_hypothesis_testing/tables/hypothesis_tests_summary.csv`<br>`03_hypothesis_testing/tables/h1_ttest_workingday.csv` (includes `registered` & `casual` offset rows)<br>`03_hypothesis_testing/tables/h2_anova_season_posthoc.csv`<br>`03_hypothesis_testing/tables/h3_chisq_contingency_table.csv` | `03_hypothesis_testing/figures/fig09_h1_workingday_ttest.png`<br>`03_hypothesis_testing/figures/fig10_h2_season_anova.png`<br>`03_hypothesis_testing/figures/fig11_h3_weathersit_highdemand_chisq.png` | `REPORT_EVIDENCE_GUIDE.md` (§3.2) | **VERIFIED** (Statistical decisions linked to domain mechanisms, including the $+1,019.22$ registered vs. $-764.56$ casual workday offset) | None |
| **REQ-4a** | **4a. Correlation Analysis — Theoretical Background:**<br>- Study and explain Pearson ($r$) and Spearman ($\rho$) correlation coefficients. | — | — | `REPORT_EVIDENCE_GUIDE.md` (§4.1)<br>`00_dataset_and_documentation/STATISTICAL_DECISIONS.md` (§4) | **VERIFIED** (Mathematical formulas, linear vs. monotonic distinction, assumptions, and outlier sensitivity documented) | None |
| **REQ-4b** | **4b. Correlation Analysis — Correlation Calculation:**<br>- Calculate Pearson and Spearman correlation coefficients between variables in the dataset. | `04_correlation_analysis/tables/pearson_correlation_matrix.csv`<br>`04_correlation_analysis/tables/spearman_correlation_matrix.csv`<br>`04_correlation_analysis/tables/correlation_pairwise_tests.csv`<br>`04_correlation_analysis/tables/extended_correlations_with_cnt.csv` | — | `REPORT_EVIDENCE_GUIDE.md` (§4.2) | **VERIFIED** ($5\times 5$ matrices, all $10$ pairwise CIs & $p$-values, plus extended $13$-variable correlation table with `cnt` exported) | None |
| **REQ-4c** | **4c. Correlation Analysis — Visualization:**<br>- Use appropriate charts to visualize relationships between variables. | — | `04_correlation_analysis/figures/fig12_pearson_correlation_heatmap.png`<br>`04_correlation_analysis/figures/fig13_spearman_correlation_heatmap.png`<br>`04_correlation_analysis/figures/fig14_continuous_predictors_scatter_grid.png` | `REPORT_EVIDENCE_GUIDE.md` (§4.2)<br>`00_dataset_and_documentation/FIGURE_REGISTER.md` (Figs 12–14) | **VERIFIED** (Separate annotated Pearson and Spearman heatmaps + $2\times 2$ scatter/LOWESS grid exported) | None |
| **REQ-4d** | **4d. Correlation Analysis — Practical Interpretation:**<br>- Discuss the practical significance of the observed correlations. | `04_correlation_analysis/tables/correlation_pairwise_tests.csv`<br>`04_correlation_analysis/tables/extended_correlations_with_cnt.csv` | `04_correlation_analysis/figures/fig12_pearson_correlation_heatmap.png` through `fig14_continuous_predictors_scatter_grid.png` | `REPORT_EVIDENCE_GUIDE.md` (§4.2) | **VERIFIED** (Covers thermal dominance, `temp`–`atemp` collinearity $r=0.9917$, humidity confounding, wind deterrence, and `casual`/`registered` leakage avoidance) | None |
| **REQ-5a** | **5a. Multiple Linear Regression — Theoretical Background:**<br>- Study and explain the theory of Multiple Linear Regression. | — | — | `REPORT_EVIDENCE_GUIDE.md` (§5.1)<br>`00_dataset_and_documentation/STATISTICAL_DECISIONS.md` (§5) | **VERIFIED** (Matrix equation, OLS estimator, Gauss-Markov assumptions, VIF, robust SEs, and $R^2$/Adj-$R^2$/MAE/RMSE defined) | None |
| **REQ-5b** | **5b. Multiple Linear Regression — Model Development and Evaluation:**<br>- Build and evaluate a Multiple Linear Regression model to predict a target variable (`cnt`) based on multiple independent variables. | `05_multiple_linear_regression/tables/regression_model_comparison.csv`<br>`05_multiple_linear_regression/tables/regression_ols_coefficients.csv`<br>`05_multiple_linear_regression/tables/regression_vif_diagnostics.csv`<br>`05_multiple_linear_regression/tables/regression_residual_diagnostics.csv`<br>`05_multiple_linear_regression/tables/train_predictions.csv`<br>`05_multiple_linear_regression/tables/test_predictions.csv` | `05_multiple_linear_regression/figures/fig15_regression_actual_vs_predicted.png`<br>`05_multiple_linear_regression/figures/fig16_regression_residuals_vs_fitted.png`<br>`05_multiple_linear_regression/figures/fig17_regression_residual_qq_hist.png`<br>`05_multiple_linear_regression/figures/fig18_regression_temporal_predictions_errors.png` | `REPORT_EVIDENCE_GUIDE.md` (§5.2 & §6)<br>`00_dataset_and_documentation/STATISTICAL_DECISIONS.md` (§5)<br>`00_dataset_and_documentation/FIGURE_REGISTER.md` (Figs 15–18) | **VERIFIED** (Chronological 80/20 split $n=584/147$, anti-leakage allowlist, VIF audit, IID/HC3/HAC coefficients, train/test metrics, and 4 diagnostic plots exported) | None |

---

## 2. Complete Inventory of Files in `report_evidence_package/` (63 Files Total)

### Root Guidance Documents (2 Files)
1. `REPORT_EVIDENCE_GUIDE.md` — Comprehensive methodology, exact statistical results, tables, figure references, and interpretations for all five requirements.
2. `EVIDENCE_MANIFEST.md` — This requirement-to-file traceability manifest and directory catalog.

### Folder `00_dataset_and_documentation/` (11 Files)
3. `00_dataset_and_documentation/day.csv` — Raw UCI Bike Sharing daily dataset ($731 \times 16$, $57,569$ bytes).
4. `00_dataset_and_documentation/Readme.txt` — Official UCI dataset documentation and variable definitions.
5. `00_dataset_and_documentation/dataset_audit.json` — Automated SHA-256 verification, dimension check, continuity check, and anomaly log.
6. `00_dataset_and_documentation/results.json` — Complete machine-readable JSON dictionary of all computed statistical results.
7. `00_dataset_and_documentation/REPORT_ASSIGNMENTS.md` — Original final-term assignment prompt.
8. `00_dataset_and_documentation/DATA_DICTIONARY.md` — Detailed variable codebook, physical unit conversions, and `season` calendar boundary documentation.
9. `00_dataset_and_documentation/RESEARCH_DESIGN.md` — Pre-declared research questions, hypothesis definitions, and observational limitations.
10. `00_dataset_and_documentation/STATISTICAL_DECISIONS.md` — Statistical engineering decisions (outlier policy, overdispersion, anti-leakage rules, robust standard errors).
11. `00_dataset_and_documentation/FIGURE_REGISTER.md` — Catalog of all 18 figures (`fig01`–`fig18`) with chart types and analytical purposes.
12. `00_dataset_and_documentation/REFERENCES.md` — Authoritative academic and software references with DOIs.
13. `00_dataset_and_documentation/RUBRIC_TRACEABILITY.md` — 100-point grading rubric traceability matrix.

### Folder `01_exploratory_data_analysis/` (12 CSV Tables + 5 PNG Figures = 17 Files)
14. `01_exploratory_data_analysis/tables/data_dictionary_summary.csv`
15. `01_exploratory_data_analysis/tables/eda_continuous_summary.csv`
16. `01_exploratory_data_analysis/tables/eda_categorical_frequencies.csv`
17. `01_exploratory_data_analysis/tables/eda_group_by_season.csv`
18. `01_exploratory_data_analysis/tables/eda_group_by_weathersit.csv`
19. `01_exploratory_data_analysis/tables/eda_group_by_workingday.csv`
20. `01_exploratory_data_analysis/tables/eda_group_by_year.csv`
21. `01_exploratory_data_analysis/tables/eda_group_by_holiday.csv`
22. `01_exploratory_data_analysis/tables/eda_weather_by_workingday.csv`
23. `01_exploratory_data_analysis/tables/eda_outlier_audit.csv`
24. `01_exploratory_data_analysis/tables/eda_outlier_handling_sensitivity.csv`
25. `01_exploratory_data_analysis/tables/eda_data_quality_anomalies.csv`
26. `01_exploratory_data_analysis/figures/fig01_daily_rentals_timeseries.png`
27. `01_exploratory_data_analysis/figures/fig02_cnt_distribution_hist_kde.png`
28. `01_exploratory_data_analysis/figures/fig03_cnt_boxplot_by_season.png`
29. `01_exploratory_data_analysis/figures/fig04_temp_vs_cnt_scatter.png`
30. `01_exploratory_data_analysis/figures/fig05_mean_cnt_by_weather_workday_ci.png`

### Folder `02_probability_distributions/` (5 CSV Tables + 3 PNG Figures = 8 Files)
31. `02_probability_distributions/tables/probability_distribution_summary.csv`
32. `02_probability_distributions/tables/cnt_overdispersion_and_fit.csv`
33. `02_probability_distributions/tables/cnt_candidate_distributions_comparison.csv`
34. `02_probability_distributions/tables/temp_distribution_diagnostics.csv`
35. `02_probability_distributions/tables/weather_variables_candidate_fits.csv`
36. `02_probability_distributions/figures/fig06_cnt_distribution_diagnostics.png`
37. `02_probability_distributions/figures/fig07_temp_distribution_diagnostics.png`
38. `02_probability_distributions/figures/fig08_hum_windspeed_distributions.png`

### Folder `03_hypothesis_testing/` (6 CSV Tables + 3 PNG Figures = 9 Files)
39. `03_hypothesis_testing/tables/hypothesis_tests_summary.csv`
40. `03_hypothesis_testing/tables/h1_ttest_workingday.csv`
41. `03_hypothesis_testing/tables/h2_anova_omnibus_and_groups.csv`
42. `03_hypothesis_testing/tables/h2_anova_season_posthoc.csv`
43. `03_hypothesis_testing/tables/h3_chisq_contingency_table.csv`
44. `03_hypothesis_testing/tables/h3_chisq_omnibus_and_robustness.csv`
45. `03_hypothesis_testing/figures/fig09_h1_workingday_ttest.png`
46. `03_hypothesis_testing/figures/fig10_h2_season_anova.png`
47. `03_hypothesis_testing/figures/fig11_h3_weathersit_highdemand_chisq.png`

### Folder `04_correlation_analysis/` (4 CSV Tables + 3 PNG Figures = 7 Files)
48. `04_correlation_analysis/tables/pearson_correlation_matrix.csv`
49. `04_correlation_analysis/tables/spearman_correlation_matrix.csv`
50. `04_correlation_analysis/tables/correlation_pairwise_tests.csv`
51. `04_correlation_analysis/tables/extended_correlations_with_cnt.csv`
52. `04_correlation_analysis/figures/fig12_pearson_correlation_heatmap.png`
53. `04_correlation_analysis/figures/fig13_spearman_correlation_heatmap.png`
54. `04_correlation_analysis/figures/fig14_continuous_predictors_scatter_grid.png`

### Folder `05_multiple_linear_regression/` (6 CSV Tables + 4 PNG Figures = 10 Files)
55. `05_multiple_linear_regression/tables/regression_model_comparison.csv`
56. `05_multiple_linear_regression/tables/regression_ols_coefficients.csv`
57. `05_multiple_linear_regression/tables/regression_vif_diagnostics.csv`
58. `05_multiple_linear_regression/tables/regression_residual_diagnostics.csv`
59. `05_multiple_linear_regression/tables/train_predictions.csv`
60. `05_multiple_linear_regression/tables/test_predictions.csv`
61. `05_multiple_linear_regression/figures/fig15_regression_actual_vs_predicted.png`
62. `05_multiple_linear_regression/figures/fig16_regression_residuals_vs_fitted.png`
63. `05_multiple_linear_regression/figures/fig17_regression_residual_qq_hist.png`
64. `05_multiple_linear_regression/figures/fig18_regression_temporal_predictions_errors.png`
*(Total = 64 files inside `report_evidence_package/`)*
