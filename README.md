# Statistical Analysis and Visualization of Daily Bike-Rental Demand

**Course:** Data Analysis and Visualization (Academic Year 2026–2027)  
**Dataset:** UCI Machine Learning Repository — *Bike Sharing Dataset* (`data/raw/day.csv`, $N = 731$ days, $p = 16$ columns)  
**DOI:** [`10.24432/C5W894`](https://doi.org/10.24432/C5W894) | **Official Source:** <https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset>

---

## 1. Project Overview & Scope

This repository implements a fully reproducible, academically rigorous statistical and machine learning pipeline analyzing daily bike-rental demand (`cnt`) across two consecutive years (2011–2012) from the Capital Bikeshare system in Washington, D.C.

All technical requirements for **Phases 0 through 6** (plus the 20-point **Python Implementation & Reproducibility** rubric component) are implemented, executed, and verified via automated `pytest` tests:
- **Phase 0:** Assignment & eligibility audit (`docs/RUBRIC_TRACEABILITY.md`, `docs/RESEARCH_DESIGN.md`, `docs/STATISTICAL_DECISIONS.md`).
- **Phase 1:** Official dataset acquisition, SHA-256 verification, schema/domain validation, and target identity verification (`cnt == casual + registered` on all 731 rows).
- **Phase 2 (15/100):** Exploratory Data Analysis (EDA), subgroup breakdowns, Tukey $1.5 \times \text{IQR}$ and $|z| > 3$ outlier diagnostics, and 5 purposeful chart types (`fig01`–`fig05`).
- **Phase 3 (15/100):** Probability Distribution Analysis for `cnt` (proving severe Poisson overdispersion with $\text{Var}/\text{Mean} = 833.15$, comparing Negative Binomial and Normal fits) and bounded continuous weather variables `temp`, `hum`, and `windspeed` (`fig06`–`fig08`).
- **Phase 4 (15/100):** Pre-registered Hypothesis Testing:
  - **H1:** Welch Two-Sample $t$-Test on `workingday` (`fig09`).
  - **H2:** Ordinary One-Way ANOVA, Welch Heteroscedastic ANOVA, and Kruskal-Wallis test across `season` with Tukey HSD and Holm-Welch post-hoc comparisons (`fig10`).
  - **H3:** Pearson $\chi^2$ Test of Independence (plus Likelihood-Ratio $G^2$ and $2 \times 2$ Fisher Exact check) between `weathersit` and median-dichotomized `high_demand` (`fig11`).
- **Phase 5 (15/100):** Pearson Linear ($r$) and Spearman Rank ($\rho$) Correlation Analysis with Fisher-$z$ 95% CIs, Holm-adjusted $p$-values, and collinearity diagnosis (`fig12`–`fig14`).
- **Phase 6 (20/100):** Anti-Leakage Multiple Linear Regression (OLS) using a chronological 80/20 train/test split (`2011-01-01`..`2012-08-06` vs `2012-08-07`..`2012-12-31`), comparing a Mean Baseline (`DummyRegressor`) against Primary OLS (`LinearRegression`), VIF multicollinearity audit, and Classical IID, White HC3, and Newey-West HAC (lag=7) standard errors (`fig15`–`fig18`).

> **Note on Phases 7 & 8:** Per user instruction, execution stops after Phase 6 so the user can author Phase 7 (Academic Report) and Phase 8 (Presentation Slides & Video) directly using the generated tables in `outputs/tables/`, the 18 high-resolution 300-DPI figures in `outputs/figures/`, and the single-source-of-truth `outputs/results.json`.

---

## 2. Reproducible Execution Instructions

### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.run_all
python -m pytest -q

# Launch the interactive Streamlit dashboard
streamlit run app/streamlit_app.py --server.port 8502
```

### Linux / macOS (Bash / Zsh)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.run_all
python -m pytest -q

# Launch the interactive Streamlit dashboard
streamlit run app/streamlit_app.py --server.port 8502
```

---

## 3. Repository Structure

```text
DA_final/
├── README.md
├── requirements.txt                  # Pinned, tested Python dependencies
├── .gitignore
├── PROGRESS.md                       # Phase-by-phase execution audit log
├── FINAL_HANDOFF.md                  # Rubric audit table, key findings & user checklist
├── docs/
│   ├── RUBRIC_TRACEABILITY.md        # 100-point rubric mapping matrix
│   ├── DATA_DICTIONARY.md            # Provenance, SHA-256 hashes & 16-column codebook
│   ├── RESEARCH_DESIGN.md            # Pre-declared hypotheses & study design
│   ├── STATISTICAL_DECISIONS.md      # Methodological & anti-leakage engineering log
│   ├── FIGURE_REGISTER.md            # Catalog of all 18 figures (300 DPI)
│   └── REFERENCES.md                 # Verified academic & software references
├── data/raw/
│   ├── day.csv                       # Official unmodified daily dataset (731 x 16)
│   └── Readme.txt                    # Official UCI codebook
├── src/
│   ├── __init__.py
│   ├── load_validate.py              # Phase 1: Acquisition, SHA-256 & domain checks
│   ├── descriptive_eda.py            # Phase 2: Descriptive stats, subgroups & outliers
│   ├── probability.py                # Phase 3: Poisson overdispersion, NegBin, Normal, Beta
│   ├── hypothesis_tests.py           # Phase 4: H1 Welch t-test, H2 ANOVA, H3 Chi-Square
│   ├── correlations.py               # Phase 5: Pearson r, Spearman rho & Fisher-z CIs
│   ├── regression.py                 # Phase 6: Chronological 80/20 OLS, VIF, HC3/HAC SEs
│   ├── visualizations.py             # Visualization facade delegating to src/plots/
│   ├── plots/                        # Modular scientific plotting subpackage
│   │   ├── __init__.py
│   │   ├── style.py                  # Shared palette, rcParams, Q-Q & stat-box helpers
│   │   ├── eda_plots.py              # Figures 1–5 (EDA)
│   │   ├── prob_hypos_plots.py       # Figures 6–11 (Probability & Hypotheses H1–H3)
│   │   └── corr_reg_plots.py         # Figures 12–18 (Correlations & OLS Regression)
│   ├── artifact_generation.py        # Builds and executes notebooks/analysis.ipynb
│   └── run_all.py                    # Master end-to-end execution script
├── notebooks/
│   └── analysis.ipynb                # Executed, human-readable walkthrough notebook
├── app/                              # Interactive Streamlit Web Application
│   ├── __init__.py
│   ├── helpers.py                    # Caching, cohort filtering & demand simulation engine
│   └── streamlit_app.py              # 5-view interactive dashboard
├── tests/
│   ├── test_dashboard_app.py         # Full automated tests for app views & simulators
│   ├── test_data_integrity.py        # Dimensions, schema, SHA-256 & cnt==casual+registered
│   ├── test_hypotheses.py            # H1, H2, H3 statistical validity & Cochran check
│   ├── test_no_leakage.py            # Strict predictor allowlist & chronological split
│   ├── test_regression.py            # Metric consistency, baseline parity & VIF reduction
│   └── test_output_contracts.py      # Figures, CSV tables & deterministic rerun verification
└── outputs/
    ├── dataset_audit.json            # Machine-readable Phase 1 data audit
    ├── results.json                  # Single source of truth for all computed numbers
    ├── figures/                      # 18 publication-grade 300 DPI PNG figures
    ├── tables/                       # 23 generated CSV summary tables
    └── model/                        # Saved train_predictions.csv & test_predictions.csv
```
