# Statistical & Methodological Decision Log

This document records the statistical engineering decisions made to ensure full compliance with the 100-point rubric and academic rigor.

## 1. Data Hygiene, Missingness, and Outlier Policy

1. **No Fabricated Missingness:** If `data/raw/day.csv` contains zero missing values across all 731 rows and 16 columns, we report the verified zero-missingness audit and do **not** artificially inject `NaN` values to demonstrate imputation.
2. **Structural Identity Verification:** Every observation must satisfy `cnt == casual + registered`. This exact accounting identity is verified programmatically in `src/load_validate.py` and `tests/test_data_integrity.py`.
3. **Outlier Detection & Retention:**
   - Outliers in continuous variables (`cnt`, `temp`, `atemp`, `hum`, `windspeed`) are flagged using Tukey's $1.5 \times \text{IQR}$ fences and standardized $|z| > 3$ thresholds.
   - Real extreme meteorological or operational events (e.g., Hurricane Sandy on October 29, 2012, where `cnt = 22`, or days with `hum = 0.0` in sensor logs) are documented and distinguished from data corruption.
   - Valid extreme observations are **retained** in the primary analysis rather than deleted to artificially inflate $R^2$ or alter p-values; where physical sensor anomalies (such as `hum = 0.0` on 2011-03-10) occur, both full-sample results and sensitivity checks are documented transparently.

## 2. Probability Distribution Analysis Protocol

1. **Discrete Count Variable (`cnt`):**
   - Because `cnt` is a non-negative integer count ($\text{cnt} \in \mathbb{Z}_{\ge 0}$), we first evaluate the theoretical Poisson assumption ($\text{Var}(Y) = \mathbb{E}[Y]$) via the index of dispersion $D = s^2 / \bar{y}$ and the dispersion test statistic $(n-1)s^2/\bar{y} \sim \chi^2_{n-1}$.
   - Pooled multi-season daily counts exhibit severe overdispersion ($s^2 \gg \bar{y}$). We therefore evaluate a Negative Binomial discrete distribution (which models overdispersion via a variance quadratic in the mean) alongside a continuous Gaussian (Normal) approximation via method-of-moments/MLE, reporting AIC/BIC, log-likelihood, Shapiro-Wilk, D'Agostino-Pearson $K^2$, Anderson-Darling, and Lilliefors / parametric bootstrap KS diagnostics rather than a naive plug-in KS p-value.
2. **Bounded Continuous Meteorological Variable (`temp`):**
   - `temp` is normalized ambient Celsius temperature bounded in $[0, 1]$. We evaluate its empirical kernel density estimate (KDE), skewness, excess kurtosis, Q-Q plot against a Normal distribution, and multimodal/bimodal seasonal mixture behavior (warm vs. cold seasons), comparing a Normal fit and Beta fit on $(0, 1)$.
3. **Supplemental Context Variables (`hum`, `windspeed`):**
   - Analyzed to illustrate skewness in windspeed and left-tail anomalies in humidity (`hum = 0`).

## 3. Hypothesis Testing & Multiple-Comparison Protocol

1. **Nominal Alpha:** $\alpha = 0.05$ (two-sided for $t$-tests; upper-tail for $F$ and $\chi^2$ omnibus tests).
2. **Assumption Checks:**
   - Normality of group residuals: Shapiro-Wilk and D'Agostino-Pearson $K^2$ tests, coupled with Central Limit Theorem justification for large group sizes ($n_k > 170$).
   - Homogeneity of variance: Levene's test (median-centered Brown-Forsythe and mean-centered variants).
   - Contingency expected frequencies: Minimum expected cell count and proportion of cells with expected count $< 5$ (Cochran's criterion).
3. **Multiple Testing Control:** Across the family of three primary omnibus hypothesis tests (H1, H2, H3), both unadjusted exact p-values and **Holm-Bonferroni adjusted p-values** are reported. Within H2 seasonal post-hoc tests, Tukey's HSD and Games-Howell / Holm-corrected Welch p-values control family-wise error rate across all $\binom{4}{2} = 6$ seasonal pairs.

## 4. Correlation Analysis Protocol

1. **Continuous Scope Only:** Pearson ($r$) and Spearman ($\rho$) correlation matrices are computed strictly on meaningful continuous variables (`cnt`, `temp`, `atemp`, `hum`, `windspeed`). Nominal integer codes (`season`, `weathersit`, `mnth`, `weekday`) are excluded from continuous correlation matrices to prevent scale-type fallacies.
2. **Collinearity Diagnostic:** The near-perfect correlation between `temp` and `atemp` ($r > 0.99$) is quantified here and used to justify dropping `atemp` from the primary OLS specification (with VIF verification in Phase 6).

## 5. Multiple Linear Regression & Anti-Leakage Protocol

1. **Forbidden Features (Target Leakage Prevention):**
   - `casual` and `registered` are components of `cnt` (`cnt = casual + registered`) and are strictly excluded.
   - `cnt` (the target), `high_demand` (target-derived binary indicator from H3), `instant` (sequential row index proxy for time/row order), and `dteday` (used only for chronological sorting and date-range indexing, never as a raw feature) are excluded from the predictor matrix $X$.
2. **Predictor Allowlist:**
   - Continuous predictors: `temp`, `hum`, `windspeed` (`atemp` excluded in the primary specification due to collinearity with `temp`, confirmed via a full-feature vs. reduced-feature VIF table; `mnth` excluded from the primary parsimonious model to avoid collinearity with `season`).
   - Binary/indicator predictors: `yr` (0 = 2011, 1 = 2012, capturing system expansion between year 1 and year 2), `holiday`, `workingday`.
   - Categorical predictors (One-Hot Encoded with `drop='first'` reference categories): `season` (reference: Season 1), `weathersit` (reference: Clear/Partly Cloudy `weathersit=1`; handling any sparse/unseen category safely via `OneHotEncoder(drop='first', handle_unknown='ignore')`).
3. **Chronological Train/Test Split (80% / 20%):**
   - Sorted strictly by `dteday` ascending:
     - **Training Set (first 80%):** $n_{\text{train}} = 584$ days (`2011-01-01` to `2012-08-06`).
     - **Hold-Out Test Set (final 20%):** $n_{\text{test}} = 147$ days (`2012-08-07` to `2012-12-31`).
   - Random shuffling is **prohibited** so that evaluation reflects genuine forward-in-time prediction.
4. **Inference & Covariance Robustness:**
   - In addition to classical IID OLS standard errors on the training set, we compute **HC3 heteroscedasticity-robust** and **Newey-West HAC (lag = 7 days)** standard errors, $t$-statistics, and 95% confidence intervals via `statsmodels` to account for residual heteroscedasticity and weekly serial correlation.
