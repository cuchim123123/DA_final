# Architectural & Methodological Decision Log (`DECISIONS.md`)

This log records engineering, statistical, and modeling decisions made prior to and during implementation so every design choice is transparent and auditable.

---

## Decision 1 — Scope, Authority & Clean-Room Originality
- **Context:** The local workspace (`DA_midterm/`) contains `TELCO_CHURN_MIDTERM_AGENT_PACK/` (`00` through `04`) but does not contain the raw `.docx` copy of `De KT giua ky_HK1_NH26-27(1).docx`.
- **Decision:** Treat `01_OFFICIAL_REQUIREMENTS_EN.md` as the authoritative English specification of instructor requirements, execute Phases 0–7 strictly in clean-room Python (reproducing all analyses directly from IBM's original CSV), and flag any user confirmation items (team member roster, confirmation against raw Vietnamese `.docx`) in `PROGRESS.md` and `REQUIREMENTS_COVERAGE.md`.
- **Originality Rule:** Zero source code, plots, tables, pre-trained pickles, or reported metrics are copied from `UtkarshRai-ds/telco-churn-prediction`.

## Decision 2 — Data Provenance, Schema Verification & `TotalCharges` Treatment
- **Context:** In-memory inspection of IBM's `Telco-Customer-Churn.csv` ($7,043$ rows, $21$ columns) confirmed two critical empirical facts:
  1. `TotalCharges` is stored as string due to **11 whitespace `" "` entries ($0.156\%$)**, and **all 11 blank entries correspond 1:1 to `tenure == 0` (`Churn == "No"`)**.
  2. There are **0 duplicate rows** and **7,043 unique `customerID` values**, while **22 pairs/groups share identical non-ID feature profiles** (primarily `tenure = 1`, single phone service, no internet, mailed check). Because they carry distinct `customerID`s in discrete plan tiers, they represent valid cross-sectional records and must **not** be dropped.
  3. Service-hierarchy dependencies are 100% consistent in the raw file: `PhoneService == "No"` ($n = 682$) maps exclusively to `MultipleLines == "No phone service"`; `InternetService == "No"` ($n = 1,526$) maps exclusively to `"No internet service"` across all 6 online add-on columns.
- **Decision:**
  - Keep `data/raw/Telco-Customer-Churn.csv` read-only with SHA-256 verification.
  - Convert `TotalCharges` via `pd.to_numeric(..., errors="coerce")` for descriptive/diagnostic auditing so the 11 blank values are explicitly counted as missing (`0.156%`).
  - Preserve all 7,043 rows (no silent row deletion). Inside preprocessing (`scikit-learn` `ColumnTransformer` / custom transformer fitted *only on training data*), test whether `tenure == 0` domain fill (`0.0`) vs. training-fold median imputation produces equivalent CV performance; use leak-free `SimpleImputer(strategy="median")` in the ML pipeline (optionally paired with explicit `TotalCharges_missing` awareness or verified sensitivity check in Phase 1/3) so any hypothetical unseen missing value is handled purely from training parameters.
  - Validate service-hierarchy consistency both on dataset ingestion and inside the interactive single-customer hypothetical risk calculator in Streamlit.

## Decision 3 — Cross-Sectional Framing & Stratified Train/Test Split (M-07)
- **Context:** Each record is a static customer snapshot ("churn within the last month") with duration `tenure` ($0..72$ months), not a calendar date series.
- **Decision:**
  - Prohibit fake time-series charts or artificial chronological train/test splits.
  - Partition the 7,043 records once at the outset using **80% / 20% Stratified Random Sampling** (`random_state=42`, stratified on `Churn`):
    - **Development / Training Set (`n = 5,634`, 80.0%):** Used exclusively for Stratified 5-Fold Cross-Validation, hyperparameter selection, calibration evaluation, and validation threshold tuning (`F1` / `F2` / business-cost optimization via out-of-fold probabilities).
    - **Sealed Hold-Out Test Set (`n = 1,409`, 20.0%):** Preserves the exact class prevalence ($\approx 26.54\%$ churn) and remains strictly untouched until final benchmark evaluation and chart generation.

## Decision 4 — Analytical Rigor Across the Four Layers
1. **Descriptive Analytics:** Report both **absolute volumes ($n$)** and **churn rates (%)** with exact denominators and **95% Wilson score confidence intervals** so high-rate tiny segments cannot mislead readers. Compute distributional statistics (mean, SD, median, IQR, skewness) for `tenure`, `MonthlyCharges`, and `TotalCharges`.
2. **Diagnostic Analytics:**
   - For categorical associations with `Churn`, compute Pearson $\chi^2$ tests, Holm-Bonferroni adjusted $p$-values, **Cramér's $V$**, and unadjusted Odds Ratios.
   - For continuous features (`tenure`, `MonthlyCharges`, `TotalCharges`) vs. `Churn`, compute Welch's $t$-test, Mann-Whitney $U$ test, and non-parametric rank-biserial correlation / Cliff's $\delta$ effect sizes.
   - Address **confounding** explicitly: e.g., `TotalCharges` correlates negatively with churn purely because it equals $\approx \text{tenure} \times \text{MonthlyCharges}$ (tenure confounding); similarly `Fiber optic` higher churn co-occurs with shorter tenure and electronic check payment. A multivariable adjusted Logistic Regression summary in Diagnostics separates marginal associations from adjusted associations while strictly disclaiming causality.
3. **Predictive Analytics (M-06, M-08):**
   - Compare **four specifications** under identical Stratified 5-Fold CV and identical hold-out evaluation:
     - **Reference Floor:** `DummyClassifier(strategy="most_frequent")` (reported strictly as no-skill prevalence reference, $73.46\%$ accuracy with $0.00$ recall).
     - **Model 1 (Baseline Algorithmic Classifier):** Regularized **Logistic Regression** (`OneHotEncoder(handle_unknown="ignore")` + `StandardScaler`, CV-tuned `C` and optional class weighting).
     - **Model 2 (Advanced Bagging Ensemble):** **Random Forest Classifier** (CV-tuned depth/min_samples_leaf/max_features).
     - **Model 3 (Advanced Boosting Ensemble):** **HistGradientBoostingClassifier** (CV-tuned learning rate, max_leaf_nodes, min_samples_leaf).
   - Assess probability calibration via Brier score, Expected Calibration Error (ECE) / reliability curve, and optionally compare isotonic/sigmoid calibration if any top model shows miscalibration on CV out-of-fold predictions.
   - Report default $0.50$ threshold metrics alongside a validation-selected operational threshold (maximizing out-of-fold $F_1$ or Youden/recall-constrained threshold, clearly justified by asymmetric cost of missed churners vs. wasted outreach).
   - Provide multi-angle explainability: (a) Logistic Regression odds ratios ($\exp(\beta)$) mapped cleanly to categorical levels, and (b) Held-out Test Permutation Importance (measuring drop in `ROC-AUC` and `PR-AUC` when permuting each raw column before the pipeline!). Permuting **original raw columns** directly eliminates fragmented dummy-variable importance distortion!
4. **Prescriptive Analytics (M-09):**
   - Segment the population into clear operational risk tiers (e.g., High / Medium / Low risk based on calibrated predicted probabilities) plus targetable behavioral segments (e.g., Month-to-month + Fiber optic + early tenure $\le 12$ months + no TechSupport/OnlineSecurity).
   - Cite exact numbers from Descriptive (segment size, base churn rate, monthly revenue at risk), Diagnostic ($\chi^2$ / Cramér's $V$ / adjusted odds), and Predictive (tier predicted churn rate vs. realized test churn rate, precision/recall/lift at top $K\%$ outreach capacity).
   - Separate observed data from user-adjustable **scenario assumptions** (outreach unit cost, assumed intervention uplift %, horizon months) and run a sensitivity grid so no illustrative retention outcome is mistaken for a measured causal finding.

## Decision 5 — Visualization Variety (M-05, $\ge 6$ Genuinely Different Chart Types)
All charts are rendered at 300 DPI via `matplotlib`/`seaborn` from executed outputs and also displayed cleanly in Streamlit:
1. **Grouped / Annotated Bar Charts with 95% Wilson CIs** (`fig01_churn_by_contract_payment.png`)
2. **Overlaid Histograms with KDE Curves** (`fig02_numeric_distributions_kde.png`)
3. **Boxplots** (`fig03_charges_by_contract_churn_boxplot.png`)
4. **Violin Plots** (`fig04_tenure_violin_by_contract_churn.png`)
5. **Binned Hexbin / Scatter Plot** (`fig05_tenure_vs_monthly_charges_scatter.png`)
6. **Heatmaps** (`fig06_diagnostic_association_heatmaps.png` — Cramér's $V$ & segment churn rate matrix; plus `fig08_confusion_matrices_heatmap.png`)
7. **Evaluation Curve Plots (ROC, Precision-Recall, Calibration Reliability)** (`fig07_model_roc_pr_calibration_curves.png`)
8. **Horizontal Diverging Bar / Dot Plot (Permutation Importance & Odds Ratios)** (`fig09_model_explainability.png`)
9. **Dual-Axis / Cumulative Lift & Scenario Sensitivity Heatmap/Chart** (`fig10_prescriptive_targeting_lift.png`)
*(That provides 9 genuinely distinct chart families covering all requirements cleanly!)*

## Decision 6 — Isolated Environment & Modular Package Structure
- Create a standalone Python virtual environment at `DA_midterm/.venv` with pinned `pyproject.toml` and `requirements.txt` (including `pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib`, `seaborn`, `streamlit`, `joblib`, `pillow`, `pytest`, `ruff`).
- Organize code cleanly under `src/telco_churn/` with separate single-purpose modules and thin `app/streamlit_app.py` orchestration so business calculations never live inside UI code.
