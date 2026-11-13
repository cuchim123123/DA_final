"""Single-pass held-out test evaluation, ROC/PR/calibration curves, and confusion matrix plots."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.calibration import calibration_curve
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

from telco_churn.analysis.charts import apply_publication_style
from telco_churn.analysis.descriptive import add_derived_analysis_columns
from telco_churn.config import FIGURES_DIR, TABLES_DIR
from telco_churn.modeling.split import DatasetSplit
from telco_churn.modeling.train import TrainingBundle, compute_ece


def _eval_threshold_row(
    model_name: str,
    role: str,
    threshold_label: str,
    threshold: float,
    y_true: np.ndarray,
    y_prob: np.ndarray,
) -> dict[str, Any]:
    y_pred = (y_prob >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    return {
        "model_name": model_name,
        "role": role,
        "threshold_setting": threshold_label,
        "threshold_value": round(float(threshold), 4),
        "n_test": int(len(y_true)),
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "specificity": round(float(spec), 4),
        "f1_score": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_true, y_prob)), 4),
        "pr_auc": round(float(average_precision_score(y_true, y_prob)), 4),
        "brier_score": round(float(brier_score_loss(y_true, y_prob)), 4),
        "calibration_ece": round(compute_ece(y_true, y_prob), 4),
        "log_loss": round(float(log_loss(y_true, np.clip(y_prob, 1e-6, 1 - 1e-6))), 4),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def evaluate_and_plot_models(
    split: DatasetSplit,
    bundle: TrainingBundle,
    tables_dir: Path = TABLES_DIR,
    figures_dir: Path = FIGURES_DIR,
    save_outputs: bool = True,
) -> dict[str, Any]:
    """Evaluate all fitted models once on the untouched hold-out test set and generate plots."""
    apply_publication_style()
    X_te = split.X_test
    y_te = split.y_test.to_numpy()
    tau_opt = bundle.optimal_threshold

    test_probs: dict[str, np.ndarray] = {}
    rows: list[dict[str, Any]] = []

    role_map = dict(zip(bundle.cv_summary_df["model_name"], bundle.cv_summary_df["role"], strict=True))
    cv_tau_map = dict(
        zip(bundle.cv_summary_df["model_name"], bundle.cv_summary_df["val_optimal_threshold"], strict=True)
    )
    for name, model in bundle.fitted_models.items():
        probs = model.predict_proba(X_te)[:, 1]
        test_probs[name] = probs
        role = role_map.get(name, "Candidate Model")
        rows.append(_eval_threshold_row(name, role, "Default (0.50)", 0.50, y_te, probs))
        if name != "Dummy Floor (Most Frequent)":
            model_tau = float(cv_tau_map[name])
            rows.append(
                _eval_threshold_row(
                    name,
                    role,
                    f"Model CV F1-Opt ({model_tau:.3f})",
                    model_tau,
                    y_te,
                    probs,
                )
            )

    test_df = pd.DataFrame(rows)

    # Anonymized hold-out prediction table for metric auditing and prescriptive tiering
    te_enriched = add_derived_analysis_columns(
        X_te.assign(customerID=[f"TEST_{i:04d}" for i in range(1, len(X_te) + 1)], Churn="No")
    )
    champ_prob = test_probs[bundle.champion_name]
    base_prob = test_probs[bundle.baseline_name]

    pred_df = pd.DataFrame(
        {
            "test_obs_id": te_enriched["customerID"],
            "y_true": y_te,
            "prob_champion": np.round(champ_prob, 6),
            "prob_logistic_baseline": np.round(base_prob, 6),
            "prob_random_forest": np.round(test_probs["Random Forest"], 6),
            "prob_hist_gradient_boosting": np.round(test_probs["HistGradientBoosting"], 6),
            "pred_champion_default_050": (champ_prob >= 0.50).astype(int),
            "pred_champion_val_opt": (champ_prob >= tau_opt).astype(int),
            "Contract": te_enriched["Contract"],
            "tenure": te_enriched["tenure"],
            "tenure_tier": te_enriched["tenure_tier"],
            "InternetService": te_enriched["InternetService"],
            "PaymentMethod": te_enriched["PaymentMethod"],
            "MonthlyCharges": te_enriched["MonthlyCharges"],
        }
    )

    if save_outputs:
        tables_dir.mkdir(parents=True, exist_ok=True)
        figures_dir.mkdir(parents=True, exist_ok=True)
        test_df.to_csv(tables_dir / "model_test_comparison.csv", index=False)
        pred_df.to_csv(tables_dir / "test_predictions.csv", index=False)

    # ------------------------------------------------------------------
    # Fig 07: ROC Curve, Precision-Recall Curve, and Calibration Curve
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.9))
    plot_specs = [
        ("Logistic Regression", "#2B5B84", "--"),
        ("Random Forest", "#1B9E77", "-."),
        ("HistGradientBoosting", "#D95F02", "-"),
    ]
    if bundle.champion_name not in {p[0] for p in plot_specs}:
        plot_specs.append((bundle.champion_name, "#7570B3", ":"))

    # Panel 1: ROC Curves
    for m_name, color, ls in plot_specs:
        probs = test_probs[m_name]
        fpr, tpr, _ = roc_curve(y_te, probs)
        auc_val = roc_auc_score(y_te, probs)
        axes[0].plot(fpr, tpr, color=color, linestyle=ls, linewidth=2.0, label=f"{m_name} (AUC={auc_val:.4f})")
    axes[0].plot([0, 1], [0, 1], color="#777777", linestyle=":", linewidth=1.2, label="Random Chance (0.5000)")
    axes[0].set_title("Held-Out Test ROC Curves")
    axes[0].set_xlabel("False Positive Rate (1 - Specificity)")
    axes[0].set_ylabel("True Positive Rate (Recall)")
    axes[0].legend(loc="lower right", frameon=True, fontsize=8.3)

    # Panel 2: Precision-Recall Curves
    pos_prev = float(y_te.mean())
    for m_name, color, ls in plot_specs:
        probs = test_probs[m_name]
        prec, rec, _ = precision_recall_curve(y_te, probs)
        ap_val = average_precision_score(y_te, probs)
        axes[1].plot(rec, prec, color=color, linestyle=ls, linewidth=2.0, label=f"{m_name} (PR-AUC={ap_val:.4f})")
    axes[1].axhline(pos_prev, color="#777777", linestyle=":", linewidth=1.2, label=f"No-Skill Prevalence ({pos_prev:.3f})")
    axes[1].set_title("Held-Out Test Precision-Recall Curves")
    axes[1].set_xlabel("Recall (Churn Sensitivity)")
    axes[1].set_ylabel("Precision (Positive Predictive Value)")
    axes[1].set_ylim(0, 1.05)
    axes[1].legend(loc="lower left", frameon=True, fontsize=8.3)

    # Panel 3: Probability Calibration Curves
    for m_name, color, ls in plot_specs:
        probs = test_probs[m_name]
        prob_true, prob_pred = calibration_curve(y_te, probs, n_bins=10, strategy="quantile")
        brier = brier_score_loss(y_te, probs)
        axes[2].plot(prob_pred, prob_true, marker="o", markersize=5, color=color, linestyle=ls, linewidth=1.8, label=f"{m_name} (Brier={brier:.4f})")
    axes[2].plot([0, 1], [0, 1], color="#777777", linestyle=":", linewidth=1.2, label="Perfect Calibration")
    axes[2].set_title("Test Calibration Reliability Curves")
    axes[2].set_xlabel("Mean Predicted Churn Probability")
    axes[2].set_ylabel("Observed Churn Fraction")
    axes[2].legend(loc="upper left", frameon=True, fontsize=8.3)

    fig.suptitle("Held-Out Test Discrimination and Calibration Benchmarks (n = 1,409)", fontsize=13.5, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(figures_dir / "fig07_model_roc_pr_calibration_curves.png", bbox_inches="tight")
    plt.close(fig)

    # ------------------------------------------------------------------
    # Fig 08: Confusion Matrix Heatmaps (Default 0.50 & Val-Opt Thresholds)
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.4))
    cm_specs = [
        ("Logistic Regression", 0.50, "Logistic Regression\n(Cutoff = 0.50)"),
        (bundle.champion_name, 0.50, f"{bundle.champion_name}\n(Default Cutoff = 0.50)"),
        (bundle.champion_name, tau_opt, f"{bundle.champion_name}\n(Val F1-Opt Cutoff = {tau_opt:.2f})"),
    ]
    for ax, (m_name, cutoff, title_txt) in zip(axes, cm_specs, strict=True):
        probs = test_probs[m_name]
        cm = confusion_matrix(y_te, (probs >= cutoff).astype(int), labels=[0, 1])
        cm_pct = cm / cm.sum() * 100.0
        labels = np.array(
            [
                [f"TN = {cm[0,0]}\n({cm_pct[0,0]:.1f}%)", f"FP = {cm[0,1]}\n({cm_pct[0,1]:.1f}%)"],
                [f"FN = {cm[1,0]}\n({cm_pct[1,0]:.1f}%)", f"TP = {cm[1,1]}\n({cm_pct[1,1]:.1f}%)"],
            ]
        )
        sns.heatmap(
            cm,
            annot=labels,
            fmt="",
            cmap="Blues",
            cbar=False,
            linewidths=0.8,
            xticklabels=["Pred: No", "Pred: Yes"],
            yticklabels=["Actual: No", "Actual: Yes"],
            ax=ax,
        )
        f1_val = f1_score(y_te, (probs >= cutoff).astype(int))
        rec_val = recall_score(y_te, (probs >= cutoff).astype(int))
        prec_val = precision_score(y_te, (probs >= cutoff).astype(int))
        ax.set_title(f"{title_txt}\nPrec={prec_val:.3f} | Rec={rec_val:.3f} | F1={f1_val:.3f}")

    fig.suptitle("Held-Out Test Confusion Matrices Across Cutoff Regimes (n = 1,409; Churn = 374)", fontsize=13.5, fontweight="bold", y=1.05)
    fig.tight_layout()
    fig.savefig(figures_dir / "fig08_confusion_matrices_heatmap.png", bbox_inches="tight")
    plt.close(fig)

    # Chart metadata for inventory
    champ_05 = test_df[(test_df["model_name"] == bundle.champion_name) & (test_df["threshold_setting"] == "Default (0.50)")].iloc[0]
    champ_opt = test_df[(test_df["model_name"] == bundle.champion_name) & (test_df["threshold_setting"] != "Default (0.50)")].iloc[0]
    lr_05 = test_df[(test_df["model_name"] == "Logistic Regression") & (test_df["threshold_setting"] == "Default (0.50)")].iloc[0]

    chart_registry = [
        {
            "figure_id": "fig07",
            "relative_path": "03_predictive/figures/fig07_model_roc_pr_calibration_curves.png",
            "chart_type": "Multi-panel Curve Plot (ROC, Precision-Recall, Calibration)",
            "section": "Predictive",
            "variables": "Predicted churn probabilities vs actual Churn (Test set n=1,409)",
            "title": "Held-Out Test Discrimination and Calibration Benchmarks (n = 1,409)",
            "axis_labels": "ROC: FPR vs TPR; PR: Recall vs Precision; Calibration: Mean Pred Prob vs Observed Fraction",
            "legend_applicable": "Yes (Models + Reference diagonal / prevalence line)",
            "interpretation_1": (
                f"On the untouched hold-out test set (n=1,409), Logistic Regression achieves ROC-AUC={lr_05['roc_auc']:.4f} "
                f"(PR-AUC={lr_05['pr_auc']:.4f}) compared with {champ_05['roc_auc']:.4f} (PR-AUC={champ_05['pr_auc']:.4f}) "
                f"for {bundle.champion_name}."
            ),
            "interpretation_2": (
                f"Calibration curves track near the diagonal (champion Brier={champ_05['brier_score']:.4f}, "
                f"ECE={champ_05['calibration_ece']:.4f}), indicating well-calibrated probabilities for tier ranking."
            ),
            "source_table": "03_predictive/tables/model_test_comparison.csv",
        },
        {
            "figure_id": "fig08",
            "relative_path": "03_predictive/figures/fig08_confusion_matrices_heatmap.png",
            "chart_type": "Confusion Matrix Heatmap",
            "section": "Predictive",
            "variables": "Actual Churn vs Predicted Churn across thresholds",
            "title": "Held-Out Test Confusion Matrices Across Cutoff Regimes (n = 1,409; Churn = 374)",
            "axis_labels": "X: Predicted Class; Y: Actual Class",
            "legend_applicable": "No (Annotated cell counts and percentages)",
            "interpretation_1": (
                f"At default 0.50 cutoff, {bundle.champion_name} catches {int(champ_05['tp'])} of 374 test churners "
                f"(Recall={champ_05['recall']:.3f}, FN={int(champ_05['fn'])}, Precision={champ_05['precision']:.3f})."
            ),
            "interpretation_2": (
                f"Lowering the cutoff to the validation-tuned threshold tau={tau_opt:.2f} raises test Recall to "
                f"{champ_opt['recall']:.3f} ({int(champ_opt['tp'])}/374 churners detected, F1={champ_opt['f1_score']:.3f}) "
                f"at the expense of {int(champ_opt['fp'])} false positives."
            ),
            "source_table": "03_predictive/tables/model_test_comparison.csv",
        },
    ]

    return {
        "test_comparison_table": test_df.to_dict(orient="records"),
        "chart_registry": chart_registry,
    }
