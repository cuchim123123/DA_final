# Pre-Declared Research Design

**Project Title:** *Statistical Analysis and Visualization of Daily Bike-Rental Demand: Weather, Seasonality, Hypothesis Testing, and Multiple Linear Regression*

## 1. Study Context and Observational Unit

- **Dataset:** UCI Machine Learning Repository — *Bike Sharing Dataset* (`day.csv`), authored by Hadi Fanaee-T and Joao Gama (2013), DOI: `10.24432/C5W894`.
- **System Studied:** Capital Bikeshare metro bike-sharing system in Washington, D.C., United States, spanning January 1, 2011 through December 31, 2012 (731 consecutive calendar days).
- **Observational Unit:** One calendar day ($N = 731$). The hourly file (`hour.csv`) is strictly excluded to preserve a consistent daily observational unit throughout the study.
- **Primary Response Variable:** `cnt` — total daily bike rentals (sum of `casual` and `registered` user rentals).

## 2. Central Research Questions

1. **RQ1 (Descriptive & Distributional Structure):** What are the central tendency, dispersion, seasonal regimes, and anomaly patterns of daily bike-rental demand (`cnt`), and do classical parametric families (Poisson, Negative Binomial, Normal) adequately characterize `cnt` and normalized temperature (`temp`)?
2. **RQ2 (Workday vs. Non-Workday Demand — H1):** Do working days (`workingday = 1`) and non-working days (`workingday = 0`, comprising weekends and public holidays) differ in mean total daily bike rentals (`cnt`)?
3. **RQ3 (Seasonal Regime Differences — H2):** Does mean daily bike-rental demand (`cnt`) vary significantly across the four astronomical seasons (`season` $\in \{1, 2, 3, 4\}$), and which pairwise seasonal transitions drive this variation?
4. **RQ4 (Weather Condition vs. High-Demand Regime — H3):** Is the categorical daily weather situation (`weathersit`) statistically associated with achieving an above-median daily rental regime (`high_demand`)?
5. **RQ5 (Bivariate Linear & Monotonic Associations):** How strongly and in what direction do continuous meteorological indicators (`temp`, `atemp`, `hum`, `windspeed`) co-vary with `cnt` under linear (Pearson $r$) and rank-monotonic (Spearman $\rho$) assumptions, and how severe is collinearity between ambient temperature (`temp`) and feeling temperature (`atemp`)?
6. **RQ6 (Multivariate Modeling & Out-of-Sample Generalization):** How accurately can an Ordinary Least Squares (OLS) multiple linear regression model conditioned on meteorological, calendar, and structural predictors estimate unseen future daily demand under a strict chronological 80/20 train-test split without target leakage?

## 3. Pre-Declared Hypothesis Tests (Locked Prior to Execution)

To cover all three inferential frameworks mandated by the course rubric (independent-samples t-test, one-way ANOVA, and Chi-square test of independence), three primary hypotheses are pre-registered at a nominal significance level of $\alpha = 0.05$:

### Hypothesis Test H1: Welch Two-Sample t-Test on Working Day Status
- **Groups:** Working days (`workingday = 1`) vs. Non-working days (`workingday = 0`).
- **Null Hypothesis ($H_0$):** $\mu_{\text{workday}} = \mu_{\text{non-workday}}$ (mean daily total rentals are equal between working and non-working days).
- **Alternative Hypothesis ($H_1$):** $\mu_{\text{workday}} \neq \mu_{\text{non-workday}}$ (two-sided test).
- **Primary Estimator & Test:** Welch's independent two-sample t-test (which does not assume homoscedasticity), accompanied by Student's pooled-variance t-test and Mann-Whitney U test as sensitivity checks, Levene's test for equality of variances, 95% confidence interval for the mean difference, and Hedges' $g$ (plus Cohen's $d$) standardized effect size.
- **Substantive Rationale:** Commuter demand (registered users) peaks on working days whereas leisure demand (casual users) peaks on weekends and holidays; testing aggregate `cnt` reveals whether commuter volume offsets weekend recreational volume in total fleet utilization.

### Hypothesis Test H2: One-Way ANOVA Across Four Seasons
- **Groups:** Four meteorological/astronomical seasons encoded in `season` (1 = Spring/Winter-early-Spring per UCI codebook, 2 = Summer/Spring-Summer, 3 = Fall/Summer-Fall, 4 = Winter/Fall-Winter; exact UCI README definition and dates documented in `DATA_DICTIONARY.md`).
- **Null Hypothesis ($H_0$):** $\mu_1 = \mu_2 = \mu_3 = \mu_4$ (all four seasonal population means of `cnt` are equal).
- **Alternative Hypothesis ($H_1$):** At least one season has a different population mean $\mu_k$.
- **Primary Estimator & Test:** Classical ordinary one-way ANOVA $F$-test paired with Welch's heteroscedastic one-way ANOVA and non-parametric Kruskal-Wallis $H$-test when Levene's test or group residual checks indicate variance heterogeneity. Effect sizes reported via $\eta^2$ (eta-squared) and $\omega^2$ (omega-squared). Post-hoc pairwise comparisons conducted via Tukey's HSD (homoscedastic) and Games-Howell / Holm-adjusted Welch pairwise t-tests (heteroscedastic).

### Hypothesis Test H3: Chi-Square Test of Independence (Weather Condition vs. High-Demand Regime)
- **Variables:**
  - Categorical predictor: `weathersit` (1 = Clear/Partly cloudy, 2 = Mist/Cloudy, 3 = Light snow/Light rain/Thunderstorm, 4 = Heavy rain/Ice pellets/Snow+Fog).
  - Categorical outcome (exploratory only): `high_demand` $= \mathbb{I}(\text{cnt} > \text{median}(\text{cnt}))$, dichotomizing days into `High Demand` (above sample median) and `Low/Moderate Demand` (at or below sample median).
- **Quarantine Rule:** `high_demand` is derived from the response `cnt` solely for this exploratory contingency table analysis and is **strictly banned** from entering the regression predictor matrix $X$.
- **Null Hypothesis ($H_0$):** Daily weather situation (`weathersit`) and demand regime (`high_demand`) are statistically independent ($P(\text{High Demand} \mid \text{weathersit} = k) = P(\text{High Demand})$ for all $k$).
- **Alternative Hypothesis ($H_1$):** Weather situation and demand regime are associated.
- **Primary Estimator & Test:** Pearson's $\chi^2$ test of independence with Cramér's $V$ effect size. Because Cochran's rule requires at least 80% of cells to have expected counts $\ge 5$ and no cell $< 1$ (and category 4 in `day.csv` is known to be rare or empty), the analysis explicitly audits expected cell counts and executes a pre-specified sensitivity test merging sparse adverse categories or applying Fisher's exact / Monte Carlo permutation test where appropriate.

## 4. Observational and Temporal Limitations

1. **Non-Causality:** Because weather, season, and calendar states are observed rather than randomized, statistically significant differences or regression coefficients represent observational associations and conditional expectations, not causal effects.
2. **Serial Correlation:** Daily counts $y_t$ exhibit positive autocorrelation across consecutive days. Classical IID tests ($t$, ANOVA, $\chi^2$, IID OLS standard errors) may understate standard errors; therefore, time-series dependence caveats are explicitly reported and Newey-West (HAC) / White (HC3) robust standard errors are computed in the regression chapter.
3. **Observed vs. Forecast Weather:** In `day.csv`, meteorological variables represent realized daily summaries. A model trained on realized weather estimates *conditional demand given weather* and would require weather forecasts (introducing forecast error) for ex-ante operational dispatch.
