# Telco Churn Midterm: Independent Project Specification and Implementation Plan

## 1. Objective and non-goals

Develop an **original Python analytical application** for the IBM Telco Customer Churn sample. The dashboard should help a user explore churn prevalence, identify associated characteristics, evaluate a predictive risk model, and plan a defensible retention prioritization strategy.

A good project has a single coherent narrative: **observed problem -> associated patterns -> predictive capability -> qualified action recommendation**. It is not a gallery of unrelated plots or a model score without business interpretation.

Not in scope: generating the Word report, PowerPoint, videos, deploying a production CRM integration, inventing intervention outcomes, collecting live customer data, complex cloud infrastructure. The local app must work reliably.

## 2. Data policy and validation

Use the **IBM-hosted original CSV**, not a modified file or a committed derivative from the inspiration repo. Record its URL and retrieval date, and verify a file checksum after acquisition. Inspect the actual schema and label distribution; do not silently rely on prior figures.

Important data specifics to audit rather than assume:

- `customerID` is an identifier, not a predictive signal. Avoid printing individual IDs in screenshots or report exhibits without a clear need.
- `Churn` is a binary label. Verify categorical values and missing/invalid target rows.
- `TotalCharges` is frequently read as a string due to blank entries. Handle its parsing and missingness explicitly, with a documented justification for the chosen treatment.
- Validate uniqueness, category domains, ranges, contradictory service combinations and accidental duplicates; avoid deleting rows automatically without auditing consequences.
- Use user-visible, neutral wording for groups, especially demographic variables. Note limitations of simplified synthetic case data and any demographic-performance differences if examined.
- Avoid claiming a genuine temporal trend when the dataset lacks suitable observation timestamps. `tenure` is duration, not a date series.

Separate original data, derived analysis tables, model-ready features and final evaluation. Do not use test data for fitting preprocessing parameters, feature-selection thresholds, model selection, hyperparameter tuning or calibration.

## 3. Four connected analytical workstreams

### 3.1 Descriptive analytics: what is observed?

Produce a data audit, churn rate, distributions of tenure, charges, contract, services and payment methods, segment counts, and uncertainty/denominators where important. Show both group volumes and rates to avoid misleading comparisons. Highlight limitations of the fictional sample.

### 3.2 Diagnostic analytics: what is associated with churn?

Investigate associations between churn and selected contract, tenure, service, payment and pricing variables. Provide suitable group comparisons, statistical tests or effect-size estimates where meaningful. Discuss confounding and correlated features. The word 'driver' must be used carefully: observational associations are not verified causes. Distinguish statistical significance from practical importance.

### 3.3 Predictive analytics: how reliably can churn risk be estimated?

At a minimum:

- Use a simple and credible baseline (e.g., properly specified Logistic Regression or DummyClassifier as a reference) and a genuinely different advanced algorithm (e.g., Random Forest, HistGradientBoosting, or XGBoost). Prefer at least **two trained predictive algorithms**, not counting a no-skill dummy as the only baseline algorithm.
- Build identical, justified training and evaluation protocols for fair comparison. Missing-value imputation and encoders belong inside scikit-learn Pipelines/ColumnTransformers and must fit only on training folds.
- Explain **stratified random** train/test splitting if chosen, since the IBM dataset has no reliable calendar observation sequence. Avoid inventing chronological splits. State test proportion, seed and target-class proportions, and justify design.
- Keep a fixed, held-out test set untouched until model and threshold selections are finalized using training/validation or cross-validation.
- Evaluate beyond accuracy: confusion matrix, precision, recall, F1, ROC-AUC and preferably PR-AUC. Report class distribution and interpretation of false negatives versus false positives.
- Select and explain threshold on validation data if adjusting it. Evaluate calibrated probabilities when the product shows churn likelihood. Do not claim good calibration without calibration assessment.
- Provide at least one meaningful interpretability technique: coefficients with correct preprocessing interpretation, permutation importance, or SHAP if feasible. Explain limitations and ensure displayed feature values are correctly mapped to encoded columns.
- Save reproducible model and preprocessing pipeline or equivalent evaluation artifacts; make dashboard scoring consistent with evaluated feature transformations.
- If the dataset is an illustrative snapshot with 'churn in last month' status, frame model predictions as **retrospective benchmark/classification** or possible risk-ranking demonstration, not evidence of prospective deployment accuracy.

### 3.4 Prescriptive analytics: what actions follow from the evidence?

Design a *decision-support* section in the dashboard with proposed risk groups and optional capacity/cost scenarios. Recommendations must use **specific real numbers** from descriptive, diagnostic and predictive results, with links to exact evidence files. Recommendations should distinguish:

1. **What is observed:** segment size, rate and magnitude in the sample.
2. **What the model estimates:** predictive risk, reliability and uncertainty.
3. **What is an assumption:** intervention cost, retention effect, customer value, outreach capacity, expected uptake.

The dataset does **not** provide causal treatment effects or proof that any intervention reduces churn. Do not present illustrative ROI or saved customers as measured facts. Any business simulation must label assumptions and show sensitivity to them; if unavailable, keep recommendations qualitative but anchored in quantified, verified risk and segment evidence.

## 4. Interactive dashboard deliverable

Implement **at least one working Streamlit dashboard** with a clear user journey. Recommended sections/views:

- **Overview:** KPI cards, class balance, customer composition, navigation and dataset caveats.
- **Explore & Diagnose:** interactive subgroup filters, six distinct plot types across project, subgroup denominators and evidence-backed explanations.
- **Model Performance & Explainability:** test-only comparisons, confusion matrices, ROC/PR plots, feature explanations, explicit model version and cutoff.
- **Retention Prioritization:** risk tiers/capacity scenarios and justified recommendations; optionally a single-customer hypothetical scoring form clearly marked as an educational demonstration.

The precise page count and layout are design choices. Prefer legible charts and explainable interactions over cosmetic animations. Every filter should change the displayed data correctly. Never recompute a model on every UI interaction. Avoid showing a training metric as test performance. A customer score must use the exact fitted preprocessing and model pipeline.

### Minimum six genuine chart types

Select chart types justified by data and story; provide **at least six genuinely different forms**, for example:

1. Grouped or ordinary **bar chart**: churn rates by contract type, with counts and confidence/context.
2. **Histogram**: tenure or charges distribution, perhaps overlaying churn groups.
3. **Boxplot**: distribution of monthly charges by churn outcome.
4. **Violin plot**: tenure distribution by outcome or contract type, used only if it adds insight beyond boxplots.
5. **Scatter plot**: tenure versus monthly charges with readable opacity/aggregation.
6. **Heatmap**: appropriately computed association strengths, subgroup rates, or held-out confusion matrix.
7. **Line/curve plot** (additional): ROC and/or precision-recall curves on held-out test data.

These examples are not a quota of arbitrary images. A stacked bar is still a bar, and a different color of the same chart is not a new chart type. Each exported figure must have a meaningful title, labeled axes (where meaningful), a legend for multiple groups and one or two verifiable interpretation sentences. Include the chart-type inventory in evidence outputs. A cross-sectional dataset should not have fake chronological line charts.

## 5. Engineering quality standards

Build a **clean-room implementation** based on the assignment and IBM dataset. The inspiration repo may be inspected for ideas or UX patterns, but must not become a dependency or the codebase to submit. Never copy its source, pre-trained models, dashboards, metrics, CSV derivatives, screenshots or narrative.

Maintain a clear separation between data ingestion/validation, exploration, feature preprocessing, model training/evaluation, recommendation logic, artifact generation, and dashboard presentation. Use a lightweight `src/` package or equivalent; avoid a 1,000-line Streamlit file or monolithic notebook that mixes all responsibilities.

Quality expectations:

- Readable functions, meaningful module boundaries, type hints where useful and comments explaining non-obvious statistical decisions rather than every trivial statement.
- Single authoritative dataset schema and model-feature contract; avoid magic numbers and hardcoded output statistics.
- Deterministic seeds, environment/dependency definition, portable project-relative paths, and a single documented end-to-end reproduction command. No absolute developer-local paths.
- Model preprocessing identical at training and scoring; data and evaluation artifacts versioned and traceable.
- No leakage from target, holdout, aggregate prevalence, fitting preprocessors on full data, or future information. Validate feature semantics before training.
- Fail explicitly on invalid schema, non-running dashboard or missing artifacts; do not silently substitute fake results.
- Automated tests for schema, data quality, preprocessing, split isolation, feature mapping, model evaluation consistency, dashboard-critical helpers and evidence-manifest completeness.
- Prefer `pytest`, `ruff` and standard Python tooling. Docker or CI may be added only if they materially improve reproducibility. Do not add infrastructure for its own sake.
- README with setup, commands, dataset citation and accurate limitations.

### Suggested structure, not a strict prescription

```
telco-churn-analytics/
  README.md
  pyproject.toml
  data/raw/
  src/telco_churn/
    data/
    analysis/
    modeling/
    recommendations/
    reporting/
  app/
  tests/
  outputs/
  docs/
    PROGRESS.md
    DECISIONS.md
    REQUIREMENTS_TRACEABILITY.md
  report_evidence_package/
  report_evidence_package.zip
```

Use a simpler or different structure if it better separates responsibilities. Never introduce layers merely for appearance.

## 6. Phased execution plan and quality gates

### Phase 0: Audit requirements and plan (no coding yet)

Read the original midterm assignment and this pack. Review the reference repository *only as inspiration*. Inspect the IBM dataset and current workspace. Create the requirement traceability matrix and an independent architecture/analysis plan. Explicitly flag source limitations, non-cloning rules and key decisions. Ask the student only if a material decision would change scope or invalidate the assignment.

**Gate:** Every mandatory item has an intended implementing module, output and verification method.

### Phase 1: Data source and integrity

Acquire the IBM original file; record URL/date/checksum; validate schema/types/duplicates/missingness/domain constraints; document cleaning decisions and data limitations.

**Gate:** Deterministic data load and data-quality tests pass, with no silent row removal.

### Phase 2: Descriptive and diagnostic layers

Compute descriptive tables and subgroup comparisons; generate defensible figures and interpretations from computed values. Produce at least six distinct chart types across the complete analysis, tracking type and intention.

**Gate:** Every chart has source data, valid metadata and checked one-to-two-sentence findings. Diagnostics do not claim causation.

### Phase 3: Predictive layer

Implement baseline and advanced classifier; justify split; cross-validate/tune on training only; select model/threshold with appropriate metrics; evaluate once on held-out test; explain model.

**Gate:** Re-run from clean artifacts, prove leakage safety and comparable evaluation, persist test metrics and full preprocessing/scoring pipeline.

### Phase 4: Prescriptive layer

Generate concrete recommendations that cite computed facts from the previous three layers; use calibrated risk estimates or clearly qualify uncalibrated scores. Create a scenario tool only with explicitly user-provided or labeled assumed parameters.

**Gate:** No claimed intervention efficacy without evidence. All numeric recommendations trace to tables and exact calculations.

### Phase 5: Streamlit dashboard

Build the interactive analytics interface, connect all views to results and preprocessing artifacts, test filters and scoring, improve usability and verify representative workflows locally.

**Gate:** Application starts from a clean setup, no missing assets/errors, dashboard interactions change results and still match source artifacts.

### Phase 6: Full quality and assignment audit

Run tests/lint/reproduction, inspect every generated plot and summary, compare actual artifacts to requirements, correct discrepancies and document limitations. Revisit the original instructor document rather than trusting a prior checklist.

**Gate:** Zero missing mandatory requirements and no invented claims. Document unresolved issues honestly.

### Phase 7: Report-evidence package and transfer

Create and validate `report_evidence_package/` and `report_evidence_package.zip` exactly as described in `03_REPORT_EVIDENCE_EXPORT_SPEC.md`. The package is for a different assistant that will write the midterm report.

**Gate:** An uninformed reviewer can trace every statement, number and chart to a portable file inside the ZIP, without accessing the coding workspace.

## 7. Progress and autonomous operation

After each phase, update `docs/PROGRESS.md` with what was completed, commands executed, tests/results, issues and next actions. Update the requirement matrix with evidence paths. Fix discovered problems as you go, but do not assume that all planned features are necessary: scope follows the instructor's requirements and analytic usefulness. Work through implementation rather than stopping at scaffolding; when unable to access the dataset or perform a key step, state precisely what is blocked.

## 8. Acceptance criteria

The project is accepted only if it produces a **runnable Python application**, a reproducible independent analysis, **at least six distinct chart types**, **at least two trained model algorithms**, documented split and explainability, **evidence-backed recommendations** and a working interactive dashboard, **plus a complete verified ZIP evidence package**.

Nothing in the reference repository's README, including its model numbers, should appear as a claimed result unless the new implementation independently regenerates and verifies that number.
