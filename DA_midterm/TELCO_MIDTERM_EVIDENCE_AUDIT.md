# Telco Churn Midterm Evidence Audit

**Review basis:** `report_evidence_package(1).zip`, original midterm requirements provided in `De KT giua ky_HK1_NH26-27(1).docx`, and independent recalculation using the exported held-out predictions. Review date: 2026-11-10.

## Overall assessment

The package is sufficient to begin the nine-section academic report and presentation. It contains 58 readable files: four analytical layers, 10 figures, four dashboard screenshots, source and data-quality documentation, model comparison tables, observations, assumptions, references, and a requirements coverage map. ZIP integrity checks succeeded. This audit does not independently validate the Python source code or reproduce every dataset-level statistic because the raw CSV and source project are not included in this evidence ZIP.

## Compliance with midterm technical requirements

| Requirement | Evidence | Assessment |
|---|---|---|
| Descriptive analysis | Churn KPIs, 17 subgroup summaries, three figures | Covered |
| Diagnostic analysis | Chi-square/Cramér's V, group comparisons, confounding audit, three figures | Covered |
| Predictive analysis | Dummy, Logistic Regression, Random Forest, HistGradientBoosting, train/test and CV files | Covered |
| Prescriptive analysis | Four recommendations, top-capacity lift, scenarios | Covered; clarify two targeting definitions |
| At least six different chart types | Grouped bars, histogram/KDE, boxplot, violin, density scatter, heatmap, model curves, confusion matrices, coefficient plots, cumulative gains | Covered |
| Interactive dashboard | Four screenshots plus interaction documentation and a reported AppTest | Adequately evidenced; live behavior not independently tested |
| At least two models | Logistic Regression, Random Forest, HistGradientBoosting plus dummy | Covered |
| Train/test strategy | Stratified 80/20 split, 5-fold CV, no claimed time field | Covered |
| Explainability | Permutation importance and regression coefficients | Covered |
| Numeric recommendations | Four evidence-linked proposals and sensitivity tables | Covered, with noted corrections |
| Report, slides, executable source | Export prepared, but report/slides not yet created; code is outside this ZIP | Pending by design |

## Independent numerical checks

- Test set: 1,409 records, with 374 churn and 1,035 non-churn observations.
- Recalculated from `03_predictive/tables/test_predictions.csv`:
  - Logistic Regression: ROC-AUC 0.8412, PR-AUC 0.6286.
  - Random Forest: ROC-AUC 0.8440, PR-AUC 0.6513, Brier 0.1361.
  - HistGradientBoosting: ROC-AUC 0.8461, PR-AUC 0.6610.
  - Random Forest at threshold 0.33: TP 279, FP 220, FN 95, TN 815; precision 0.5591, recall 0.7460, F1 0.6392.
- Risk tiers reproduced: high-risk 275/185 churn, elevated-risk 224/94, low-risk 910/95.
- Capacity-based capture reproduced: top 30% (423 test accounts) contained 246 of 374 churners, capture 65.78%, lift 2.19x.
- Every subgroup partition in `descriptive_subgroups.csv` sums to 7,043 customers, 1,869 churners, and $139,130.85 in monthly charges associated with churned records.
- All 10 analytical figures and four dashboard screenshots are present and readable.

## Corrections recommended before report drafting

1. **REC-2 group size mismatch.** `REC-2` calls its target `Fiber optic subscribers without OnlineSecurity or TechSupport` but reports `n=3,096`, which is the count of all fiber-optic customers, not the subset meeting the additional conditions. Either change the target to `Fiber-optic subscribers, prioritizing those without OnlineSecurity or TechSupport` and explicitly describe 3,096 as the broad segment, or compute and report the actual intersected subgroup count and its churn statistics. Do not imply 3,096 is the narrowed cohort.
2. **REC-4 conflates a capacity cutoff and a probability cutoff.** Top 30% capacity means 423 of 1,409 test records, with minimum probability approximately 0.3918. The selected probability threshold 0.33 flags 499 of 1,409 test records, or about 35.4%. These represent different policies and should be clearly separated. The `2,113` full-sample figure is a 30% capacity illustration, not proof that 2,113 full-sample customers were ranked and evaluated.
3. **HistGradientBoosting validation threshold inconsistency.** `model_cv_comparison.csv` lists validation threshold 0.340, whereas `model_test_comparison.csv` describes its tuned threshold as 0.33. The latter test results reproduce the 0.33 threshold, so the selection/reporting process needs clarification and a single consistent chosen threshold for this model.
4. **Revenue language.** `$139,130.85/month` represents the sum of monthly charges for records labeled as already churned. It is a historical billing-based exposure proxy, not measured future lost revenue or revenue preserved by an intervention. Scenario financial projections are assumption-based, not demonstrated treatment lift.
5. **Dataset limitations.** IBM's Telco sample represents a fictional cross-sectional telecommunications company. Avoid causal claims, live deployment claims, or prospective retention-effect guarantees.

## Further data requirements

**No additional Python output is necessary to write the report** if the REC-2 label is corrected to distinguish the broad fiber-optic cohort from the narrower priority group. If a precise numerical estimate for the combined `Fiber optic AND (no OnlineSecurity OR no TechSupport)` segment is desired, the coding agent should export that additional group breakdown. That is an optional improvement, not a core rubric gap.

## Appropriate next steps

Have the coding agent fix the documented inconsistencies and, if feasible, regenerate the evidence ZIP. Then prepare the nine report sections and slides from the evidence. Use results as measured outcomes of this fictional snapshot, clearly distinguishing observed numbers from simulated retention interventions.
