# Data Dictionary & Provenance Specification (`day.csv`)

## 1. Dataset Provenance & Integrity Metadata

- **Dataset Name:** Bike Sharing Dataset (`day.csv` — Daily Aggregation)
- **Official Source Repository:** UCI Machine Learning Repository — <https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset>
- **Archive Download URL:** `https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip`
- **Digital Object Identifier (DOI):** `10.24432/C5W894` (<https://doi.org/10.24432/C5W894>)
- **Original Creators:** Hadi Fanaee-T and Joao Gama, Laboratory of Artificial Intelligence and Decision Support (LIAAD), University of Porto, Portugal.
- **Primary Publication Citation:**
  > Fanaee-T, H., & Gama, J. (2013). Event labeling combining ensemble detectors and background knowledge. *Progress in Artificial Intelligence*, 2(2–3), 113–127. Springer Berlin Heidelberg. <https://doi.org/10.1007/s13748-013-0040-3>
- **Underlying Operational Sources:**
  - Rental logs: Capital Bikeshare system, Washington, D.C., USA (<http://capitalbikeshare.com/system-data>)
  - Meteorological logs: Freemeteo weather station data (<http://www.freemeteo.com>)
  - Public holiday schedule: District of Columbia Department of Human Resources (<http://dchr.dc.gov/page/holiday-schedule>)
- **Temporal Coverage:** January 1, 2011 (`2011-01-01`) to December 31, 2012 (`2012-12-31`) — 731 consecutive calendar days (2012 is a leap year with 366 days; $365 + 366 = 731$).
- **Cryptographic Verification (SHA-256):**
  - `bike+sharing+dataset.zip` (279,992 bytes): `b70182d0d0508e9abbb79306ce5c0cec34869000f8220175ac83d11dbe845401`
  - `data/raw/day.csv` (57,569 bytes): `a6bcf826782d3c0fbfdcbeead17cd0884185a0dafe8ff10cd48a874ee7ba18be`
  - `data/raw/Readme.txt` (5,607 bytes): `b92c8628622948bf0828c43a1b315d1517c3d7fd63654730d0dea379b8e88175`
- **Granularity Separation Rule:** The UCI archive also includes `hour.csv` (17,379 hourly records; catalog total often listed as 17,389 across combined metadata). This study analyzes **exclusively `day.csv` ($N = 731$ days, $p = 16$ columns)** and never mixes hourly and daily observational units.

---

## 2. Complete Variable Codebook (`day.csv`, 16 Columns)

| # | Column Name | Data Type | Statistical Scale | Domain / Legal Values | Official Codebook Definition & Normalization (`Readme.txt`) | Analytical & Modeling Role |
|---:|---|---|---|---|---|---|
| 1 | `instant` | `int64` | Identifier / Index | $\{1, 2, \dots, 731\}$ | Sequential record index from day 1 to day 731. | **Identifier only.** Strictly excluded from correlations and regression predictors ($X$) to prevent time-index leakage. |
| 2 | `dteday` | `string` / `datetime64[ns]` | Temporal Index | `2011-01-01` to `2012-12-31` | Calendar date in ISO `YYYY-MM-DD` format without missing days. | **Chronological index.** Used to verify continuity and perform the strict 80/20 chronological train/test split; excluded as a raw regression feature. |
| 3 | `season` | `int64` | Nominal Categorical | $\{1, 2, 3, 4\}$ | Official UCI `Readme.txt` labels: `1: Spring ("springer")`, `2: Summer`, `3: Fall`, `4: Winter`. *(See Section 3 note on calendar date spans).* | **Grouping factor** in EDA & H2 (One-Way ANOVA); **One-Hot Encoded** categorical predictor in OLS regression; excluded from continuous Pearson/Spearman matrices. |
| 4 | `yr` | `int64` | Binary Indicator | $\{0, 1\}$ | Year indicator: `0 = 2011` ($n=365$), `1 = 2012` ($n=366$). | **Structural growth indicator** in EDA and OLS regression (captures year-over-year network expansion). |
| 5 | `mnth` | `int64` | Cyclic / Ordinal Discrete | $\{1, 2, \dots, 12\}$ | Calendar month (`1 = January` to `12 = December`). | **Descriptive temporal variable.** Excluded from the primary parsimonious OLS specification to avoid structural collinearity with `season`. |
| 6 | `holiday` | `int64` | Binary Indicator | $\{0, 1\}$ | `1` if the day is a designated D.C. public holiday (non-weekend), `0` otherwise. | **Binary predictor** in EDA and OLS regression. |
| 7 | `weekday` | `int64` | Cyclic Categorical | $\{0, 1, 2, 3, 4, 5, 6\}$ | Day of week (`0 = Sunday`, `1 = Monday`, ..., `6 = Saturday`; verifiable since `2011-01-01` was a Saturday = `6`). | **Descriptive calendar variable.** Summarized via `workingday` in hypothesis testing and primary OLS model. |
| 8 | `workingday` | `int64` | Binary Indicator | $\{0, 1\}$ | `1` if the day is neither a weekend nor a public holiday; `0` otherwise (weekends + holidays). | **Primary binary factor** in H1 (Welch Two-Sample t-test) and **binary predictor** in OLS regression. |
| 9 | `weathersit` | `int64` | Ordinal / Categorical | $\{1, 2, 3, 4\}$ *(in `day.csv`, only $\{1, 2, 3\}$ occur)* | Daily weather situation:<br>`1`: Clear, Few clouds, Partly cloudy<br>`2`: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist<br>`3`: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds<br>`4`: Heavy Rain + Ice Pellets + Thunderstorm + Mist, Snow + Fog *(0 days in `day.csv`; occurs only in `hour.csv`)* | **Categorical factor** in EDA and H3 (Chi-Square test of independence); **One-Hot Encoded** predictor in OLS regression. |
| 10 | `temp` | `float64` | Continuous Ratio (Normalized) | $[0, 1]$ (Observed: $[0.0591, 0.8617]$) | Normalized ambient temperature in Celsius.Per `Readme.txt`: values divided by $41^\circ\text{C}$ ($\text{temp}_{\text{C}} \approx 41 \times \text{temp}$). | **Primary continuous predictor** in EDA, Probability Distribution Analysis (Chapter 6), Correlation Analysis (Chapter 8), and OLS Regression (Chapter 9). |
| 11 | `atemp` | `float64` | Continuous Ratio (Normalized) | $[0, 1]$ (Observed: $[0.0791, 0.8409]$) | Normalized "feeling" (apparent) temperature in Celsius. Per `Readme.txt`: values divided by $50^\circ\text{C}$ ($\text{atemp}_{\text{C}} \approx 50 \times \text{atemp}$). | **Continuous variable** in EDA and Correlation Analysis; **excluded from primary OLS model** due to extreme collinearity with `temp` ($r = 0.9917$, $\text{VIF}_{\text{temp}} = 184.86$, $\text{VIF}_{\text{atemp}} = 179.30$), demonstrated in VIF audit tables. |
| 12 | `hum` | `float64` | Continuous Ratio (Normalized) | $[0, 1]$ (Observed: $[0.0000, 0.9725]$) | Normalized relative humidity divided by $100$ ($\text{hum}_{\%} = 100 \times \text{hum}$). Note: 1 day (`2011-03-10`) records `hum = 0.0`. | **Continuous predictor** in EDA, Probability Diagnostics, Correlation Analysis, and OLS Regression. |
| 13 | `windspeed` | `float64` | Continuous Ratio (Normalized) | $[0, 1]$ (Observed: $[0.0224, 0.5075]$) | Normalized wind speed divided by $67$ ($\text{wind}_{67} = 67 \times \text{windspeed}$). | **Continuous predictor** in EDA, Probability Diagnostics, Correlation Analysis, and OLS Regression. |
| 14 | `casual` | `int64` | Discrete Count | $\mathbb{Z}_{\ge 0}$ (Observed: $[2, 3410]$) | Daily count of bike rentals by non-registered (casual) users. | **Component outcome.** **Strictly forbidden in regression $X$** because `cnt = casual + registered` (target leakage). |
| 15 | `registered` | `int64` | Discrete Count | $\mathbb{Z}_{\ge 0}$ (Observed: $[20, 6946]$) | Daily count of bike rentals by registered members. | **Component outcome.** **Strictly forbidden in regression $X$** because `cnt = casual + registered` (target leakage). |
| 16 | `cnt` | `int64` | Discrete Count | $\mathbb{Z}_{\ge 0}$ (Observed: $[22, 8714]$) | Total daily bike rentals (`cnt = casual + registered`). | **Primary Response Variable ($Y$)** across all analytical chapters. |

---

## 3. Methodological Note on `season` Coding vs. Calendar Dates

In `data/raw/Readme.txt` (line 67), the dataset creators define:
- `1: springer` (Spring)
- `2: summer` (Summer)
- `3: fall` (Fall)
- `4: winter` (Winter)

Inspection of the actual date transition boundaries in `day.csv` reveals that the integer codes follow astronomical solstice/equinox boundaries shifted by one label relative to meteorological convention:
- `season = 1` ("Spring" in UCI codebook): **Dec 21 – Mar 20** ($n = 181$ days; astronomically Northern Hemisphere Winter, lowest temperatures).
- `season = 2` ("Summer" in UCI codebook): **Mar 21 – Jun 20** ($n = 184$ days; astronomically Northern Hemisphere Spring).
- `season = 3` ("Fall" in UCI codebook): **Jun 21 – Sep 22** ($n = 188$ days; astronomically Northern Hemisphere Summer, highest temperatures).
- `season = 4` ("Winter" in UCI codebook): **Sep 23 – Dec 20** ($n = 178$ days; astronomically Northern Hemisphere Fall).

**Standardization Decision:** To remain 100% faithful to the official UCI codebook (`Readme.txt`) while preventing physical misinterpretation of temperature patterns, this project uses the official UCI code numbers and names with explicit calendar annotations in tables and prose:
- `1: Spring (UCI Code 1: Dec 21–Mar 20)`
- `2: Summer (UCI Code 2: Mar 21–Jun 20)`
- `3: Fall (UCI Code 3: Jun 21–Sep 22)`
- `4: Winter (UCI Code 4: Sep 23–Dec 20)`
