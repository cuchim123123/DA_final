# MASTER IMPLEMENTATION PLAN — BIKE SHARING DATA ANALYSIS

**Course:** Data Analysis and Visualization  
**Assignment:** End-of-Semester Research Project, Academic Year 2026–2027  
**Language:** English for the implementation plan, all code, documentation, report, slides, chart labels, and presentation script unless the instructor explicitly requires another language  
**Goal:** Meet every published full-credit criterion (target: 100/100); actual grading remains the instructor's decision.

> **AI agent mission:** Act as a competent Python data analyst, applied statistician, reproducibility engineer, academic report writer, and independent QA reviewer. **Implement and run the project.** Do not stop at a proposal, code skeleton, unexecuted notebook, or attractive but unsupported presentation. Every number, chart, hypothesis result, and model metric must come from executed code and the actual dataset.

## A. Assignment authority, scope, and the midterm restriction

### A1. Read these documents first

1. `ĐỀ BÀI TIỂU LUẬN CUỐI KỲ 1_NH 26-27.docx` — **primary authority** for the final project and its grading rubric.
2. `De KT giua ky_HK1_NH26-27.docx` — secondary reference, useful for checking earlier project expectations and the rule against dataset reuse. **Do not merge midterm-only requirements into the final assignment as though they were mandatory.**
3. This implementation plan — operational guidance, subordinate to the official final assignment.
4. Any existing project files, code, and user-provided decisions.

**Final assignment, mandatory:**
- Use **one real-world dataset throughout** the analysis, with at least **500 rows and 5 variables**.
- It must be **different from the dataset used for the midterm project**.
- Conduct exploratory data analysis, probability-distribution analysis, hypothesis tests, Pearson/Spearman correlation analysis, and multiple linear regression.
- Submit **Word + PDF reports, executable Python code, and presentation slides**.
- Record a **7–15-minute presentation video**, upload it to YouTube, and put the actual video link on **slide 2** after the title slide.
- The report must identify each group member's genuine contribution, percentage, and completion level; each member submits their own copy as instructed.
- Avoid plagiarism; cite the dataset, relevant methods, and any references actually used.

**Final grading weights (100 total):**

| Component | Weight | Full-credit evidence |
|---|---:|---|
| Exploratory analysis + visualization | 15 | Accurate descriptive statistics, missing/outlier analysis, meaningful plots, explanations |
| Probability distributions | 15 | At least two variables, appropriate distributions, histogram/KDE and diagnostics, interpretation |
| Hypothesis testing | 15 | Theory for t-test, chi-square and ANOVA; at least two valid research questions; sound execution and interpretation |
| Correlations | 15 | Pearson and Spearman theory, calculations, scatter/heatmap, practical interpretation |
| Multiple linear regression | 20 | Correct theory, a working multivariable linear regression, model evaluation, analysis and visuals |
| Python implementation | 20 | Executable, readable, complete and commented code with reproducible outputs |

**Midterm-only items (NOT a separate final-project rubric):** An interactive dashboard, six different chart types, a comparison of two prediction algorithms, and an explicit interpretability method were required in the midterm document. Some of these are worthwhile additions to the final project, but do not consume time on them at the expense of its published grading criteria. The proposed final-project baseline-vs-OLS comparison and several chart types are quality enhancements, not claims that the final assignment mandates them.

**Critical eligibility checkpoint:** The midterm document contains *suggested project topics and datasets*, not a record of which dataset the user actually selected. **Never infer from that list that Bike Sharing was or was not used in the midterm.** Record `MIDTERM_DATASET_NOT_CONFIRMED` until the actual prior dataset is established. If Bike Sharing was used in the midterm, do not submit it again; identify and agree on a replacement before publishing results. Otherwise, proceed with Bike Sharing and keep this verification prominently flagged for the user before submission.

**Administrative discrepancies:** The final handout shows a submission deadline of **October 13, 2026**, which is in the past. Request updated deadline confirmation rather than silently changing it. The handout's compressed-file naming example has an unusual `.docx` extension: check the actual submission portal/instructor directions and use a proper ZIP unless instructed otherwise. Do not invent student IDs, names, contribution percentages, or YouTube URLs.

### A2. The chosen dataset

**Default:** UCI Machine Learning Repository — *Bike Sharing*, `day.csv`.
- Official source: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
- DOI: https://doi.org/10.24432/C5W894
- Dataset source/credit: Hadi Fanaee-T, UCI Machine Learning Repository; preserve the current dataset license citation.
- Study context: real daily bike-rental counts from the Washington, D.C. Capital Bikeshare system, 2011–2012.
- `day.csv`: **731 observations, 16 columns**, including identifiers, dates, predictors, component counts, and the `cnt` target.
- The UCI catalog may show **17,389 observations for the combined collection**; this is not the row count of `day.csv`. The archive also contains `hour.csv`; do not mix units of observation or append the hourly file into daily analysis.
- **Response variable:** `cnt` — total rental counts per day.
- **Primary question:** How are daily bike-rental counts associated with season, temperature, humidity, wind, weather condition, and workday status? How well can a multiple linear regression estimate demand on an unseen future period?

**Data semantics that must be checked against the original README:** `season`, `weathersit`, `yr`, `workingday`, `holiday`, the normalization of `temp`, `atemp`, `hum`, `windspeed`, and definitions of `casual`, `registered`, `cnt`. Some third-party tutorials use conflicting season labels. **Use the authoritative dataset codebook and document the chosen mapping.**

### A3. Data-quality and scientific integrity non-negotiables

- Verify the original dataset rather than assuming the absence/presence of missingness, duplicates, outliers, or errors.
- UCI describes this dataset as not having missing values; **do not fabricate missing data simply to demonstrate imputation**.
- Never remove an extreme observation just to improve the model. Distinguish real unusual days from corrupted records.
- Never fabricate p-values, confidence intervals, R², visuals, external citations, or user participation.
- Do not infer causality from observational correlations or hypothesis tests.
- Explicitly acknowledge that daily observations are time-ordered and may violate independence assumptions in conventional tests.
- Separate exploratory inference from out-of-sample prediction. State limitations, not just statistically significant findings.

---

## B. Research design (decide before checking for significant results)

### B1. Central research question

**Proposed title:** *Statistical Analysis and Visualization of Daily Bike-Rental Demand: Weather, Seasonality, Hypothesis Testing, and Multiple Linear Regression*.

Build one coherent narrative spanning the six grading categories:

1. **Describe** typical and unusual daily demand.
2. **Characterize** probability distributions of demand and weather variables.
3. **Test** predeclared hypotheses about differences and associations.
4. **Quantify** Pearson and Spearman relationships.
5. **Explain and evaluate** a multivariable linear regression model.
6. **Translate** the findings into measured, appropriately qualified practical implications.

### B2. Three hypothesis tests (cover all named methods, even though the final assignment requires two research questions)

**H1 — Welch independent-samples t-test**
- Research question: Do working days (`workingday=1`) and nonworking days (`workingday=0`) have different mean daily rental counts (`cnt`)?
- H0: μ_workday = μ_nonworkday. H1: μ_workday ≠ μ_nonworkday (two-sided).
- Report group sizes, mean, SD, mean difference, 95% confidence interval, Welch t, approximate degrees of freedom, p-value, and effect size (Hedges' g or Cohen's d with clear definition).
- Use Welch rather than assuming equal variances by default. Include a figure comparing the groups.

**H2 — One-way ANOVA with appropriate robustness checks**
- Research question: Does mean `cnt` differ across the four seasons?
- H0: all four means are equal. H1: at least one differs.
- Examine sample sizes, group distributions, severe outliers, and equality of variances (e.g., Levene). Use ordinary ANOVA where assumptions are defensible; otherwise use Welch's ANOVA or a justified robustness check. Report F, df, p-value, practical effect size (η² or ω²), and valid post-hoc comparisons (Tukey or Games–Howell as appropriate).
- State the time-series dependence caveat; seasonal differences are observational and can be confounded by year and other conditions.

**H3 — Chi-square test of independence**
- Research question: Is the categorical weather condition (`weathersit`) associated with a *predefined* low/high daily-demand category?
- Define `high_demand` with a reproducible median-based threshold, document the threshold and the information loss from dichotomizing `cnt`. **This variable is only for this exploratory categorical test and must never enter the `cnt` regression predictors.**
- H0: weather category and demand category are statistically independent. H1: an association exists.
- Report contingency table, observed/expected cell counts, χ², df, p-value, Cramér's V, proportions, and the expected-count diagnostic. If categories are too sparse, apply a documented, scientifically sensible category combination, or use an appropriate exact/Monte Carlo alternative; do not silently ignore violated assumptions.
- Present this analysis as exploratory, because the target-derived classification and temporal dependence limit strong inferential claims.

**Statistical decision rules:** Preselect α = 0.05; show exact numeric p-values when available. Explain confidence intervals and both practical and statistical significance. If treating the three tests as a family, show Holm-adjusted p-values alongside unadjusted values. A non-significant result means insufficient evidence, **not proof of equality**. A significant p-value is **not** the probability that H0 is false.

### B3. Correlations

- Pearson: strength/direction of linear association; Spearman: strength/direction of rank-based monotonic association.
- Focus on meaningful numeric fields (`cnt`, `temp`, `atemp`, `hum`, `windspeed`), including `cnt`-to-weather pairwise relationships.
- Never interpret integer-coded `season`/`weathersit` as naturally continuous metrics.
- Use two separate labeled correlation heatmaps, scatter plots for selected relationships, effect-size interpretation, and caution about confounding and seasonality.
- Inspect collinearity such as `temp` vs `atemp` before fitting OLS.

### B4. Probability distributions

**Minimum two scientifically motivated variables:**
1. `cnt`: discrete nonnegative daily count; compare mean vs variance and evaluate whether a simple Poisson assumption is plausible. Pooled multi-season counts may be overdispersed; do **not** assert Poisson simply because the variable is a count. Also evaluate shape/normal approximation where defensible.
2. `temp`: bounded normalized temperature; examine histogram, KDE, Q-Q plot, skewness, kurtosis, and an approximate Normal candidate, explicitly noting boundedness and seasonal mixtures.

Optional third variable: `windspeed` or `hum` if it adds interpretive value and can be assessed with a defensible support/distribution family.

For each: describe domain, rationale, fitted distribution or candidate family, chart, quantitative diagnostic, and interpretation. If no candidate fits well, **report that transparently**. Use goodness-of-fit tests only with valid parameter-estimation assumptions (avoid a naive one-sample KS p-value after estimating the same distribution's parameters from the sample).

### B5. Multiple linear regression

**Primary task:** Fit and analyze a genuine **multiple linear regression** with `cnt` as response and more than one defensible predictor.

**Never include these in the predictor matrix:**
- `casual`, `registered` — because the dataset obeys **`cnt = casual + registered`**, yielding target leakage.
- `cnt` itself, target-derived `high_demand`, record ID `instant`.
- Future realized outcomes or fields unavailable at the stated prediction time.

**Possible predictors:** `temp`, `hum`, `windspeed`, `season` (categorical), `weathersit` (categorical), `workingday`, `yr`. Decide whether using `temp` *or* `atemp` better manages collinearity. Be careful with seasonal and monthly variables that encode overlapping information.

**Workflow:**
- Parse/sort by date and allocate approximately the first 80% of days to training, the last 20% to hold-out testing. **No shuffling.** Print exact date ranges.
- Fit all preprocessing (imputation only if genuinely needed, categorical encoding, scaling if any) **using training data only** via scikit-learn pipelines.
- Define `DummyRegressor(strategy='mean')` as a transparent baseline (optional but helpful) and an OLS linear regression as the main rubric model. Compare them on the same test period.
- Report train metrics and hold-out **MAE, RMSE, R²**; where appropriate provide adjusted R² with the correct sample/parameter context and an OLS coefficients table.
- Plot actual vs predicted, residual vs fitted, residual distribution/Q-Q, and prediction errors over time.
- Assess multicollinearity and other material linear-model limitations. If coefficients are interpreted inferentially, explain heteroskedasticity and serial correlation; use robust/HAC covariance where justified, not unexplained IID standard errors.
- Discuss predictor availability: the model can be interpreted as conditional on **observed weather** unless forecast-weather data are available. Do not market retrospective weather as a ready-to-deploy future forecasting system.
- Do not hide negative test R², replace OLS with a nonlinear model, or tune on the hold-out to obtain attractive results.
- A nonlinear model, if added, must be clearly supplemental and not a substitute for the required multiple linear regression.

---

## C. Required project structure and delivery artifacts

```text
bike-sharing-final-project/
├── README.md
├── requirements.txt                  # pinned, tested dependencies
├── .gitignore
├── PROGRESS.md                       # updated after every phase
├── FINAL_HANDOFF.md                  # honest pass/fail + user actions
├── docs/
│   ├── RUBRIC_TRACEABILITY.md
│   ├── DATA_DICTIONARY.md
│   ├── RESEARCH_DESIGN.md
│   ├── STATISTICAL_DECISIONS.md
│   ├── FIGURE_REGISTER.md
│   └── REFERENCES.md
├── data/raw/day.csv                  # unmodified official daily dataset
├── src/
│   ├── __init__.py
│   ├── load_validate.py
│   ├── descriptive_eda.py
│   ├── probability.py
│   ├── hypothesis_tests.py
│   ├── correlations.py
│   ├── regression.py
│   ├── visualizations.py
│   ├── artifact_generation.py
│   └── run_all.py
├── notebooks/analysis.ipynb          # executable, human-readable walkthrough
├── tests/
│   ├── test_data_integrity.py
│   ├── test_hypotheses.py
│   ├── test_no_leakage.py
│   ├── test_regression.py
│   └── test_output_contracts.py
├── outputs/
│   ├── figures/                      # high-resolution PNG/SVG where appropriate
│   ├── tables/                       # generated numerical tables
│   ├── model/                        # model metadata / diagnostics
│   └── results.json                  # machine-readable results source of truth
├── report/
│   ├── Final_Report.docx
│   └── Final_Report.pdf
├── presentation/
│   ├── Final_Presentation.pptx
│   └── SPEAKER_SCRIPT.md
└── submission/
    ├── SUBMISSION_CHECKLIST.md
    └── STUDENT_ID.zip                # placeholder until verified ID is known
```

**Reproducibility:** The following must work from a clean environment using the documented supported Python version:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m src.run_all
python -m pytest -q
```

Document platform-specific virtual-environment activation (Windows PowerShell, Linux/macOS). Require testable dependency pins, deterministic seeds when random operations are performed, clearly specified input path and generated output paths. **Do not type model statistics or hypothesis results manually into the report**: generate them from `outputs/results.json` and the same executed computation used for charts.

**Code quality:** Modest modular design, descriptive function names, docstrings and explanatory comments. Avoid needless web services, databases, microservices, deep learning, or large frameworks. If charts use categorical labels, explain definitions and units. Preserve raw data unchanged and record acquisition URL, date, codebook, and checksum.

---

## D. Sequential implementation phases and acceptance gates

### Phase 0 — Assignment and eligibility audit

**Implement:**
1. Read both assignment documents and existing repository contents; never overwrite uncommitted user changes.
2. Write `RUBRIC_TRACEABILITY.md` mapping each weighted rubric requirement to code, numerical table, figure(s), report chapter, and presentation slide.
3. Record what was *actually* used in the midterm, if available. If not, leave `MIDTERM_DATASET_NOT_CONFIRMED` visible; the suggestion list cannot settle this question.
4. Record administrative placeholders and deadline concerns.
5. Initialize `PROGRESS.md` with an audit trail.

**PASS:** Every final-assignment requirement has a planned piece of evidence; no fictional administrative data; the dataset reuse concern is either resolved or clearly documented for the user. Do not present dataset eligibility as confirmed without evidence.

### Phase 1 — Acquire, inspect, and validate the real dataset

**Implement:**
1. Download the official UCI archive or use the user-provided verified original. Extract only `day.csv` and README/codebook; register hash and citation.
2. Validate minimum 500 rows and 5 variables; verify 731 × 16 if using the standard unmodified file.
3. Inspect datatypes, date parsing, duplicates, missingness, categorical levels, illegal values, date gaps, and numeric ranges.
4. Assert `cnt == casual + registered` for **all rows**. Investigate any discrepancy rather than hiding it.
5. Produce source metadata, data dictionary, `dataset_audit.json`, and readable tables.
6. Explain why no imputation is needed if no missing values are found.

**PASS:** All data-integrity tests pass, the schema and meanings are documented, and the original CSV is unchanged.

### Phase 2 — Exploratory data analysis (15/100)

**Implement:**
1. Provide a dataset overview and full descriptive statistics for meaningful continuous variables: sample size, mean, median, standard deviation, min/max, quartiles and IQR.
2. Break down rental counts by year, season, weather category and working-day status, including group sizes.
3. Produce at least **five purposeful plot types** (minimum final requirement is three), for example:
   - Time series of daily rentals by date — trend, seasonality, unusual days.
   - Histogram of `cnt` with KDE — distribution shape.
   - Boxplots of `cnt` by season — median, spread, potential outliers.
   - Scatter plot of `temp` vs `cnt` — continuous relationship.
   - Bar chart of group means, ideally with appropriate uncertainty markers — group comparisons.
4. Analyze potential outliers using IQR fences, robust statistics or defensible z-scores. Distinguish unusual valid days from data errors. Compare sensitivity if exclusions are defensible, but keep legitimate extremes by default.
5. For each figure provide title, axis labels, units, appropriate legend, a written justification of plot type and at least 1–2 factual interpretation sentences.

**PASS:** Reproducible statistics, missing/duplicate decisions, outlier discussion, 3+ different suitable chart types and evidence-based insights.

### Phase 3 — Probability-distribution analysis (15/100)

**Implement:**
1. Analyze at least `cnt` and `temp` with separate rationale and distribution diagnostics.
2. Produce properly scaled histogram + KDE, plus Q-Q or other distribution-appropriate diagnostic visual for each.
3. Consider Poisson for the count variable **only with an overdispersion check**; consider plausible approximate Normal behavior for bounded normalized temperature while explaining its limitations.
4. Quantify mean/variance, skewness and other valid shape indicators. Use distribution-testing procedures with justified assumptions and note sensitivity to sample size and time dependence.
5. Explain *what* the distribution tells us about demand/weather and what conclusion is not supported.

**PASS:** At least two researched distributions, visuals and numbers, scientifically defensible comments, no false assertion that data must match a familiar distribution.

### Phase 4 — Hypothesis-testing analysis (15/100)

**Implement:**
1. Give concise, dataset-relevant theory for **t-tests, chi-square tests and ANOVA**: purpose, input variables, H0/H1, assumptions and basic test logic.
2. Execute **all three predeclared tests** in Section B2, not just one or two.
3. Report n, test statistic, applicable degrees of freedom, p-value, confidence intervals when appropriate, effect size, assumption checks, and interpretive figure.
4. Apply robust versions or documented alternatives when assumptions are materially violated.
5. Discuss multiple testing, time dependence, observational limitations and practical significance.

**PASS:** Three valid executed tests, at least two explicit research questions, complete interpretation, correct limitations and no misstatement of p-values.

### Phase 5 — Pearson and Spearman correlations (15/100)

**Implement:**
1. Write short formulas/definitions and a contrast between linear correlation and rank-based monotonic correlation.
2. Compute both **Pearson and Spearman** matrices using scientifically meaningful numeric variables, with p-values for key tested pairs where appropriate.
3. Create two separately labeled heatmaps and meaningful scatter plots for the strongest/relevant relationships.
4. Discuss magnitude and sign, nonlinearity, seasonality, collinearity, spurious relationships and practical relevance. Never claim causality.

**PASS:** Both coefficients correctly computed/explained, legible visuals, and clear interpretation rather than a screenshot of a correlation matrix.

### Phase 6 — Multiple linear regression (20/100)

**Implement:**
1. Present the OLS multiple regression equation, interpretation of coefficients and assumptions, R²/adjusted R² and appropriate prediction metrics.
2. Register a strict predictor allowlist; assert exclusion of `cnt`, `casual`, `registered`, `instant`, target-derived features, and any future data.
3. Split chronologically, report exact date ranges and justify the time-aware split.
4. Fit the model using a train-only preprocessing pipeline, handling categorical predictors with proper one-hot encoding.
5. Fit a mean-only baseline for context and multiple linear regression as the mandatory principal model; evaluate both on the **same untouched test period**.
6. Report MAE, RMSE and R², interpreted in daily rental units; provide OLS coefficient estimates and appropriate intervals/caveats.
7. Create actual-versus-predicted, residual-versus-fitted, residual distribution/Q-Q, and temporal error plots. Check multicollinearity and meaningful residual patterns.
8. Explain at least 3–5 model associations and operational limitations, including whether actual or forecast weather is assumed known.

**PASS:** Correct multiple linear model, genuine hold-out evaluation, no leakage, diagnostic interpretation, actual results, and no unsupported prediction/causation claims.

### Phase 7 — Produce the academic Word/PDF report

Write the deliverable **in English**, with coherent prose rather than a raw notebook dump. Recommended structure:

1. Cover page (real group/student details or prominently labeled placeholders).
2. Abstract and keywords.
3. Introduction, motivation and research questions.
4. Dataset provenance, schema, ethical/citation context, preparation and data-quality decisions.
5. EDA and visualization with described methods, figures, descriptive tables and interpretation.
6. Probability distributions (two variables minimum) with theory, fitted candidates, diagnostics and conclusions.
7. Hypothesis testing: t-test, chi-square, ANOVA theory, method, results, confidence intervals/effect sizes, limitations.
8. Correlations: Pearson/Spearman theory, plots, numeric analysis and practical insight.
9. Multiple linear regression: model specification, leakage avoidance, split, OLS coefficients, performance, diagnostics and limitations.
10. Discussion, practical implications, limitations and future work.
11. Conclusion.
12. References, contribution table (real members only), and appendices with execution instructions.

**Design requirements:** consistent heading hierarchy and citations, proper table/figure captions and sources, page numbers, readable equations, labeled units, no unsupported results, no clipped charts/tables, and no blank or broken final pages. Any claim involving a number must match the executed machine-readable results. Generate both **`Final_Report.docx` and `Final_Report.pdf`**, and **render and visually inspect every page** before delivery. If conversion is impossible, report the precise blocker instead of claiming completion.

**PASS:** Every required statistical section is substantive, the report agrees with code outputs, both files open successfully, and layout QA is documented.

### Phase 8 — Produce slides, video script and submission bundle

**Implement:**
1. Create approximately 12–15 clean, academically styled slides, with narrative, varying visual compositions and charts from the actual analysis.
2. **Slide 1:** project title. **Slide 2:** genuine public/unlisted YouTube video link, or **clearly marked `PENDING_USER_VIDEO_URL`** if video does not exist. No fictional URL.
3. Suggested content: problem/data; EDA; distribution diagnostics; t-test; ANOVA; chi-square; correlation; model design; performance; residual diagnostics; conclusions and limitations; contribution/references.
4. Create `SPEAKER_SCRIPT.md` for a sensible **7–15-minute presentation**, ideally around 9–11 minutes. Do not claim an estimated reading time is an actual recorded-video duration.
5. Build the final ZIP with source code, required dependencies, dataset (subject to license/citation), reports, presentation and relevant reproducibility materials. Use the true naming convention after student ID and portal rules have been confirmed.
6. Test that the ZIP opens; ensure files are not missing, accidentally empty, or only linked to a local machine path.
7. Generate `FINAL_HANDOFF.md` and `SUBMISSION_CHECKLIST.md` with outstanding human actions: recording/uploading video, inserting YouTube link, personal details, actual midterm dataset verification, deadline/portal checks.

**PASS:** All AI-producible files genuinely exist, open correctly and agree. User-dependent requirements are reported as **NEEDS_USER**, never PASS by assumption.

---

## E. Automated verification and final scoring audit

At minimum, automate these checks:

- `test_dataset_minimum_dimensions`: rows >= 500 and columns >= 5.
- `test_data_dictionary_matches_csv`: required columns, legal categories, parseable dates, reasonable ranges.
- `test_target_invariant`: every `cnt` equals `casual + registered`.
- `test_raw_data_unchanged`: the file checksum matches the registered original after all runs.
- `test_duplicate_and_missing_decisions`: the audit is reproducible and no fake cleaning is introduced.
- `test_statistical_output_validity`: finite statistics/valid p-value bounds; valid groups; expected-frequency check for chi-square; explicit effect size.
- `test_correlation_tables`: both Pearson and Spearman output exists with explicit variable labels.
- `test_regression_feature_allowlist`: no `cnt`, `casual`, `registered`, `instant`, `high_demand`, or target-derived features in X.
- `test_chronological_split`: `max(train_date) < min(test_date)`; test data are never used to fit preprocessing.
- `test_metric_consistency`: reported prediction metrics equal a fresh calculation from saved y_true/y_pred.
- `test_baseline_same_test`: baseline and OLS use identical untouched holdout rows.
- `test_required_plots`: all required figures exist, are nonempty, and match the registered captions/units.
- `test_report_numeric_consistency`: report metrics and p-values are populated from the same results source.
- `test_reproducibility`: an independent rerun produces consistent tables/figures within documented tolerance.
- `test_submission_archive`: ZIP opens and contains expected artifacts.

**Final audit table to produce in `FINAL_HANDOFF.md`:**

| Rubric item | Weight | Code location | Numerical evidence | Figure(s) | Report section | Result |
|---|---:|---|---|---|---|---|
| EDA | 15 | ... | ... | ... | ... | PASS/FAIL |
| Probability | 15 | ... | ... | ... | ... | PASS/FAIL |
| Hypothesis tests | 15 | ... | ... | ... | ... | PASS/FAIL |
| Correlation | 15 | ... | ... | ... | ... | PASS/FAIL |
| Multiple linear regression | 20 | ... | ... | ... | ... | PASS/FAIL |
| Python quality | 20 | ... | ... | ... | ... | PASS/FAIL |

**A green test suite does not prove an A grade.** After technical tests, perform a separate *scientific review* (assumptions, leakage, credible conclusions, appropriate methods, no cherry-picking) and a *presentation review* (chart legibility, captions, numerical consistency, layout, and citation integrity).

---

## F. Agent execution protocol (mandatory)

1. **Implement, execute, inspect, repair.** Do not claim success after only writing code or generating files.
2. **Work phase by phase, saving state.** After every phase update `PROGRESS.md` with completed tasks, changed files, executed commands, observed output, remaining issues, and exact next action. Commit by phase when a Git repository exists and commits are appropriate.
3. **Reuse existing valid work.** Before modifying files, inspect the repository and protect unrelated or uncommitted changes.
4. **Do not invent missing observations, identities, significance, scores, sources or recorded video.** All scientific quantities must be computed.
5. **Ask only for blockers that materially change academic validity**, such as confirmation that the selected dataset was already used midterm. Continue other safe implementation tasks while the answer is unresolved, and flag the final eligibility gate.
6. **Never let impressive presentation camouflage incorrect statistics.** Verify assumptions, cleaning choices, variable definitions, valid comparisons and predictive leakage.
7. **English everywhere** unless the official instructor subsequently requires Vietnamese. Keep Vietnamese filenames intact as references to the original assignments.
8. **Prefer simple, inspectable Python** over unnecessary abstractions or infrastructure. Maintain code comments and tests.
9. **References are evidence, not source code to plagiarize.** Cite UCI and any external papers/tutorials/code actually used. Original analysis and original wording are mandatory.
10. **At the end, make an honest handoff:** actual artifacts, actual test output, actual unresolved issues, and user-dependent completion checklist.

### Resume behavior after interruption

On restart, read `PROGRESS.md` and `FINAL_HANDOFF.md` if present; inspect existing output and test status; **resume from the first incomplete or failed phase**, not from a new speculative rewrite. Re-run affected tests and regenerate dependent artifacts when upstream computations change. Never copy stale numbers into reports/slides.

---

## G. Agent launch prompt (copy/paste)

> Implement the attached English master plan `BIKE_SHARING_100_SCORE_AGENT_PLAN_EN.md` for the final Data Analysis and Visualization project.
>
> Read the original final-project assignment and the midterm assignment. Treat the final document as authoritative. The midterm file contains *suggested* datasets; it does not establish which dataset was used. Track this unresolved dataset-reuse check explicitly.
>
> Default to the UCI Bike Sharing `day.csv` dataset. Use English for all code comments, documentation, Word/PDF report, figures, slides, and speaker script. Execute **all phases 0–8**, including real calculations, statistical assumptions and diagnostics, real artifact generation, reproducibility tests, and a requirement-by-requirement grading audit.
>
> Update `PROGRESS.md` after **every completed phase**. Resume from it if interrupted. Do not stop after planning or scaffolding. Make justified implementation decisions yourself; request clarification only for actual academic-validity blockers.
>
> No fabricated findings, no target leakage, no copying other projects' analyses, and no claim of 100/100 before grading. Do not claim that a video was recorded or uploaded. Put the actual YouTube link on slide 2 when the user provides one; otherwise retain a prominent placeholder and mark the submission incomplete.
>
> Start by auditing the two assignment documents and repository files, then implement Phase 1, run the tests, and progress sequentially to final handoff.

---

## H. Source references to record and verify

- UCI Bike Sharing dataset: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
- Dataset DOI: https://doi.org/10.24432/C5W894
- Original dataset README/codebook within the downloaded UCI archive.
- Official instructor's **final-project document** (primary grading authority).
- Official instructor's **midterm document** (secondary context, including illustrative topics).
- External tutorials, sample repos, or statistical references **only if actually consulted**, with precise attribution. Never copy their results without independently running the analysis on the chosen input.

**End state:** A genuinely reproducible project, complete in its AI-producible components, with the strongest evidence reasonably possible for **every criterion in the published 100-point rubric**, and an explicit checklist for tasks only the student can complete.
