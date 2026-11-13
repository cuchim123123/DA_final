# Complete Academic Report Evidence Guide (`REPORT_EVIDENCE_GUIDE.md`)

## Purpose of This Document
This guide is a self-contained, authoritative reference designed for an AI assistant or academic author tasked with completing the final-term project report in Microsoft Word. Every statistic, test result, table reference, and figure reference in this document is computed deterministically from the official **UCI Bike Sharing Dataset (`day.csv`, $N = 731, p = 16$)** and corresponds 1:1 to the files inside `report_evidence_package/`.

All internal file paths below are **relative to the root of `report_evidence_package/`**.

---

## 0. General Requirements & Dataset Provenance

### 0.1 Specific Requirement Being Addressed
- Select **one real-world dataset** from an open source (e.g., UCI Machine Learning Repository or Kaggle) and use it consistently throughout all five analytical sections.
- The dataset must contain **at least 500 rows and 5 variables**.
- The dataset must be different from the dataset used in the midterm assignment.

### 0.2 Confirmed Numerical & Provenance Findings
- **Dataset Title:** Bike Sharing Dataset — Daily Aggregated Log (`day.csv`).
- **Repository & DOI:** UCI Machine Learning Repository (<https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset>), DOI: `10.24432/C5W894`.
- **Primary Academic Citation:** Fanaee-T, H., & Gama, J. (2013). Event labeling combining ensemble detectors and background knowledge. *Progress in Artificial Intelligence*, 2(2–3), 113–127. Springer. <https://doi.org/10.1007/s13748-013-0040-3>
- **Operational System & Location:** Capital Bikeshare metro bike-sharing network, Washington, D.C., USA (weather data from Freemeteo; holiday calendar from D.C. Department of Human Resources).
- **Observational Unit & Coverage:** One calendar day ($N = 731$ consecutive days from `2011-01-01` to `2012-12-31`: $365$ days in 2011 + $366$ days in leap year 2012).
- **Dimensions:** **$731$ rows $\times$ $16$ columns** (exceeds the $\ge 500$ rows and $\ge 5$ variables threshold).
- **Cryptographic Integrity (SHA-256):**
  - `00_dataset_and_documentation/day.csv` ($57,569$ bytes): `a6bcf826782d3c0fbfdcbeead17cd0884185a0dafe8ff10cd48a874ee7ba18be`
  - `00_dataset_and_documentation/Readme.txt` ($5,607$ bytes): `b92c8628622948bf0828c43a1b315d1517c3d7fd63654730d0dea379b8e88175`

### 0.3 Supporting Package Files
- Raw Dataset: `00_dataset_and_documentation/day.csv`
- Official UCI Codebook: `00_dataset_and_documentation/Readme.txt`
- Automated Dataset Audit JSON: `00_dataset_and_documentation/dataset_audit.json`
- Master Statistical Results JSON: `00_dataset_and_documentation/results.json`
- Detailed Variable Codebook: `00_dataset_and_documentation/DATA_DICTIONARY.md`
- Verified Bibliography: `00_dataset_and_documentation/REFERENCES.md`

### 0.4 Important Cautions & Unresolved Administrative Items
- **Granularity Rule:** The UCI archive also contains `hour.csv` ($17,379$ hourly rows). This study analyzes **exclusively `day.csv` ($N = 731$)** so that the observational unit remains strictly one calendar day across all five requirements.
- **Unresolved Administrative Check (Student Action Required):** Confirm before final submission that the UCI Bike Sharing dataset was not used in the student's midterm assignment, and fill in student name/ID placeholders in the report template.

---

## 1. Requirement 1: Exploratory Data Analysis (EDA)

### 1.1 Subrequirement 1.1 — Summarize Dataset Information

#### Specific Question / Requirement
- Examine the number of records, number of variables, and data type of each variable.
- Handle missing data and duplicate records (if any).

#### Statistical Methodology Applied
- Programmatic schema inspection of all $16$ columns (`dtype`, statistical measurement scale, domain bounds, unique value counts, and physical de-normalization rules per `Readme.txt`).
- Full-matrix missingness audit across all $731 \times 16 = 11,696$ cells (`isna().sum()`).
- Exact row-level duplicate check (`duplicated().sum()`), primary key uniqueness check on `instant` and `dteday`, chronological continuity check (`pd.date_range('2011-01-01', '2012-12-31')`), and structural accounting identity check (`cnt == casual + registered`).

#### Confirmed Numerical Findings
- **Dimensions:** $731$ records (rows) and $16$ variables (columns).
- **Missing Values:** **$0$ missing cells ($0.00\%$)** across all $16$ columns ($11,696$ cells verified). No imputation or row deletion is required.
- **Duplicate Records:** **$0$ duplicate rows** and **$0$ duplicate calendar dates** (`instant` spans $1..731$ with $731$ unique integers; `dteday` spans `2011-01-01` to `2012-12-31` with $731$ unique consecutive dates and $0$ date gaps).
- **Accounting Invariant:** `cnt = casual + registered` holds with **$0$ violations** across all $731$ rows.
- **Complete 16-Variable Schema & Summary (`01_exploratory_data_analysis/tables/data_dictionary_summary.csv`):**

| # | Column | Python `dtype` | Statistical Scale | Missing | Unique | Min | Max | Mean | SD | Median | Domain & Physical Normalization (`Readme.txt`) |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `instant` | `int64` | Identifier / Index | 0 | 731 | 1 | 731 | 366.00 | 211.17 | 366.0 | Sequential day index ($1..731$). Excluded from modeling to prevent time-index leakage. |
| 2 | `dteday` | `str` (date) | Temporal Index | 0 | 731 | `2011-01-01` | `2012-12-31` | — | — | — | ISO calendar date. Used for chronological 80/20 split. |
| 3 | `season` | `int64` | Nominal Categorical | 0 | 4 | 1 | 4 | 2.50 | 1.11 | 3.0 | `1`: Spring ($n=181$), `2`: Summer ($n=184$), `3`: Fall ($n=188$), `4`: Winter ($n=178$). |
| 4 | `yr` | `int64` | Binary Indicator | 0 | 2 | 0 | 1 | 0.5007 | 0.5003 | 1.0 | `0`: 2011 ($n=365$, $49.93\%$), `1`: 2012 ($n=366$, $50.07\%$). |
| 5 | `mnth` | `int64` | Cyclic Discrete | 0 | 12 | 1 | 12 | 6.52 | 3.45 | 7.0 | Calendar month (`1 = Jan` to `12 = Dec`, $57$–$62$ days each). |
| 6 | `holiday` | `int64` | Binary Indicator | 0 | 2 | 0 | 1 | 0.0287 | 0.1672 | 0.0 | `1`: Public holiday ($n=21$, $2.87\%$), `0`: Regular day ($n=710$, $97.13\%$). |
| 7 | `weekday` | `int64` | Cyclic Categorical | 0 | 7 | 0 | 6 | 3.00 | 2.00 | 3.0 | Day of week (`0 = Sun` to `6 = Sat`, $104$–$105$ days each). |
| 8 | `workingday` | `int64` | Binary Indicator | 0 | 2 | 0 | 1 | 0.6840 | 0.4652 | 1.0 | `1`: Workday Mon–Fri non-holiday ($n=500$, $68.40\%$), `0`: Weekend/Holiday ($n=231$, $31.60\%$). |
| 9 | `weathersit` | `int64` | Ordinal Categorical | 0 | 3 | 1 | 3 | 1.40 | 0.54 | 1.0 | `1`: Clear/Partly cloudy ($n=463$, $63.34\%$), `2`: Mist/Cloudy ($n=247$, $33.79\%$), `3`: Light Snow/Rain ($n=21$, $2.87\%$), `4`: Heavy Rain/Ice ($n=0$, $0.00\%$). |
| 10 | `temp` | `float64` | Continuous Ratio | 0 | 499 | 0.0591 | 0.8617 | 0.4954 | 0.1831 | 0.4983 | Normalized temperature in $[0,1]$, divided by $41^\circ\text{C}$ ($\text{temp}_{^\circ\text{C}} = 41 \times \text{temp}$). |
| 11 | `atemp` | `float64` | Continuous Ratio | 0 | 690 | 0.0791 | 0.8409 | 0.4744 | 0.1630 | 0.4867 | Normalized feeling temperature in $[0,1]$, divided by $50^\circ\text{C}$ ($\text{atemp}_{^\circ\text{C}} = 50 \times \text{atemp}$). |
| 12 | `hum` | `float64` | Continuous Ratio | 0 | 595 | 0.0000 | 0.9725 | 0.6279 | 0.1424 | 0.6267 | Normalized relative humidity in $[0,1]$, divided by $100\%$ ($\text{hum}_{\%} = 100 \times \text{hum}$). |
| 13 | `windspeed` | `float64` | Continuous Ratio | 0 | 650 | 0.0224 | 0.5075 | 0.1905 | 0.0775 | 0.1810 | Normalized wind speed in $[0,1]$, divided by $67\text{ km/h}$ ($\text{wind}_{\text{km/h}} = 67 \times \text{windspeed}$). |
| 14 | `casual` | `int64` | Discrete Count | 0 | 606 | 2 | 3,410 | 848.18 | 686.62 | 713.0 | Daily rentals by casual (non-registered) users ($18.83\%$ of total rides). |
| 15 | `registered` | `int64` | Discrete Count | 0 | 679 | 20 | 6,946 | 3,656.17 | 1,560.26 | 3,662.0 | Daily rentals by registered subscribers ($81.17\%$ of total rides). |
| 16 | `cnt` | `int64` | Discrete Count (Target) | 0 | 696 | 22 | 8,714 | 4,504.35 | 1,937.21 | 4,548.0 | Total daily bike rentals (`cnt = casual + registered`). |

- **Physical Sensor Anomalies Detected During Data Quality Audit (`01_exploratory_data_analysis/tables/eda_data_quality_anomalies.csv`):**
  1. **Zero Humidity Sensor Dropout (`2011-03-10`, `instant = 69`):** Recorded `hum = 0.0000` ($0\%$ humidity, $z = -4.4085$) on a day classified as `weathersit = 3` (Light Rain/Snow, `cnt = 623`), indicating a weather-station hygrometer dropout rather than true $0\%$ atmospheric humidity.
  2. **Feeling-Temperature Discrepancy (`2012-08-17`, `instant = 595`):** Recorded `temp = 0.7233` ($29.66^\circ\text{C}$) alongside `atemp = 0.2424` ($12.12^\circ\text{C}$), a discrepancy of $|\text{temp} - \text{atemp}| = 0.4809$ (`cnt = 7,148`).

#### Supporting Package Files
- `01_exploratory_data_analysis/tables/data_dictionary_summary.csv`
- `01_exploratory_data_analysis/tables/eda_categorical_frequencies.csv`
- `01_exploratory_data_analysis/tables/eda_data_quality_anomalies.csv`
- `00_dataset_and_documentation/dataset_audit.json`
- `00_dataset_and_documentation/DATA_DICTIONARY.md`

---

### 1.2 Subrequirement 1.2 — Descriptive Statistical Analysis & Visualization

#### Specific Question / Requirement
- Calculate descriptive statistics such as mean, median, standard deviation, and quartiles.
- Visualize the data using appropriate charts (**at least 3 different types of charts**) to identify trends in the data.
- Explain the reasons for selecting each chart type.

#### Statistical Methodology Applied
- Parametric and non-parametric descriptive statistics computed for all $7$ continuous/count variables (`cnt`, `casual`, `registered`, `temp`, `atemp`, `hum`, `windspeed`) in both normalized and physical units: Mean, Standard Deviation (SD), Variance, Standard Error of Mean (SE), 95% CI of Mean, 10% Trimmed Mean, Empirical Mode, Min, $Q_1$ (25th percentile), Median ($Q_2$, 50th percentile), $Q_3$ (75th percentile), Max, Range, Interquartile Range ($\text{IQR} = Q_3 - Q_1$), Median Absolute Deviation ($\text{MAD}$), Coefficient of Variation ($\text{CV}\%$), Skewness, and Excess Kurtosis.
- Stratified subgroup summaries computed across `season`, `yr`, `weathersit`, `workingday`, `holiday`, and crossed `weathersit x workingday`.
- Five distinct chart types generated at 300 DPI (exceeding the minimum of 3 chart types):
  1. Multi-layer Time-Series Line Plot (`fig01`)
  2. Histogram + Kernel Density Estimate (KDE) + Year-Stratified Boxplot Rug (`fig02`)
  3. Boxplot + Jittered Strip Plot across Seasons (`fig03`)
  4. Multivariate Scatter Plot with OLS & LOWESS Curves (`fig04`)
  5. Grouped Bar Chart with 95% $t$-Confidence Intervals (`fig05`)

#### Confirmed Numerical Findings
- **Continuous Variable Descriptive Statistics (`01_exploratory_data_analysis/tables/eda_continuous_summary.csv`):**

| Variable | Unit | $n$ | Mean | SD | Variance | Min | $Q_1$ (25%) | Median (50%) | $Q_3$ (75%) | Max | IQR | CV (%) | Skewness | Excess Kurtosis | Physical Mean (SD) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `cnt` | bikes/day | 731 | 4,504.35 | 1,937.21 | 3,752,788.21 | 22.00 | 3,152.00 | 4,548.00 | 5,956.00 | 8,714.00 | 2,804.00 | 43.01% | -0.0474 | -0.8119 | 4,504.35 (1,937.21) bikes/day |
| `registered` | bikes/day | 731 | 3,656.17 | 1,560.26 | 2,434,399.96 | 20.00 | 2,497.00 | 3,662.00 | 4,776.50 | 6,946.00 | 2,279.50 | 42.67% | +0.0437 | -0.7131 | 3,656.17 (1,560.26) bikes/day |
| `casual` | bikes/day | 731 | 848.18 | 686.62 | 471,450.44 | 2.00 | 315.50 | 713.00 | 1,096.00 | 3,410.00 | 780.50 | 80.95% | +1.2665 | +1.3221 | 848.18 (686.62) bikes/day |
| `temp` | norm $[0,1]$ | 731 | 0.4954 | 0.1831 | 0.0335 | 0.0591 | 0.3371 | 0.4983 | 0.6554 | 0.8617 | 0.3183 | 36.95% | -0.0545 | -1.1189 | $20.31^\circ\text{C}$ ($7.51^\circ\text{C}$) |
| `atemp` | norm $[0,1]$ | 731 | 0.4744 | 0.1630 | 0.0266 | 0.0791 | 0.3378 | 0.4867 | 0.6086 | 0.8409 | 0.2708 | 34.35% | -0.1311 | -0.9851 | $23.72^\circ\text{C}$ ($8.15^\circ\text{C}$) |
| `hum` | norm $[0,1]$ | 731 | 0.6279 | 0.1424 | 0.0203 | 0.0000 | 0.5200 | 0.6267 | 0.7302 | 0.9725 | 0.2102 | 22.68% | -0.0698 | -0.0645 | $62.79\%$ ($14.24\%$) |
| `windspeed` | norm $[0,1]$ | 731 | 0.1905 | 0.0775 | 0.0060 | 0.0224 | 0.1349 | 0.1810 | 0.2332 | 0.5075 | 0.0983 | 40.68% | +0.6773 | +0.4109 | $12.76\text{ km/h}$ ($5.19\text{ km/h}$) |

- **Subgroup Descriptive Breakdowns (`01_exploratory_data_analysis/tables/eda_group_by_year.csv`, `01_exploratory_data_analysis/tables/eda_group_by_season.csv`, `01_exploratory_data_analysis/tables/eda_group_by_weathersit.csv`, `01_exploratory_data_analysis/tables/eda_group_by_workingday.csv`, `01_exploratory_data_analysis/tables/eda_group_by_holiday.csv`, and `01_exploratory_data_analysis/tables/eda_weather_by_workingday.csv`):**
  - **By Year (`yr`):**
    - `2011` (`yr = 0`, $n = 365$, $49.93\%$): Mean $= 3,405.76$, SD $= 1,378.75$, Median $= 3,740.00$, IQR $= 2,454.00$, Range $= [431, 6,043]$.
    - `2012` (`yr = 1`, $n = 366$, $50.07\%$): Mean $= 5,599.93$, SD $= 1,788.67$, Median $= 5,927.00$, IQR $= 2,642.25$, Range $= [22, 8,714]$.
    - **Year-over-Year Growth:** $+2,194.17$ bikes/day (**$+64.43\%$** increase in mean daily ridership).
  - **By Season (`season`):**
    - `Season 1: Spring (Dec 21–Mar 20)` ($n = 181$, $24.76\%$): Mean $= 2,604.13$, SD $= 1,399.94$, Median $= 2,209.00$, IQR $= 1,918.00$, 95% CI $= [2,398.80, 2,809.46]$.
    - `Season 2: Summer (Mar 21–Jun 20)` ($n = 184$, $25.17\%$): Mean $= 4,992.33$, SD $= 1,695.98$, Median $= 4,941.50$, IQR $= 2,374.00$, 95% CI $= [4,745.65, 5,239.02]$.
    - `Season 3: Fall (Jun 21–Sep 22)` ($n = 188$, $25.72\%$): Mean $= 5,644.30$, SD $= 1,459.80$, Median $= 5,353.50$, IQR $= 2,342.75$, 95% CI $= [5,434.27, 5,854.33]$.
    - `Season 4: Winter (Sep 23–Dec 20)` ($n = 178$, $24.35\%$): Mean $= 4,728.16$, SD $= 1,699.62$, Median $= 4,634.50$, IQR $= 2,009.00$, 95% CI $= [4,476.76, 4,979.56]$.
  - **By Weather Situation (`weathersit`):**
    - `1: Clear / Partly Cloudy` ($n = 463$, $63.34\%$): Mean $= 4,876.79$, SD $= 1,879.48$, Median $= 4,844.00$, IQR $= 2,822.00$.
    - `2: Mist / Cloudy` ($n = 247$, $33.79\%$): Mean $= 4,035.86$ ($-17.24\%$ vs. Clear), SD $= 1,809.11$, Median $= 4,040.00$, IQR $= 2,583.00$.
    - `3: Light Snow / Light Rain` ($n = 21$, $2.87\%$): Mean $= 1,803.29$ ($-63.02\%$ vs. Clear), SD $= 1,240.28$, Median $= 1,817.00$, IQR $= 1,719.00$.
    - `4: Heavy Rain / Ice Pellets` ($n = 0$, $0.00\%$): Unobserved at the daily aggregation level.
  - **By Working Day (`workingday`):**
    - `0: Non-Working Day` ($n = 231$, $31.60\%$): Mean $= 4,330.17$, SD $= 2,052.14$, Median $= 4,459.00$, IQR $= 3,197.00$.
    - `1: Working Day` ($n = 500$, $68.40\%$): Mean $= 4,584.82$, SD $= 1,878.42$, Median $= 4,582.00$, IQR $= 2,643.25$.
  - **By Public Holiday (`holiday`):**
    - `0: Regular Day` ($n = 710$, $97.13\%$): Mean $= 4,527.10$, SD $= 1,929.01$, Median $= 4,558.00$, IQR $= 2,718.75$.
    - `1: Public Holiday` ($n = 21$, $2.87\%$): Mean $= 3,735.00$, SD $= 2,103.35$, Median $= 3,351.00$, IQR $= 4,083.00$.

#### Exported Figures, Selection Rationale, and Trend Interpretations
1. **Figure 1 (`01_exploratory_data_analysis/figures/fig01_daily_rentals_timeseries.png`):**
   - **Chart Type:** Multi-layer Time-Series Line Plot with 30-day rolling mean, chronological 80/20 split boundary (`2012-08-07`), and extreme-event annotations.
   - **Why Selected:** A continuous sequential line plot is uniquely suited to reveal multi-year secular growth, annual seasonal oscillation, and single-day exogenous shocks across $731$ ordered days.
   - **Trend Identified:** Two full seasonal waves peak in June–September and trough in January–February, superimposed on a $+64.43\%$ structural upward shift from 2011 to 2012. Extreme dips correspond to severe weather events, notably Hurricane Sandy on `2012-10-29` (`cnt = 22`).
2. **Figure 2 (`01_exploratory_data_analysis/figures/fig02_cnt_distribution_hist_kde.png`):**
   - **Chart Type:** Histogram + Kernel Density Estimate (KDE) + Year-Stratified Boxplot Rug.
   - **Why Selected:** Displays the empirical probability density, central tendency (mean vs. median), dispersion, and regime shift between 2011 and 2012.
   - **Trend Identified:** Pooled `cnt` is nearly symmetric ($\text{skewness} = -0.0474$, $\text{mean} = 4,504.35 \approx \text{median} = 4,548.00$) but flat-topped (platykurtic, $\text{excess kurtosis} = -0.8119$) because it mixes the lower-volume 2011 distribution (median $3,740$) with the higher-volume 2012 distribution (median $5,927$).
3. **Figure 3 (`01_exploratory_data_analysis/figures/fig03_cnt_boxplot_by_season.png`):**
   - **Chart Type:** Boxplot with Jittered Strip Plot across the four seasons.
   - **Why Selected:** Summarizes non-parametric five-number summaries ($Q_1$, median, $Q_3$, whiskers) while showing the exact underlying daily points ($n = 178..188$ per group) to expose within-season spread and multi-modality.
   - **Trend Identified:** `Season 1 (Dec 21–Mar 20)` has sharply lower ridership (median $2,209.0$) than `Season 2` ($4,941.5$), `Season 3` ($5,353.5$), and `Season 4` ($4,634.5$).
4. **Figure 4 (`01_exploratory_data_analysis/figures/fig04_temp_vs_cnt_scatter.png`):**
   - **Chart Type:** Multivariate Scatter Plot of `temp` vs. `cnt` colored by `season` with OLS linear and LOWESS non-parametric curves.
   - **Why Selected:** Directly visualizes continuous bivariate co-variation, seasonal clustering, and potential non-linear thermal saturation at extreme heat.
   - **Trend Identified:** Ridership rises strongly and nearly linearly with temperature from $5^\circ\text{C}$ to $27^\circ\text{C}$ ($r = +0.6275$), then plateaus and bends slightly downward when normalized `temp` exceeds $0.75$ ($\approx 31^\circ\text{C}$) due to heat discomfort.
5. **Figure 5 (`01_exploratory_data_analysis/figures/fig05_mean_cnt_by_weather_workday_ci.png`):**
   - **Chart Type:** Grouped Bar Chart of mean `cnt` across `weathersit` $\times$ `workingday` with 95% $t$-confidence intervals and sample size labels ($n$).
   - **Why Selected:** Enables simultaneous comparison of two categorical factors and their interaction while quantifying estimation uncertainty via confidence intervals (especially critical for sparse cells like `weathersit = 3` on non-working days where $n = 5$).
   - **Trend Identified:** Adverse weather depresses ridership across both working and non-working days; under clear weather (`weathersit = 1`), working days average $5,023.90$ vs. $4,587.27$ on non-working days, whereas under light rain/snow (`weathersit = 3`), both drop to $\approx 1,800$ bikes/day.

---

### 1.3 Subrequirement 1.3 — Outlier Detection

#### Specific Question / Requirement
- Present methods for identifying outliers.
- Propose appropriate methods for handling outliers.

#### Statistical Methodology Applied
- **Method 1 — Tukey's Interquartile Range (IQR) Rule (Non-parametric):** Flags observations below $\text{Lower Fence} = Q_1 - 1.5 \times \text{IQR}$ or above $\text{Upper Fence} = Q_3 + 1.5 \times \text{IQR}$ (plus extreme fences at $\pm 3.0 \times \text{IQR}$).
- **Method 2 — Standardized Z-Score Rule (Parametric):** Flags observations with $|z_i| = |(x_i - \bar{x}) / s| > 3.0$.
- **Method 3 — Physical Domain & Multivariate Residual Inspection:** Cross-checks univariate outliers against meteorological domain bounds (`hum == 0.0` during precipitation; `|temp - atemp|` consistency) and Cook's distance ($D_i > 4/n$) in regression.
- **Sensitivity Analysis:** Compares descriptive statistics and correlations across (a) the untouched dataset ($N = 731$), (b) dropping the `hum = 0.0` sensor error ($N = 730$), and (c) $1.5 \times \text{IQR}$ winsorization of weather variables ($N = 731$).

#### Confirmed Numerical Findings
- **Outlier Audit Across All 7 Continuous Variables (`01_exploratory_data_analysis/tables/eda_outlier_audit.csv`):**

| Variable | $Q_1$ | $Q_3$ | IQR | Lower Fence ($1.5\times\text{IQR}$) | Upper Fence ($1.5\times\text{IQR}$) | IQR Outliers (Below / Above / Total) | IQR Outlier % | $|z| > 3$ Count (%) | Max $|z|$ | Sample Flagged Dates & Diagnosis |
|---|---:|---:|---:|---:|---:|---|---:|---|---:|---|
| `cnt` | 3,152.0 | 5,956.0 | 2,804.0 | -1,054.0 | 10,162.0 | 0 / 0 / **0** | 0.00% | **0** (0.00%) | 2.3138 | None |
| `registered` | 2,497.0 | 4,776.5 | 2,279.5 | -922.25 | 8,195.75 | 0 / 0 / **0** | 0.00% | **0** (0.00%) | 2.3305 | None |
| `casual` | 315.5 | 1,096.0 | 780.5 | -855.25 | 2,266.75 | 0 / 44 / **44** | 6.02% | **8** (1.09%) | 3.7311 | `2011-07-04`, `2012-03-17`, `2012-05-19`: Genuine warm weekend/holiday leisure surges |
| `temp` | 0.3371 | 0.6554 | 0.3183 | -0.1404 | 1.1329 | 0 / 0 / **0** | 0.00% | **0** (0.00%) | 2.3832 | None |
| `atemp` | 0.3378 | 0.6086 | 0.2708 | -0.0683 | 1.0147 | 0 / 0 / **0** | 0.00% | **0** (0.00%) | 2.4256 | None (Univariate; bivariate anomaly with `temp` on `2012-08-17`) |
| `hum` | 0.5200 | 0.7302 | 0.2102 | 0.2047 | 1.0455 | 2 / 0 / **2** | 0.27% | **2** (0.27%) | 4.4085 | `2011-03-10` (`hum=0.0`, sensor error, $z=-4.41$); `2011-02-19` (`hum=0.1879`, dry windy day, $z=-3.09$) |
| `windspeed` | 0.1349 | 0.2332 | 0.0983 | -0.0124 | 0.3806 | 0 / 13 / **13** | 1.78% | **2** (0.27%) | 4.0901 | `2011-02-19` (`wind=0.5075`, $z=4.09$), `2012-03-08`: Genuine windy frontal systems |

- **Outlier Handling Protocol & Sensitivity Verification (`01_exploratory_data_analysis/tables/eda_outlier_handling_sensitivity.csv`):**
  1. **Retain Genuine Behavioral & Meteorological Extremes:** The $44$ upper-tail days in `casual` and $13$ high-wind days in `windspeed` represent authentic weekend tourism peaks and real storm fronts. Deleting them would censor true tail behavior.
  2. **Quarantine Target Components & Collinear Anomalies:** `casual` is excluded from regression predictors to prevent target leakage, and `atemp` (containing the `2012-08-17` anomaly) is excluded from primary OLS due to collinearity with `temp`.
  3. **Use Non-Parametric & Robust Estimators:** Pair parametric tests with rank-based tests (Spearman $\rho$, Mann-Whitney $U$, Kruskal-Wallis $H$) and White HC3 / Newey-West HAC robust standard errors in regression.
  4. **Explicit Sensitivity Check on Sensor Dropout (`hum = 0.0`):** Removing `2011-03-10` ($N = 730$) shifts mean `cnt` from $4,504.35$ to $4,509.67$ and shifts the `cnt`–`hum` Pearson correlation from $r = -0.1007$ ($p = 0.00645$) to $r = -0.1146$ ($p = 0.00192$), while `cnt`–`windspeed` shifts from $r = -0.2345$ to $r = -0.2328$. Thus, all substantive conclusions are invariant.

---

### 1.4 Subrequirement 1.4 — Overall Dataset Assessment

#### Specific Question / Requirement
- Identify and discuss the notable characteristics of the dataset based on the analyses above.

#### Synthesis of Notable Dataset Characteristics
1. **Structural Multi-Year Expansion:** Daily rental volume increased by **$+64.43\%$** between 2011 ($\bar{y}_{2011} = 3,405.76$) and 2012 ($\bar{y}_{2012} = 5,599.93$) as Capital Bikeshare expanded stations and membership. Ignoring `yr` confounds secular network growth with weather effects.
2. **Bifurcated User Composition (`registered` vs. `casual`):** Registered subscribers generate **$81.17\%$** of all rides ($\bar{y} = 3,656.17$, symmetric, $\text{skewness} = +0.0437$) and drive weekday commuting, whereas casual riders generate **$18.83\%$** ($\bar{y} = 848.18$, right-skewed, $\text{skewness} = +1.2665$) and surge on warm weekends and holidays.
3. **Compensating Weekday/Weekend Dynamics:** Aggregate daily ridership `cnt` shows almost no difference between working days ($4,584.82$) and non-working days ($4,330.17$) because the weekday surge in registered commuters ($+1,019.22$ bikes/day) is largely canceled out by the weekend surge in casual leisure riders ($+764.56$ bikes/day).
4. **Strong Thermal & Weather Regime Dependence:** Ridership is tightly coupled to ambient temperature ($r = +0.6275$) and season ($\eta^2 = 0.3470$), and drops by **$63.02\%$** on days with light rain or snow (`weathersit = 3`, $\bar{y} = 1,803.29$) relative to clear days (`weathersit = 1`, $\bar{y} = 4,876.79$).
5. **Important Codebook Note on `season` Labels:** In UCI's official `Readme.txt`, integer codes `1..4` are labeled `1: Spring`, `2: Summer`, `3: Fall`, `4: Winter`, but their calendar date boundaries follow astronomical solstice/equinox transitions shifted by one label:
   - `season = 1` ("Spring"): **Dec 21 – Mar 20** (coldest months, mean `temp` $= 0.2977 \approx 12.2^\circ\text{C}$, lowest ridership $= 2,604.13$).
   - `season = 2` ("Summer"): **Mar 21 – Jun 20** (mean `temp` $= 0.5444 \approx 22.3^\circ\text{C}$, mean `cnt` $= 4,992.33$).
   - `season = 3` ("Fall"): **Jun 21 – Sep 22** (warmest months, mean `temp` $= 0.7063 \approx 29.0^\circ\text{C}$, highest ridership $= 5,644.30$).
   - `season = 4` ("Winter"): **Sep 23 – Dec 20** (mean `temp` $= 0.4229 \approx 17.3^\circ\text{C}$, mean `cnt` $= 4,728.16$).
   The report should state this explicitly so readers understand why `Season 1 (Spring)` has the coldest temperatures and lowest ridership, and why `Season 3 (Fall)` has the warmest temperatures and highest ridership.

---

## 2. Requirement 2: Probability Distribution Analysis

### 2.1 Specific Question / Requirement
- Select **at least two important variables** and examine whether they follow any probability distribution (Normal, Poisson, Exponential, etc.).
- Use appropriate charts to illustrate the distributions.
- Provide observations about the characteristics of the data based on the distribution analysis.

### 2.2 Statistical Methodology Applied
- **Primary Variable 1 — `cnt` (Total Daily Bike Rentals, Discrete Count $\in \mathbb{Z}_{\ge 0}$):**
  - Tested against five theoretical families: **Poisson($\lambda$)**, **Negative Binomial($r, p$)**, **Normal($\mu, \sigma$)**, **Gamma($\alpha, \theta$)**, and **Exponential($\text{scale}$)**.
  - Evaluated Poisson equidispersion ($\text{Var}(Y) = \mathbb{E}[Y]$) via the **Index of Dispersion** $D = s^2 / \bar{y}$, the $\chi^2$ dispersion statistic $(n-1)s^2/\bar{y} \sim \chi^2_{730}$, and the **Cameron-Trivedi overdispersion test**.
  - Evaluated continuous Normal approximation via **Shapiro-Wilk $W$**, **D'Agostino-Pearson $K^2$**, **Jarque-Bera**, **Anderson-Darling**, and **Lilliefors parametric bootstrap KS test** ($2,000$ resamples).
- **Primary Variable 2 — `temp` (Normalized Ambient Temperature $\in [0, 1]$):**
  - Tested against **Normal($\mu, \sigma$)**, **Beta($\alpha, \beta$) on $(0, 1)$** (via both Method of Moments and MLE), and **Gamma($\alpha, \theta$)**.
  - Analyzed seasonal sub-regimes (`season 1..4`) to explain bimodal mixture flatness (negative excess kurtosis).
- **Supplemental Context Variables — `hum` and `windspeed`:**
  - Evaluated across **Normal**, **Beta$(0,1)$**, and **Gamma** distributions (`fig08`) to provide complete distributional context for all meteorological predictors.

### 2.3 Confirmed Numerical Findings

#### Variable 1: Total Daily Rentals (`cnt`)
- **Shape Summary (`02_probability_distributions/tables/probability_distribution_summary.csv`):**
  - $n = 731$, Mean $\hat{\mu} = 4,504.3488$, SD $\hat{\sigma} = 1,937.2115$, Variance $s^2 = 3,752,788.2083$, Skewness $= -0.0474$ (virtually symmetric), Excess Kurtosis $= -0.8119$ (platykurtic / flat-topped).
- **Candidate Distribution Comparison (`02_probability_distributions/tables/cnt_candidate_distributions_comparison.csv` & `cnt_overdispersion_and_fit.csv`):**

| Candidate Distribution | Domain | Fitted Parameters | Log-Likelihood | AIC | KS Distance | Goodness-of-Fit & Diagnostic Conclusion |
|---|---|---|---:|---:|---:|---|
| **Normal (Gaussian)** | $(-\infty, +\infty)$ | $\hat{\mu} = 4,504.35, \hat{\sigma} = 1,937.21$ | $-6,569.69$ | **$13,143.37$** | **$0.0471$** | **Lowest AIC & smallest KS distance** among single parametric curves, but formal normality is rejected (Shapiro-Wilk $W = 0.9801, p = 2.081 \times 10^{-8}$; D'Agostino $K^2 = 62.7077, p = 2.417 \times 10^{-14}$; Jarque-Bera $= 20.4822, p = 3.567 \times 10^{-5}$; Lilliefors bootstrap $p = 0.0010$). |
| **Gamma** | $(0, +\infty)$ | $\hat{\alpha} = 4.0216, \hat{\theta} = 1,120.04$ | $-6,613.89$ | $13,231.77$ | $0.0964$ | Second-best continuous fit, but imposes positive skewness incompatible with symmetric `cnt` ($\text{skew} = -0.0474$). |
| **Negative Binomial** | $\{0, 1, 2, \dots\}$ | $r = 5.4129, p = 0.001200$ | $-6,632.31$ | $13,268.61$ | $0.0734$ | **Best discrete count distribution** ($\Delta\text{AIC} = -662,932.83$ vs. Poisson); captures quadratic overdispersion $\text{Var}(Y) = \mu + \mu^2/r$, though right-skewed relative to the empirical middle plateau. |
| **Exponential** | $[0, +\infty)$ | $\text{scale} = 4,504.35$ | $-6,880.76$ | $13,763.51$ | $0.2559$ | Poor fit; assumes mode at $0$ and memoryless exponential decay. |
| **Poisson** | $\{0, 1, 2, \dots\}$ | $\hat{\lambda} = 4,504.35$ | $-338,099.72$ | $676,201.44$ | $0.4576$ | **Catastrophically rejected.** Index of Dispersion $D = s^2/\bar{y} = 833.1478$ ($\chi^2_{730} = 608,197.88, p = 0.0$; Cameron-Trivedi $t = 24.7853, p = 3.541 \times 10^{-99}$). |

#### Variable 2: Normalized Ambient Temperature (`temp`)
- **Shape Summary (`02_probability_distributions/tables/temp_distribution_diagnostics.csv`):**
  - $n = 731$, Mean $= 0.4954$ ($20.31^\circ\text{C}$), SD $= 0.1831$ ($7.51^\circ\text{C}$), Variance $= 0.0335$, Skewness $= -0.0545$, Excess Kurtosis $= -1.1189$ (strongly platykurtic / bimodal).
- **Candidate Distribution Comparison (`02_probability_distributions/tables/weather_variables_candidate_fits.csv`):**
  - **Beta$(0, 1)$ Fit (Best Fit):** $\hat{\alpha}_{\text{MLE}} = 3.3881, \hat{\beta}_{\text{MLE}} = 3.4640$ ($\hat{\alpha}_{\text{MoM}} = 3.2004, \hat{\beta}_{\text{MoM}} = 3.2600$), Log-Likelihood $= +234.35$, **$\text{AIC} = -464.70$**, KS distance $= 0.0614$.
  - **Normal Fit:** $\hat{\mu} = 0.4954, \hat{\sigma} = 0.1831$, Log-Likelihood $= +204.49$, $\text{AIC} = -404.97$, Lilliefors KS $= 0.0727$ ($p = 0.0005$), Shapiro-Wilk $W = 0.9659$ ($p = 5.146 \times 10^{-12}$), D'Agostino $K^2 = 294.2970$ ($p = 1.242 \times 10^{-64}$), Jarque-Bera $= 38.5282$ ($p = 4.302 \times 10^{-9}$), Anderson-Darling $A^2 = 8.0456$ ($p = 0.01$).
  - **Gamma Fit:** $\hat{\alpha} = 6.2673, \hat{\theta} = 0.0790$, Log-Likelihood $= +187.50$, $\text{AIC} = -371.00$, KS distance $= 0.0885$.
- **Seasonal Mixture Sub-Regimes Explaining Non-Normality of `temp`:**
  - `Season 1`: Mean $= 0.2977$, SD $= 0.1027$ ($\approx 12.2^\circ\text{C}$)
  - `Season 2`: Mean $= 0.5444$, SD $= 0.1226$ ($\approx 22.3^\circ\text{C}$)
  - `Season 3`: Mean $= 0.7063$, SD $= 0.0708$ ($\approx 29.0^\circ\text{C}$)
  - `Season 4`: Mean $= 0.4229$, SD $= 0.1078$ ($\approx 17.3^\circ\text{C}$)

#### Supplemental Context Variables (`hum` and `windspeed`)
- **Relative Humidity (`hum`):** Mean $= 0.6279$, SD $= 0.1424$, Skewness $= -0.0698$, Excess Kurtosis $= -0.0645$. Very close to Gaussian in bulk shape (D'Agostino $K^2 = 0.6835, p = 0.7105$; Jarque-Bera $= 0.7500, p = 0.6873$; Normal $\text{AIC} = -771.82$ beats Beta $\text{AIC} = -697.98$), with Shapiro-Wilk ($W = 0.9933, p = 0.00248$) sensitive to the single `hum = 0.0` sensor dropout on `2011-03-10`.
- **Wind Speed (`windspeed`):** Mean $= 0.1905$, SD $= 0.0775$, Skewness $= +0.6773$, Excess Kurtosis $= +0.4109$. Strictly positive and right-skewed; rejects Normal ($W = 0.9712, p = 8.426 \times 10^{-11}$, Normal $\text{AIC} = -1,661.58$), and is well described by **Beta$(\alpha = 4.7763, \beta = 20.2884)$** ($\text{AIC} = -1,725.60, \text{KS} = 0.0272$) or **Gamma$(\alpha = 5.8533, \theta = 0.0325)$** ($\text{AIC} = -1,724.33, \text{KS} = 0.0197$).

### 2.4 Supporting Package Files
- Tables:
  - `02_probability_distributions/tables/probability_distribution_summary.csv`
  - `02_probability_distributions/tables/cnt_overdispersion_and_fit.csv`
  - `02_probability_distributions/tables/cnt_candidate_distributions_comparison.csv`
  - `02_probability_distributions/tables/temp_distribution_diagnostics.csv`
  - `02_probability_distributions/tables/weather_variables_candidate_fits.csv`
- Figures:
  - **Figure 6:** `02_probability_distributions/figures/fig06_cnt_distribution_diagnostics.png` (2-panel: Histogram of `cnt` with Normal, Negative Binomial, and Poisson overlays + Normal Q-Q plot showing S-shaped light-tail curvature).
  - **Figure 7:** `02_probability_distributions/figures/fig07_temp_distribution_diagnostics.png` (2-panel: Histogram of `temp` with KDE, Normal, and Beta$(3.39, 3.46)$ overlays + Normal Q-Q plot showing bimodal seasonal inflection).
  - **Figure 8:** `02_probability_distributions/figures/fig08_hum_windspeed_distributions.png` (2x2 grid: Histogram/parametric fits and Q-Q plots for `hum` and `windspeed`).

### 2.5 Key Observations & Methodological Implications
1. **Why Unconditional `cnt` Is Overdispersed & Platykurtic:** Daily bike rentals do not arise from a homogeneous stationary Poisson process ($\lambda = \text{const}$). Instead, $\lambda_t$ varies systematically with year (`2011` vs. `2012`), season, and temperature. Mixing those regimes produces variance $833.15$ times larger than the mean and a flat-topped empirical distribution. Once we condition on `yr`, `temp`, `season`, and `weathersit` in Multiple Linear Regression (Requirement 5), the conditional variance drops by $83.87\%$.
2. **Why `temp` Follows a Bounded Bimodal Mixture Rather Than a Bell Curve:** Mid-latitude annual temperatures dwell near winter lows and summer highs with rapid spring/autumn transitions, yielding negative excess kurtosis ($-1.1189$) and bounded support $[0.0591, 0.8617]$ where a Beta distribution outperforms a Gaussian curve by $\Delta\text{AIC} = -59.73$.

---

## 3. Requirement 3: Hypothesis Testing

### 3.1 Subrequirement 3a — Statistical Test Theory

#### Specific Question / Requirement
- Study and explain the following statistical tests: **t-test**, **Chi-square test**, and **ANOVA**.

#### Concise Theoretical Reference for the Report

| Test Family | Purpose & Variable Types | Null ($H_0$) & Alternative ($H_1$) Hypotheses | Test Statistic & Degrees of Freedom | Required Assumptions & Robust Alternatives |
|---|---|---|---|---|
| **1. Independent Two-Sample t-Test** (Student's pooled & Welch's unpooled) | Compares population means of one continuous outcome $Y$ across two independent categorical groups ($k = 2$). | $H_0: \mu_1 = \mu_2$<br>$H_1: \mu_1 \neq \mu_2$ (two-sided) | **Student:** $t = \frac{\bar{Y}_1 - \bar{Y}_2}{s_p\sqrt{1/n_1 + 1/n_2}}$, $\text{df} = n_1 + n_2 - 2$.<br>**Welch:** $t = \frac{\bar{Y}_1 - \bar{Y}_2}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}$, Welch-Satterthwaite $\text{df}$. | 1. Independent observations.<br>2. Approximate normality within groups (or large $n_1, n_2 > 30$ via CLT).<br>3. Equal variances $\sigma_1^2 = \sigma_2^2$ for Student's $t$ (tested via Levene's test); **Welch's $t$-test** relaxes homoscedasticity; **Mann-Whitney $U$** is the non-parametric rank alternative. |
| **2. Chi-Square ($\chi^2$) Test of Independence** | Tests whether two categorical variables $A$ ($r$ levels) and $B$ ($c$ levels) are statistically independent in an $r \times c$ contingency table. | $H_0: P(A=i, B=j) = P(A=i)P(B=j)$ (independent)<br>$H_1:$ $A$ and $B$ are associated | $\chi^2 = \sum_{i=1}^r \sum_{j=1}^c \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$,<br>where $E_{ij} = \frac{R_i C_j}{N}$,<br>$\text{df} = (r-1)(c-1)$. | 1. Independent observations allocated to mutually exclusive cells.<br>2. **Cochran's Rule:** At least $80\%$ of cells have expected frequency $E_{ij} \ge 5$ and all $E_{ij} \ge 1$.<br>3. If sparse cells occur, use **Likelihood Ratio $G^2$** or **Fisher's Exact Test**; quantify effect size via **Cramér's $V = \sqrt{\chi^2 / (N \cdot \min(r-1, c-1))}$**. |
| **3. One-Way Analysis of Variance (ANOVA)** | Compares population means of one continuous outcome $Y$ across $k \ge 3$ independent categorical groups. | $H_0: \mu_1 = \mu_2 = \dots = \mu_k$<br>$H_1:$ At least one $\mu_i \neq \mu_j$ | $F = \frac{\text{MSB}}{\text{MSW}} = \frac{\text{SSB}/(k-1)}{\text{SSW}/(N-k)}$,<br>$\text{df}_1 = k-1, \text{df}_2 = N-k$. | 1. Independent observations.<br>2. Normal residuals within groups (or large $n_j$ via CLT).<br>3. Homogeneity of variance $\sigma_1^2 = \dots = \sigma_k^2$ (tested via Levene / Brown-Forsythe). If violated, use **Welch's heteroscedastic ANOVA** and **Kruskal-Wallis $H$**; follow significant omnibus $F$ with **Tukey HSD** or **Holm-adjusted Welch** post-hoc tests; measure effect size via $\eta^2 = \text{SSB}/\text{SST}$ and $\omega^2$. |

---

### 3.2 Subrequirements 3b & 3c — Research Questions, Statistical Testing, and Interpretation

#### Specific Question / Requirement
- Propose **two research questions** (three complete research questions covering all three tests — `t-test`, `ANOVA`, and `Chi-square` — are provided below so the report can present either all three or any required pair) that can be statistically tested using the selected dataset.
- Apply statistical hypothesis testing to answer the proposed research questions.
- Explain the results of the statistical hypothesis tests.

#### Omnibus Summary Table Across All Three Hypothesis Tests (`03_hypothesis_testing/tables/hypothesis_tests_summary.csv`)

| ID | Test Family | Variables Tested | Primary Test Statistic | Unadjusted $p$-Value | Holm-Adjusted $p$-Value | Effect Size | Decision ($\alpha = 0.05$) |
|---|---|---|---|---:|---:|---|---|
| **H1** | Welch Two-Sample $t$-Test | `workingday` ($0$ vs. $1$) $\rightarrow$ `cnt` | $t_{\text{Welch}} = 1.6014$ ($\text{df} = 413.94$) | $0.1101$ ($0.110057$) | $0.1101$ | Hedges' $g = +0.1315$ | **Fail to Reject $H_0$** |
| **H2** | One-Way & Welch ANOVA | `season` ($1..4$) $\rightarrow$ `cnt` | $F(3, 727) = 128.7696$<br>$F_{\text{Welch}}(3, 401.83) = 153.9939$ | $6.720 \times 10^{-67}$<br>$1.952 \times 10^{-66}$ | $2.016 \times 10^{-66}$ | $\eta^2 = 0.3470$,<br>$\omega^2 = 0.3440$ | **Reject $H_0$** |
| **H3** | Pearson Chi-Square ($\chi^2$) | `weathersit` ($1..3$) $\times$ `high_demand` ($\text{cnt} > 4,548$) | $\chi^2(2) = 44.0879$ | $2.669 \times 10^{-10}$ | $5.339 \times 10^{-10}$ | Cramér's $V = 0.2456$ | **Reject $H_0$** |

---

#### Detailed Evidence for Research Question 1 (H1 — Independent Two-Sample $t$-Test)
- **Research Question:** *Does mean daily total bike ridership (`cnt`) differ significantly between working days (`workingday = 1`) and non-working days (`workingday = 0`, weekends and public holidays)?*
- **Hypotheses ($\alpha = 0.05$, two-sided):**
  - $H_0: \mu_{\text{workday}} - \mu_{\text{non-workday}} = 0$
  - $H_1: \mu_{\text{workday}} - \mu_{\text{non-workday}} \neq 0$
- **Group Descriptive Statistics (`03_hypothesis_testing/tables/h1_ttest_workingday.csv`):**
  - **Working Days (`workingday = 1`, $n_1 = 500$):** Mean $= 4,584.8200$, SD $= 1,878.4156$, Median $= 4,582.00$, IQR $= 2,643.25$.
  - **Non-Working Days (`workingday = 0`, $n_0 = 231$):** Mean $= 4,330.1688$, SD $= 2,052.1412$, Median $= 4,459.00$, IQR $= 3,197.00$.
  - **Observed Difference ($\bar{Y}_1 - \bar{Y}_0$):** $+254.6512$ bikes/day ($\text{SE}_{\text{Welch}} = 159.0206$).
- **Assumption Checks:**
  - **Homogeneity of Variance:** Levene's mean-centered test $F = 4.4181, p = 0.0359$; Brown-Forsythe median-centered test $F = 4.3454, p = 0.0375$. Because group variances differ modestly ($p < 0.05$, with wider dispersion on weekends/holidays), **Welch's unpooled $t$-test** is used as the primary test.
  - **Normality:** Shapiro-Wilk $W_1 = 0.9766$ ($p = 3.489 \times 10^{-7}$), $W_0 = 0.9761$ ($p = 6.035 \times 10^{-4}$). With large sample sizes ($n_1 = 500, n_0 = 231$), the Central Limit Theorem guarantees asymptotic normality of sample means; non-parametric Mann-Whitney $U$ and permutation tests are also reported to verify robustness.
- **Calculated Test Results:**
  - **Welch's $t$-Test (Primary):** $t = 1.6014$, $\text{df} = 413.9358$, **$p = 0.1101$** ($0.110057$), 95% CI for mean difference $= [-57.9375, +567.2398]$ bikes/day.
  - **Student's Pooled $t$-Test:** $t = 1.6543$, $\text{df} = 729$, $p = 0.0985$.
  - **Mann-Whitney $U$ Test:** $U = 61,893.0$, $p = 0.1186$, rank-biserial $r_{rb} = +0.0717$.
  - **Exact Two-Sided Permutation Test ($10,000$ resamples):** $p = 0.0987$.
  - **Standardized Effect Size:** Cohen's $d = +0.1316$, **Hedges' $g = +0.1315$** (negligible/very small effect).
- **Substantive Interpretation & Component Decomposition (Why $H_0$ Is Not Rejected):**
  - At $\alpha = 0.05$, we **fail to reject $H_0$** ($p = 0.1101 > 0.05$; the 95% CI $[-57.94, +567.24]$ spans zero).
  - Crucially, decomposing `cnt = registered + casual` reveals two massive, opposite behavioral shifts that cancel each other out in aggregate `cnt` (`03_hypothesis_testing/tables/h1_ttest_workingday.csv`):
    - **Registered Subscribers (`registered`):** Mean is **$3,978.25$** on working days vs. **$2,959.03$** on non-working days $\rightarrow$ difference $= \mathbf{+1,019.22}$ bikes/day ($t_{\text{Welch}} = +9.2394, \text{df} = 534.78, p = 5.822 \times 10^{-19}$, Hedges' $g = +0.6845$).
    - **Casual Users (`casual`):** Mean is **$606.57$** on working days vs. **$1,371.13$** on non-working days $\rightarrow$ difference $= \mathbf{-764.56}$ bikes/day ($t_{\text{Welch}} = -12.7316, \text{df} = 273.63, p = 1.786 \times 10^{-29}$, Hedges' $g = -1.2996$).
    - **Net Aggregate Offset:** $+1,019.2154 - 764.5642 = +254.6512$ bikes/day ($p = 0.1101$). Thus, total fleet utilization remains high all week because weekday commuter demand is replaced by weekend recreational demand.
- **Supporting Figure:** `03_hypothesis_testing/figures/fig09_h1_workingday_ttest.png`

---

#### Detailed Evidence for Research Question 2 (H2 — One-Way ANOVA Across Seasons)
- **Research Question:** *Does mean daily total bike ridership (`cnt`) differ significantly across the four UCI seasonal regimes (`season` $\in \{1, 2, 3, 4\}$), and which specific pairs of seasons drive these differences?*
- **Hypotheses ($\alpha = 0.05$):**
  - $H_0: \mu_1 = \mu_2 = \mu_3 = \mu_4$
  - $H_1:$ At least one seasonal population mean $\mu_k$ differs from the others.
- **Seasonal Group Summaries (`03_hypothesis_testing/tables/h2_anova_omnibus_and_groups.csv`):**
  - `Season 1: Spring (Dec 21–Mar 20)` ($n = 181$): Mean $= 2,604.1326$, SD $= 1,399.9421$, SE $= 104.0569$, 95% CI $= [2,398.80, 2,809.46]$, Median $= 2,209.00$, IQR $= 1,918.00$.
  - `Season 2: Summer (Mar 21–Jun 20)` ($n = 184$): Mean $= 4,992.3315$, SD $= 1,695.9772$, SE $= 125.0291$, 95% CI $= [4,745.65, 5,239.02]$, Median $= 4,941.50$, IQR $= 2,374.00$.
  - `Season 3: Fall (Jun 21–Sep 22)` ($n = 188$): Mean $= 5,644.3032$, SD $= 1,459.8004$, SE $= 106.4669$, 95% CI $= [5,434.27, 5,854.33]$, Median $= 5,353.50$, IQR $= 2,342.75$.
  - `Season 4: Winter (Sep 23–Dec 20)` ($n = 178$): Mean $= 4,728.1629$, SD $= 1,699.6153$, SE $= 127.3915$, 95% CI $= [4,476.76, 4,979.56]$, Median $= 4,634.50$, IQR $= 2,009.00$.
- **Assumption Checks:**
  - Levene's test $F = 2.7393, p = 0.0425$; Brown-Forsythe median-centered test $F = 3.2497, p = 0.0214$. Because group standard deviations range from $1,399.94$ to $1,699.62$, we report **Ordinary One-Way ANOVA**, **Welch's heteroscedastic ANOVA**, and **Kruskal-Wallis non-parametric ANOVA**, plus both **Tukey HSD** and **Holm-adjusted Welch pairwise $t$-tests**.
- **Calculated Omnibus Results:**
  - **Ordinary One-Way ANOVA:** $F(3, 727) = 128.7696$, **$p = 6.720 \times 10^{-67}$** (Holm-adjusted $p = 2.016 \times 10^{-66}$).
  - **Welch's Heteroscedastic ANOVA:** $F_{\text{Welch}}(3, 401.83) = 153.9939$, **$p = 1.952 \times 10^{-66}$**.
  - **Kruskal-Wallis Test:** $H(3) = 250.9335$, **$p = 4.111 \times 10^{-54}$** ($\epsilon^2_{\text{KW}} = 0.3437$).
  - **Omnibus Effect Size:** **$\eta^2 = 0.3470$** and **$\omega^2 = 0.3440$** (a very large effect: **$34.70\%$** of the total variance in daily bike rentals is explained by season alone).
- **Post-Hoc Pairwise Comparisons (`03_hypothesis_testing/tables/h2_anova_season_posthoc.csv`):**

| Pairwise Comparison ($\text{Group 2} - \text{Group 1}$) | Mean Diff ($\bar{Y}_2 - \bar{Y}_1$) | Tukey 95% CI | Tukey $p_{\text{adj}}$ | Welch $t$ ($\text{df}$) | Welch $p_{\text{Holm}}$ | Hedges' $g$ | Significant at $\alpha = 0.05$? |
|---|---:|---|---:|---|---:|---:|---|
| `Season 2 (Summer)` $-$ `Season 1 (Spring)` | $+2,388.20$ | $[+1,965.33, +2,811.07]$ | $< 0.0001$ | $+14.6816$ ($352.41$) | $1.031 \times 10^{-37}$ | $+1.5314$ | **Yes (Reject $H_0$)** |
| `Season 3 (Fall)` $-$ `Season 1 (Spring)` | $+3,040.17$ | $[+2,619.54, +3,460.80]$ | $< 0.0001$ | $+20.4213$ ($366.99$) | $1.097 \times 10^{-61}$ | $+2.1205$ | **Yes (Reject $H_0$)** |
| `Season 4 (Winter)` $-$ `Season 1 (Spring)` | $+2,124.03$ | $[+1,697.64, +2,550.42]$ | $< 0.0001$ | $+12.9129$ ($342.19$) | $9.560 \times 10^{-31}$ | $+1.3624$ | **Yes (Reject $H_0$)** |
| `Season 3 (Fall)` $-$ `Season 2 (Summer)` | $+651.97$ | $[+233.09, +1,070.85]$ | $0.0004$ | $+3.9702$ ($359.59$) | $1.735 \times 10^{-4}$ | $+0.4115$ | **Yes (Reject $H_0$)** |
| `Season 4 (Winter)` $-$ `Season 2 (Summer)` | $-264.17$ | $[-688.83, +160.49]$ | **$0.3782$** | $-1.4800$ ($359.55$) | **$0.1398$** | $-0.1553$ | **No (Fail to Reject)** |
| `Season 4 (Winter)` $-$ `Season 3 (Fall)` | $-916.14$ | $[-1,338.57, -493.71]$ | $< 0.0001$ | $-5.5181$ ($349.31$) | $2.006 \times 10^{-7}$ | $-0.5783$ | **Yes (Reject $H_0$)** |

- **Substantive Interpretation:**
  - We **strongly reject $H_0$** ($p = 6.72 \times 10^{-67}$). Five of the six seasonal pairs differ significantly under both Tukey HSD and Holm-adjusted Welch tests.
  - Peak demand occurs in `Season 3 (Jun 21–Sep 22)` ($5,644.30$ bikes/day), which exceeds `Season 1 (Dec 21–Mar 20)` ($2,604.13$ bikes/day) by $+3,040.17$ bikes/day ($+116.7\%$, Hedges' $g = +2.12$).
  - Only `Season 2 (Mar 21–Jun 20)` ($4,992.33$) vs. `Season 4 (Sep 23–Dec 20)` ($4,728.16$) is statistically indistinguishable ($p_{\text{Tukey}} = 0.3782, p_{\text{Welch-Holm}} = 0.1398$), reflecting similar moderate shoulder-season temperatures coupled with higher 2012 baseline membership in late autumn.
- **Supporting Figure:** `03_hypothesis_testing/figures/fig10_h2_season_anova.png`

---

#### Detailed Evidence for Research Question 3 (H3 — Chi-Square Test of Independence)
- **Research Question:** *Is the daily weather situation (`weathersit` $\in \{1, 2, 3\}$) statistically independent of whether a day achieves an above-median high-demand rental regime (`high_demand`: $\text{cnt} > 4,548.0$)?*
- **Hypotheses ($\alpha = 0.05$):**
  - $H_0:$ `weathersit` and `high_demand` are statistically independent.
  - $H_1:$ `weathersit` and `high_demand` are statistically associated.
- **Contingency Table ($3 \times 2$, $N = 731$, Median Threshold $= 4,548.0$ bikes/day; `03_hypothesis_testing/tables/h3_chisq_contingency_table.csv`):**

| Weather Situation (`weathersit`) | Observed Low Demand ($\le 4,548$) | Observed High Demand ($> 4,548$) | Row Total | Expected Low Demand | Expected High Demand | Low Demand % | High Demand % | Std. Adjusted Residual (High Demand) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `1: Clear / Partly Cloudy` | 193 | **270** | 463 | 231.82 | 231.18 | 41.68% | **58.32%** | $+5.9587$ |
| `2: Mist / Cloudy` | 153 | **94** | 247 | 123.67 | 123.33 | 61.94% | **38.06%** | $-4.5872$ |
| `3: Light Snow / Light Rain` | 20 | **1** | 21 | 10.51 | 10.49 | 95.24% | **4.76%** | $-4.2007$ |
| **Column Total** | **366** | **365** | **731** | **366.00** | **365.00** | **50.07%** | **49.93%** | — |

- **Assumption Check (Cochran's Rule):**
  - Minimum expected cell count is **$E_{\min} = 10.4856 \ge 5.0$** ($0$ cells have expected frequency $< 5$). Cochran's rule is 100% satisfied (`weathersit = 4` has $0$ days in `day.csv` and is therefore not an active structural row).
- **Calculated Test Results (`03_hypothesis_testing/tables/h3_chisq_omnibus_and_robustness.csv`):**
  - **Pearson Chi-Square ($\chi^2$):** $\chi^2(2) = 44.0879$, **$p = 2.669 \times 10^{-10}$** (Holm-adjusted $p = 5.339 \times 10^{-10}$).
  - **Likelihood Ratio ($G^2$):** $G^2(2) = 48.1658$, $p = 3.475 \times 10^{-11}$.
  - **Effect Size:** **Cramér's $V = 0.2456$** (Cohen's $w = 0.2456$, moderate association).
  - **Collapsed $2 \times 2$ Robustness Check (`Clear [1]` vs. `Adverse [2 & 3]`):** Fisher's Exact Odds Ratio $= 2.5476$, two-sided $p = 2.878 \times 10^{-9}$ (clear days have $2.55\times$ the odds of achieving above-median ridership compared to misty or rainy/snowy days).
- **Substantive Interpretation:**
  - We **reject $H_0$** ($p = 2.669 \times 10^{-10}$). Weather condition strongly governs the probability of achieving a high-demand day: **$58.32\%$** of Clear days ($270/463$) exceed the median, dropping to **$38.06\%$** under Mist/Cloudy skies ($94/247$, adjusted residual $-4.59$) and collapsing to **$4.76\%$** ($1/21$ days, adjusted residual $-4.20$) during Light Snow/Rain.
- **Supporting Figure:** `03_hypothesis_testing/figures/fig11_h3_weathersit_highdemand_chisq.png`

---

## 4. Requirement 4: Correlation Analysis Between Variables

### 4.1 Subrequirement 4a — Theoretical Background

#### Specific Question / Requirement
- Study and explain the following correlation coefficients: **Pearson correlation coefficient** and **Spearman correlation coefficient**.

#### Concise Theoretical Comparison for the Report

| Dimension | Pearson Product-Moment Correlation ($r$) | Spearman Rank-Order Correlation ($\rho$ or $r_s$) |
|---|---|---|
| **Mathematical Definition** | $r = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^n (x_i - \bar{x})^2}\sqrt{\sum_{i=1}^n (y_i - \bar{y})^2}}$ | Pearson correlation computed on the rank-transformed variables $R(x_i), R(y_i)$ (without ties: $\rho = 1 - \frac{6\sum d_i^2}{n(n^2-1)}$). |
| **Type of Relationship Measured** | **Linear** association (how closely points cluster around a straight line $Y = a + bX$). | **Monotonic** association (whether $Y$ consistently increases or decreases as $X$ increases, regardless of curvature). |
| **Scale & Distributional Assumptions** | Parametric; requires interval/ratio continuous variables; exact $t$-test ($t = r\sqrt{(n-2)/(1-r^2)}$) assumes bivariate normality or large $n$. | Non-parametric; valid for continuous or ordinal variables; invariant to any strictly monotonic non-linear transformation. |
| **Range & Outlier Sensitivity** | $[-1, +1]$. Highly sensitive to extreme leverage points and outliers. | $[-1, +1]$. Robust to extreme outliers and skewed tails because extreme values are bounded by their rank order $1..n$. |

---

### 4.2 Subrequirements 4b, 4c & 4d — Correlation Calculation, Visualization, and Practical Interpretation

#### Specific Question / Requirement
- Calculate Pearson and Spearman correlation coefficients between variables in the selected dataset.
- Use appropriate charts to visualize relationships between variables.
- Discuss the practical significance of the observed correlations.

#### Statistical Methodology Applied
- Computed the exact $5 \times 5$ **Pearson ($r$)** and **Spearman ($\rho$)** correlation matrices across the $5$ core continuous study variables (`cnt`, `temp`, `atemp`, `hum`, `windspeed`) to avoid scale-type fallacies on nominal codes (`04_correlation_analysis/tables/pearson_correlation_matrix.csv` and `spearman_correlation_matrix.csv`).
- For all $\binom{5}{2} = 10$ unique variable pairs, computed Fisher-$z$ 95% confidence intervals, exact two-sided $p$-values, Holm-Bonferroni adjusted $p$-values, and $\Delta = \rho - r$ linearity comparisons (`04_correlation_analysis/tables/correlation_pairwise_tests.csv`).
- Also computed an extended reference table of correlations between `cnt` and all remaining variables (`registered`, `casual`, `yr`, `workingday`, `holiday`, `season`, `weathersit`, `mnth`, `weekday`) with explicit methodological role annotations (`04_correlation_analysis/tables/extended_correlations_with_cnt.csv`).

#### Confirmed Numerical Findings

1. **Primary $5 \times 5$ Continuous Correlation Matrices ($N = 731$):**
   - **Pearson Linear Correlation Matrix ($r$, `04_correlation_analysis/tables/pearson_correlation_matrix.csv`)** and **Spearman Rank Correlation Matrix ($\rho$, `04_correlation_analysis/tables/spearman_correlation_matrix.csv`):**

| Variable | `cnt` ($r$ / $\rho$) | `temp` ($r$ / $\rho$) | `atemp` ($r$ / $\rho$) | `hum` ($r$ / $\rho$) | `windspeed` ($r$ / $\rho$) |
|---|---|---|---|---|---|
| **`cnt`** | $1.0000$ / $1.0000$ | **$+0.6275$** / **$+0.6220$** | **$+0.6311$** / **$+0.6228$** | **$-0.1007$** / **$-0.0981$** | **$-0.2345$** / **$-0.2172$** |
| **`temp`** | $+0.6275$ / $+0.6220$ | $1.0000$ / $1.0000$ | **$+0.9917$** / **$+0.9926$** | $+0.1270$ / $+0.1299$ | $-0.1579$ / $-0.1472$ |
| **`atemp`** | $+0.6311$ / $+0.6228$ | **$+0.9917$** / **$+0.9926$** | $1.0000$ / $1.0000$ | $+0.1400$ / $+0.1396$ | $-0.1836$ / $-0.1690$ |
| **`hum`** | $-0.1007$ / $-0.0981$ | $+0.1270$ / $+0.1299$ | $+0.1400$ / $+0.1396$ | $1.0000$ / $1.0000$ | **$-0.2485$** / **$-0.2390$** |
| **`windspeed`** | $-0.2345$ / $-0.2172$ | $-0.1579$ / $-0.1472$ | $-0.1836$ / $-0.1690$ | $-0.2485$ / $-0.2390$ | $1.0000$ / $1.0000$ |

2. **All 10 Pairwise Correlation Tests (`04_correlation_analysis/tables/correlation_pairwise_tests.csv`):**

| Variable Pair | Pearson $r$ | $r^2$ | Pearson 95% CI | Pearson $p$ (Unadj.) | Spearman $\rho$ | Spearman 95% CI | Spearman $p$ (Unadj.) | $\rho - r$ | Magnitude |
|---|---:|---:|---|---:|---:|---|---:|---:|---|
| `cnt` vs. `temp` | **$+0.6275$** | $0.3937$ | $[+0.5814, +0.6695]$ | $2.811 \times 10^{-81}$ | **$+0.6220$** | $[+0.5755, +0.6646]$ | $1.675 \times 10^{-79}$ | $-0.0055$ | Strong positive |
| `cnt` vs. `atemp` | **$+0.6311$** | $0.3982$ | $[+0.5853, +0.6728]$ | $1.855 \times 10^{-82}$ | **$+0.6228$** | $[+0.5763, +0.6653]$ | $9.615 \times 10^{-80}$ | $-0.0083$ | Strong positive |
| `cnt` vs. `windspeed` | **$-0.2345$** | $0.0550$ | $[-0.3019, -0.1648]$ | $1.360 \times 10^{-10}$ | **$-0.2172$** | $[-0.2852, -0.1470]$ | $2.969 \times 10^{-9}$ | $+0.0173$ | Weak negative |
| `cnt` vs. `hum` | **$-0.1007$** | $0.0101$ | $[-0.1719, -0.0284]$ | $0.00645$ | **$-0.0981$** | $[-0.1694, -0.0258]$ | $0.00793$ | $+0.0025$ | Weak negative |
| `temp` vs. `atemp` | **$+0.9917$** | $0.9835$ | $[+0.9904, +0.9928]$ | $< 10^{-300}$ ($0.0$) | **$+0.9926$** | $[+0.9914, +0.9936]$ | $< 10^{-300}$ ($0.0$) | $+0.0009$ | Near-perfect collinear |
| `temp` vs. `hum` | $+0.1270$ | $0.0161$ | $[+0.0550, +0.1977]$ | $0.000580$ | $+0.1299$ | $[+0.0579, +0.2005]$ | $0.000430$ | $+0.0029$ | Weak positive |
| `temp` vs. `windspeed` | $-0.1579$ | $0.0249$ | $[-0.2278, -0.0864]$ | $1.787 \times 10^{-5}$ | $-0.1472$ | $[-0.2173, -0.0754]$ | $6.510 \times 10^{-5}$ | $+0.0108$ | Weak negative |
| `atemp` vs. `hum` | $+0.1400$ | $0.0196$ | $[+0.0682, +0.2104]$ | $0.000146$ | $+0.1396$ | $[+0.0678, +0.2100]$ | $0.000152$ | $-0.0003$ | Weak positive |
| `atemp` vs. `windspeed` | $-0.1836$ | $0.0337$ | $[-0.2528, -0.1126]$ | $5.756 \times 10^{-7}$ | $-0.1690$ | $[-0.2386, -0.0977]$ | $4.345 \times 10^{-6}$ | $+0.0147$ | Weak negative |
| `hum` vs. `windspeed` | $-0.2485$ | $0.0617$ | $[-0.3153, -0.1792]$ | $9.488 \times 10^{-12}$ | $-0.2390$ | $[-0.3062, -0.1694]$ | $5.907 \times 10^{-11}$ | $+0.0095$ | Weak negative |

3. **Extended Correlations with `cnt` (`04_correlation_analysis/tables/extended_correlations_with_cnt.csv`):**
   - Part-whole components (excluded from regression to prevent target leakage): `registered` ($r = +0.9455, \rho = +0.9403, p < 10^{-300}$) and `casual` ($r = +0.6728, p = 1.717 \times 10^{-97}; \rho = +0.7535, p = 6.508 \times 10^{-135}$).
   - Binary/categorical indicators: `yr` ($r = +0.5667, \rho = +0.5720, p < 10^{-62}$), `season` ($r = +0.4061, \rho = +0.3984$), `weathersit` ($r = -0.2974, \rho = -0.2721$), `mnth` ($r = +0.2800, \rho = +0.2720$), `workingday` ($r = +0.0612, p = 0.0985\text{ [NS]}; \rho = +0.0578, p = 0.1186\text{ [NS]}$), `holiday` ($r = -0.0683, p = 0.0648\text{ [NS]}$), `weekday` ($r = +0.0674, p = 0.0684\text{ [NS]}$).

#### Exported Visualizations (`04_correlation_analysis/figures/`)
- **Figure 12 (`04_correlation_analysis/figures/fig12_pearson_correlation_heatmap.png`):** Annotated $5 \times 5$ heatmap of Pearson linear correlation coefficients ($r$) and exact significance stars/$p$-values.
- **Figure 13 (`04_correlation_analysis/figures/fig13_spearman_correlation_heatmap.png`):** Annotated $5 \times 5$ heatmap of Spearman rank-order correlation coefficients ($\rho$) and exact $p$-values.
- **Figure 14 (`04_correlation_analysis/figures/fig14_continuous_predictors_scatter_grid.png`):** $2 \times 2$ bivariate scatter matrix with OLS linear lines and LOWESS smooth curves (`temp` vs. `cnt`, `atemp` vs. `cnt`, `hum` vs. `cnt`, `windspeed` vs. `cnt`, plus collinearity inset).

#### Practical Significance & Interpretation
1. **Temperature Is the Dominant Meteorological Driver:** Ambient temperature (`temp`, $r = +0.6275, r^2 = 39.37\%$) and feeling temperature (`atemp`, $r = +0.6311, r^2 = 39.82\%$) account for nearly $40\%$ of daily ridership variance on their own. The close agreement between Pearson $r$ ($+0.6275$) and Spearman $\rho$ ($+0.6220$) shows that the relationship is predominantly linear across most of the temperature range, with mild curvature only at extreme summer heat ($> 31^\circ\text{C}$).
2. **Severe Collinearity Between `temp` and `atemp` ($r = +0.9917, \rho = +0.9926$):** Because `atemp` is a deterministic thermal-comfort function of `temp`, they share $r^2 = 98.35\%$ of their variance. Entering both into Multiple Linear Regression inflates VIF to $184.86$ (`temp`) and $179.30$ (`atemp`). Therefore, `atemp` **must be dropped** in Requirement 5.
3. **Confounding Between Temperature and Humidity:** Marginally, `hum` has only a weak negative correlation with `cnt` ($r = -0.1007, p = 0.00645$) because warm summer days in Washington, D.C. are also more humid ($r(\text{temp}, \text{hum}) = +0.1270, p = 0.00058$). Once temperature and weather situation are held constant in multiple regression, the partial negative effect of humidity becomes much stronger ($\hat{\beta}_{\text{hum}} = -1,218.46, p = 2.56 \times 10^{-5}$).
4. **Wind Deterrence:** Higher wind speeds consistently deter cyclists ($r = -0.2345, \rho = -0.2172, p = 1.36 \times 10^{-10}$) due to aerodynamic drag and wind chill.

---

## 5. Requirement 5: Multiple Linear Regression

### 5.1 Subrequirement 5a — Theoretical Background

#### Specific Question / Requirement
- Study and explain the theory of Multiple Linear Regression.

#### Concise Theoretical Summary for the Report
- **Structural Model Equation:**
  $$Y_i = \beta_0 + \beta_1 X_{i1} + \beta_2 X_{i2} + \dots + \beta_p X_{ip} + \varepsilon_i, \quad i = 1, \dots, n$$
  where $Y_i$ is the dependent variable (`cnt`), $X_{i1}, \dots, X_{ip}$ are $p$ explanatory variables, $\beta_0$ is the intercept, $\beta_j$ is the partial regression slope (expected change in $Y$ per 1-unit increase in $X_j$, holding all other predictors constant), and $\varepsilon_i$ is the random disturbance term.
- **Ordinary Least Squares (OLS) Estimation:** Minimizes the Residual Sum of Squares $\text{RSS} = \sum_{i=1}^n (y_i - \hat{y}_i)^2$, yielding the closed-form estimator $\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top \mathbf{y}$.
- **Classical Gauss-Markov & Inference Assumptions:**
  1. **Linearity in Parameters & Zero Conditional Mean:** $\mathbb{E}[\boldsymbol{\varepsilon} \mid \mathbf{X}] = \mathbf{0}$ (checked via Residuals vs. Fitted plot + LOWESS curve).
  2. **No Perfect or Severe Multicollinearity:** $\text{rank}(\mathbf{X}) = p + 1$; diagnosed via **Variance Inflation Factor** $\text{VIF}_j = \frac{1}{1 - R_j^2}$ (threshold $\text{VIF}_j < 5.0$).
  3. **Homoscedasticity (Constant Error Variance):** $\text{Var}(\varepsilon_i \mid \mathbf{X}) = \sigma^2$ (tested via **Breusch-Pagan LM and $F$ tests**).
  4. **No Serial Correlation (Independent Errors):** $\text{Cov}(\varepsilon_i, \varepsilon_j \mid \mathbf{X}) = 0$ for $i \neq j$ (tested via **Durbin-Watson $d$** and **Ljung-Box $Q$** statistics).
  5. **Normality of Errors:** $\varepsilon_i \sim \mathcal{N}(0, \sigma^2)$ for exact finite-sample $t$ and $F$ inference (tested via **Shapiro-Wilk $W$**, **Jarque-Bera**, and **Normal Q-Q plot**). When heteroscedasticity or autocorrelation is present in time-series data, OLS point estimates $\hat{\boldsymbol{\beta}}$ remain unbiased and consistent, and valid inference is restored using **White's HC3 heteroscedasticity-robust** and **Newey-West HAC (lag = 7)** standard errors.
- **Evaluation Metrics:**
  - **Coefficient of Determination ($R^2$):** $R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$
  - **Adjusted $R^2$:** $R^2_{\text{adj}} = 1 - (1 - R^2)\frac{n - 1}{n - p - 1}$
  - **Mean Absolute Error (MAE):** $\text{MAE} = \frac{1}{n}\sum_{i=1}^n |y_i - \hat{y}_i|$
  - **Root Mean Squared Error (RMSE):** $\text{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2}$

---

### 5.2 Subrequirement 5b — Model Development and Evaluation

#### Specific Question / Requirement
- Build and evaluate a **Multiple Linear Regression model** to predict a dependent variable (target variable) based on multiple independent variables from the selected dataset.

#### Statistical Methodology & Anti-Leakage Design
1. **Target Variable ($Y$):** `cnt` (total daily bike rentals).
2. **Strict Anti-Leakage Feature Quarantine:**
   - `casual` and `registered` are **strictly excluded** because `cnt = casual + registered` (including them would cause $100\%$ target leakage).
   - `high_demand` (derived from `cnt` in H3), `instant` (row index), and `dteday` (raw date string) are **strictly excluded**.
   - `atemp` is **excluded from the primary model** because of severe collinearity with `temp` ($r = 0.9917$, $\text{VIF} = 184.86$ when included), and `mnth`/`weekday` are excluded to avoid structural collinearity with `season` and `workingday`.
3. **Final 11 Encoded Predictors ($p = 11$):**
   - **Continuous (3):** `temp`, `hum`, `windspeed`
   - **Binary Indicators (3):** `yr` ($1 = 2012, 0 = 2011$), `holiday` ($1 = \text{Yes}$), `workingday` ($1 = \text{Workday}$)
   - **One-Hot Encoded Categoricals (`drop='first'`, 5):** `season_2` (Summer), `season_3` (Fall), `season_4` (Winter) [Reference: `season = 1` Spring]; `weathersit_2` (Mist/Cloudy), `weathersit_3` (Light Snow/Rain) [Reference: `weathersit = 1` Clear].
4. **Chronological 80/20 Train/Test Split (Zero Temporal Leakage):**
   - Sorted strictly by `dteday` ascending:
     - **Training Set (first 80%):** $n_{\text{train}} = 584$ days (`2011-01-01` to `2012-08-06`).
     - **Hold-Out Test Set (final 20%):** $n_{\text{test}} = 147$ days (`2012-08-07` to `2012-12-31`).
   - All model parameters and dummy encodings are fitted **exclusively on the 584 training days** and evaluated out-of-sample on the 147 hold-out days.

#### Confirmed Numerical Findings

1. **Multicollinearity Audit — Primary Model vs. Collinear Model With `atemp` (`05_multiple_linear_regression/tables/regression_vif_diagnostics.csv`):**

| Encoded Predictor | Readable Name | Primary Model VIF (No `atemp`) | Primary Tolerance ($1/\text{VIF}$) | Collinear Model VIF (With `atemp`) |
|---|---|---:|---:|---:|
| `num__temp` | Normalized Temperature (`temp`) | **$3.6091$** | $0.2771$ | **$184.8565$** |
| `num__atemp` | Normalized Feeling Temp (`atemp`) | *Dropped* | — | **$179.2965$** |
| `cat__season_3` | Season 3: Fall (vs. Season 1) | **$4.6288$** | $0.2160$ | $4.7060$ |
| `cat__season_2` | Season 2: Summer (vs. Season 1) | **$2.6676$** | $0.3749$ | $2.6681$ |
| `num__hum` | Normalized Humidity (`hum`) | **$1.9176$** | $0.5215$ | $1.9374$ |
| `cat__season_4` | Season 4: Winter (vs. Season 1) | **$1.7834$** | $0.5607$ | $1.7902$ |
| `cat__weathersit_2` | Weather 2: Mist/Cloudy (vs. Clear 1) | **$1.5861$** | $0.6305$ | $1.5937$ |
| `cat__weathersit_3` | Weather 3: Light Snow/Rain (vs. Clear 1) | **$1.3083$** | $0.7644$ | $1.3206$ |
| `bin__yr` | Year Indicator (`yr`: $1 = 2012$) | **$1.2098$** | $0.8266$ | $1.2108$ |
| `num__windspeed` | Normalized Wind Speed (`windspeed`) | **$1.1846$** | $0.8442$ | $1.2463$ |
| `bin__workingday` | Working Day Indicator (`workingday = 1`) | **$1.0758$** | $0.9295$ | $1.0765$ |
| `bin__holiday` | Public Holiday Indicator (`holiday = 1`) | **$1.0702$** | $0.9344$ | $1.0786$ |

- **VIF Conclusion:** Dropping `atemp` reduces the maximum VIF from **$184.86$** to **$4.63$** (`cat__season_3`), so all $11$ predictors in the primary model satisfy $\text{VIF} < 5.0$.

2. **Fitted Multiple Linear Regression Coefficients (`05_multiple_linear_regression/tables/regression_ols_coefficients.csv`, Training Set $n = 584$):**
   - Omnibus Model Fit: **$R^2 = 0.8387$**, **Adjusted $R^2 = 0.8356$**, $F(11, 572) = 270.3766$, $p = 2.489 \times 10^{-218}$, $\text{AIC} = 9,362.38$, $\text{BIC} = 9,414.82$.

| Term | Predictor Description | Coef ($\hat{\beta}$) | Std. Beta ($\beta^*$) | IID OLS SE ($p$-value) | White HC3 SE ($t_{\text{HC3}}, p_{\text{HC3}}$) | Newey-West HAC SE ($p_{\text{HAC}}$) | Physical & Practical Interpretation (Ceteris Paribus) |
|---|---|---:|---:|---|---|---|----|
| `const` | Intercept (Ref: 2011, Season 1, Clear, Non-Workday) | **$+1,722.21$** | — | $217.80$ ($1.36\times 10^{-14}$) | $216.59$ ($t=7.95, p=1.84\times 10^{-15}$) | $256.61$ ($1.93\times 10^{-11}$) | Baseline expected rentals when continuous predictors $= 0$ in reference regime. |
| `num__temp` | Normalized Temperature (`temp`) | **$+4,714.31$** | **$+0.4962$** | $303.08$ ($9.31\times 10^{-46}$) | $348.77$ ($t=13.52, p=1.24\times 10^{-41}$) | $583.13$ ($6.25\times 10^{-16}$) | **$+471.43$ bikes/day per $+0.10$ `temp`** ($\approx \mathbf{+114.98}$ bikes/day per $+1^\circ\text{C}$). Second strongest standardized driver ($\beta^* = +0.4962$). |
| `num__hum` | Normalized Humidity (`hum`) | **$-1,218.46$** | $-0.1008$ | $281.23$ ($1.74\times 10^{-5}$) | $289.43$ ($t=-4.21, p=2.56\times 10^{-5}$) | $322.78$ ($0.00016$) | **$-121.85$ bikes/day per $+10\%$ relative humidity** ($\approx -12.18$ bikes/day per $+1\%$ humidity). |
| `num__windspeed` | Normalized Wind Speed (`windspeed`) | **$-2,675.83$** | $-0.1140$ | $429.18$ ($8.79\times 10^{-10}$) | $447.30$ ($t=-5.98, p=2.20\times 10^{-9}$) | $512.78$ ($1.81\times 10^{-7}$) | **$-267.58$ bikes/day per $+0.10$ `windspeed`** ($\approx \mathbf{-39.94}$ bikes/day per $+1\text{ km/h}$ wind speed). |
| `bin__yr` | Year Indicator (`1 = 2012` vs. `0 = 2011`) | **$+1,947.85$** | **$+0.5276$** | $68.19$ ($3.45\times 10^{-112}$) | $72.58$ ($t=26.84, p=1.21\times 10^{-158}$) | $105.43$ ($3.29\times 10^{-76}$) | **$+1,947.85$ bikes/day** structural expansion in 2012 vs. 2011 at identical weather/season. Largest standardized effect ($\beta^* = +0.5276$). |
| `bin__holiday` | Public Holiday (`1 = Yes` vs. `0 = No`) | **$-451.16$** | $-0.0412$ | $190.22$ ($0.0180$) | $238.01$ ($t=-1.90, p=0.0580$) | $217.46$ ($0.0380$) | **$-451.16$ bikes/day** penalty on public holidays ($p_{\text{IID}}=0.018, p_{\text{HAC}}=0.038, p_{\text{HC3}}=0.058$). |
| `bin__workingday` | Working Day (`1 = Workday` vs. `0 = Weekend`) | **$+66.82$** | $+0.0174$ | $67.02$ ($0.3192$) | $75.48$ ($t=0.89, p=0.3760$) | $78.40$ ($0.3941$) | **Statistically non-significant ($p > 0.31$)** — confirms H1 finding that weekday commuter gains and weekend casual losses offset each other. |
| `cat__season_2` | Season 2: Summer (vs. Season 1) | **$+1,162.90$** | $+0.3022$ | $105.53$ ($9.66\times 10^{-26}$) | $120.78$ ($t=9.63, p=6.06\times 10^{-22}$) | $207.03$ ($1.94\times 10^{-8}$) | **$+1,162.90$ bikes/day** in Mar 21–Jun 20 vs. Dec 21–Mar 20 beyond temperature alone. |
| `cat__season_3` | Season 3: Fall (vs. Season 1) | **$+751.76$** | $+0.1800$ | $150.89$ ($8.35\times 10^{-7}$) | $170.45$ ($t=4.41, p=1.03\times 10^{-5}$) | $285.61$ ($0.00849$) | **$+751.76$ bikes/day** in Jun 21–Sep 22 vs. Dec 21–Mar 20 holding `temp` constant. |
| `cat__season_4` | Season 4: Winter (vs. Season 1) | **$+1,465.42$** | $+0.2947$ | $111.52$ ($1.19\times 10^{-34}$) | $96.49$ ($t=15.19, p=4.32\times 10^{-52}$) | $146.54$ ($1.52\times 10^{-23}$) | **$+1,465.42$ bikes/day** in Sep 23–Dec 20 vs. Dec 21–Mar 20 holding `temp` constant (autumn cycling inertia & membership ramp-up). |
| `cat__weathersit_2` | Weather 2: Mist/Cloudy (vs. Clear 1) | **$-363.47$** | $-0.0951$ | $80.79$ ($8.28\times 10^{-6}$) | $78.76$ ($t=-4.62, p=3.93\times 10^{-6}$) | $78.99$ ($4.20\times 10^{-6}$) | **$-363.47$ bikes/day** under misty/cloudy skies compared to clear weather at equal temp/humidity. |
| `cat__weathersit_3` | Weather 3: Light Snow/Rain (vs. Clear 1) | **$-1,660.90$** | $-0.1606$ | $198.63$ ($4.73\times 10^{-16}$) | $223.47$ ($t=-7.43, p=1.07\times 10^{-13}$) | $203.41$ ($3.21\times 10^{-16}$) | **$-1,660.90$ bikes/day** under light snow/rain compared to clear weather at equal temp/humidity. |

3. **Model Comparison Across Training & Unseen Hold-Out Test Sets (`05_multiple_linear_regression/tables/regression_model_comparison.csv`):**

| Model Specification | Role | Predictors ($p$) | Train MAE | Train RMSE | Train $R^2$ | Train Adj. $R^2$ | Test MAE | Test RMSE | Test $R^2$ | Test Mean Bias ($\widehat{Y} - Y$) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Mean Baseline (`DummyRegressor`)** | Predicts Train Mean ($4,153.60$) | 0 | $1,442.95$ | $1,787.36$ | $0.0000$ | $0.0000$ | $2,290.41$ | $2,560.56$ | $-0.8657$ | $-1,744.20$ |
| **Primary Multiple Linear Regression (OLS)** | **Primary Model (Drops `atemp`)** | **11** | **$539.45$** | **$717.85$** | **$0.8387$** | **$0.8356$** | **$891.69$** | **$1,164.87$** | **$0.6139$** | **$-204.70$** |
| **Supplemental Collinear OLS (With `atemp`)** | Demonstrates VIF Collinearity | 12 | $538.80$ | $717.65$ | $0.8388$ | $0.8354$ | $894.37$ | $1,165.61$ | $0.6134$ | $-209.01$ |
| **Supplemental Ridge ($\alpha = 0.01$)** | $L_2$-Regularized Check | 11 | $539.45$ | $717.85$ | $0.8387$ | $0.8356$ | $891.71$ | $1,164.89$ | $0.6139$ | $-204.75$ |

- **Out-of-Sample Improvement Over Baseline:**
  - On the unseen 147-day late-2012 test horizon (`2012-08-07` to `2012-12-31`), Primary OLS reduces **Test MAE by $61.07\%$** (from $2,290.41$ to $891.69$ bikes/day) and reduces **Test RMSE by $54.51\%$** (from $2,560.56$ to $1,164.87$ bikes/day), achieving **Test $R^2 = 0.6139$** vs. $-0.8657$ for the naive mean baseline.
  - Note that adding `atemp` (`Collinear OLS`) slightly **worsens** out-of-sample Test MAE ($894.37$ vs. $891.69$) and Test RMSE ($1,165.61$ vs. $1,164.87$) while inflating VIF to $184.86$, confirming that dropping `atemp` improves both interpretability and generalization.

4. **Residual & Assumption Diagnostics (`05_multiple_linear_regression/tables/regression_residual_diagnostics.csv`):**
   - **Heteroscedasticity:** Breusch-Pagan $\text{LM} = 62.5664$ ($p = 3.082 \times 10^{-9}$), $F = 6.2394$ ($p = 9.370 \times 10^{-10}$). Residual variance increases at higher fitted rental volumes (`fig16`).
   - **Autocorrelation (Serial Dependence):** Durbin-Watson $d = 1.2253$ ($< 2.0$ indicates positive first-order autocorrelation); Ljung-Box lag-1 $Q = 87.6334$ ($p = 7.878 \times 10^{-21}$), lag-7 $Q = 145.7213$ ($p = 3.211 \times 10^{-28}$).
   - **Residual Normality:** Shapiro-Wilk $W = 0.9764$ ($p = 4.320 \times 10^{-8}$), Jarque-Bera $= 81.5531$ ($p = 1.954 \times 10^{-18}$), Residual Skewness $= -0.4031$, Excess Kurtosis $= +1.6691$. Departure from exact normality is driven by negative tail shocks on extreme storm/shutdown days (`fig17`).
   - **Influential Observations (Cook's Distance):** Threshold $4/n_{\text{train}} = 0.006849$; $37$ training days exceed $4/n$, with maximum Cook's distance $D_{\max} = 0.05899$ on `2012-04-22` (far below the critical $D > 0.50$ or $1.0$ threshold, meaning no single day unduly distorts the OLS hyperplane).
   - **Largest Hold-Out Test Error:** Occurs on `2012-10-30` (`instant = 669`, the day after Hurricane Sandy landfall), where actual `cnt = 1,096`, predicted $\hat{y} = 4,763.07$, and residual $e = -3,667.07$ bikes/day (`fig18`).
   - **How Diagnostics Are Addressed:** Because Breusch-Pagan and Ljung-Box detect heteroscedasticity and serial correlation, `regression_ols_coefficients.csv` reports both **White's HC3 heteroscedasticity-robust** and **Newey-West HAC (lag = 7)** standard errors alongside classical IID OLS standard errors. Every core driver (`temp`, `hum`, `windspeed`, `yr`, `season`, `weathersit`) remains highly statistically significant ($p < 0.01$) across all three covariance estimators.

#### Supporting Package Files
- Tables:
  - `05_multiple_linear_regression/tables/regression_model_comparison.csv`
  - `05_multiple_linear_regression/tables/regression_ols_coefficients.csv`
  - `05_multiple_linear_regression/tables/regression_vif_diagnostics.csv`
  - `05_multiple_linear_regression/tables/regression_residual_diagnostics.csv`
  - `05_multiple_linear_regression/tables/train_predictions.csv`
  - `05_multiple_linear_regression/tables/test_predictions.csv`
- Figures:
  - **Figure 15 (`05_multiple_linear_regression/figures/fig15_regression_actual_vs_predicted.png`):** Parity plot of Actual vs. Predicted `cnt` on Training ($n=584$) and Hold-Out Test ($n=147$) sets vs. $45^\circ$ identity line and mean baseline.
  - **Figure 16 (`05_multiple_linear_regression/figures/fig16_regression_residuals_vs_fitted.png`):** Residuals ($e_i = y_i - \hat{y}_i$) vs. Fitted values ($\hat{y}_i$) across train and test sets with LOWESS trend and annotated extreme shocks.
  - **Figure 17 (`05_multiple_linear_regression/figures/fig17_regression_residual_qq_hist.png`):** 2-panel diagnostic of training residuals (Histogram/KDE vs. Normal curve + Standardized Normal Q-Q plot).
  - **Figure 18 (`05_multiple_linear_regression/figures/fig18_regression_temporal_predictions_errors.png`):** 2-panel chronological hold-out forecast (`2012-08-07` to `2012-12-31`) comparing Actual `cnt`, Primary OLS predictions, and Mean Baseline, plus daily residual error bars.

---

## 6. Methodological Limitations & Cautions for the Report Discussion
1. **Observational Non-Causality:** Weather, season, and calendar indicators are observational rather than experimentally randomized. Regression slopes and hypothesis tests quantify conditional expectations and statistical associations, not interventional causal effects.
2. **Time-Series Dependence & Dynamic Growth:** Consecutive daily counts exhibit autocorrelation ($\text{DW} = 1.2253$), and the binary indicator `yr` captures a step-change between 2011 and 2012 ($+1,947.85$ bikes/day). In late 2012 (the test period), continued month-over-month subscriber growth causes the static `yr = 1` dummy to slightly underpredict peak autumn days (mean test prediction bias $= -204.70$ bikes/day).
3. **Non-Linear Thermal Saturation at Extreme Heat:** Linear OLS assumes a constant slope $+114.98$ bikes/day per $+1^\circ\text{C}$, whereas `fig04` and `fig14` show that demand flattens when temperature exceeds $\approx 31^\circ\text{C}$ ($\text{temp} > 0.75$).
4. **Realized vs. Forecasted Weather:** In `day.csv`, `temp`, `hum`, `windspeed`, and `weathersit` are realized daily summaries. Operational day-ahead bike rebalancing requires plugging meteorological *forecasts* into the regression equation, introducing weather-forecast uncertainty.
