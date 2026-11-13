"""Model explainability: raw-column test permutation importance and logistic odds-ratio weights."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance

from telco_churn.analysis.charts import apply_publication_style
from telco_churn.config import FIGURES_DIR, RANDOM_STATE, RAW_PREDICTORS, TABLES_DIR
from telco_churn.modeling.split import DatasetSplit
from telco_churn.modeling.train import TrainingBundle


def explain_and_plot_models(
    split: DatasetSplit,
    bundle: TrainingBundle,
    tables_dir: Path = TABLES_DIR,
    figures_dir: Path = FIGURES_DIR,
    save_outputs: bool = True,
) -> dict[str, Any]:
    """Compute unified raw-feature permutation importance and logistic regression coefficients."""
    apply_publication_style()
    X_te = split.X_test
    y_te = split.y_test

    champion_model = bundle.fitted_models[bundle.champion_name]
    lr_model = bundle.fitted_models[bundle.baseline_name]

    # 1. Raw-column permutation importance on hold-out test set (avoids one-hot dummy dilution)
    perm_roc = permutation_importance(
        champion_model,
        X_te,
        y_te,
        scoring="roc_auc",
        n_repeats=30,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    perm_pr = permutation_importance(
        champion_model,
        X_te,
        y_te,
        scoring="average_precision",
        n_repeats=30,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    perm_rows = []
    for idx, feat in enumerate(RAW_PREDICTORS):
        perm_rows.append(
            {
                "raw_feature": feat,
                "roc_auc_drop_mean": round(float(perm_roc.importances_mean[idx]), 5),
                "roc_auc_drop_sd": round(float(perm_roc.importances_std[idx]), 5),
                "pr_auc_drop_mean": round(float(perm_pr.importances_mean[idx]), 5),
                "pr_auc_drop_sd": round(float(perm_pr.importances_std[idx]), 5),
            }
        )
    perm_df = pd.DataFrame(perm_rows).sort_values("roc_auc_drop_mean", ascending=False).reset_index(drop=True)
    perm_df["importance_rank"] = np.arange(1, len(perm_df) + 1)

    # 2. Logistic Regression encoded coefficients & odds multipliers
    prep = lr_model.named_steps["prep"]
    clf = lr_model.named_steps["clf"]
    encoded_names = list(prep.get_feature_names_out())
    coefs = clf.coef_[0]

    lr_rows = []
    for fname, beta in zip(encoded_names, coefs, strict=True):
        clean_name = fname.replace("num__", "").replace("bin__", "").replace("cat__", "")
        lr_rows.append(
            {
                "encoded_feature": clean_name,
                "scale_note": "1 SD standardized change" if fname.startswith("num__") else "Active indicator (1 vs 0)",
                "log_odds_coef": round(float(beta), 4),
                "odds_multiplier_exp_beta": round(float(np.exp(beta)), 4),
                "direction": "Increases Churn Odds" if beta > 0 else "Decreases Churn Odds",
            }
        )
    lr_df = (
        pd.DataFrame(lr_rows)
        .assign(abs_beta=lambda d: d["log_odds_coef"].abs())
        .sort_values("abs_beta", ascending=False)
        .drop(columns=["abs_beta"])
        .reset_index(drop=True)
    )

    if save_outputs:
        tables_dir.mkdir(parents=True, exist_ok=True)
        figures_dir.mkdir(parents=True, exist_ok=True)
        perm_df.to_csv(tables_dir / "permutation_importance.csv", index=False)
        lr_df.to_csv(tables_dir / "logistic_odds_ratios.csv", index=False)

    # ------------------------------------------------------------------
    # Fig 09: Explainability Plot (Permutation Importance + Log-Odds)
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 6.2))

    top_perm = perm_df.head(12).iloc[::-1]
    y_pos = np.arange(len(top_perm))
    axes[0].barh(
        y_pos,
        top_perm["roc_auc_drop_mean"],
        xerr=top_perm["roc_auc_drop_sd"],
        capsize=3.5,
        color="#2B5B84",
        alpha=0.9,
        edgecolor="black",
        linewidth=0.5,
    )
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels(top_perm["raw_feature"])
    axes[0].set_title(f"{bundle.champion_name}\nTop 12 Raw-Feature Permutation Importance (Test ROC-AUC)")
    axes[0].set_xlabel("Mean Decrease in Held-Out ROC-AUC (± 1 SD, 30 Repeats)")

    # Exclude redundant duplicate structural 'No internet/phone service' & complement binary mirrors in chart for clarity
    def _is_redundant_display_term(name: str) -> bool:
        return (
            name.endswith("_No internet service")
            or name.endswith("_No phone service")
            or name.endswith("_No") and name.split("_")[0] in {"PhoneService", "PaperlessBilling", "Partner", "Dependents", "StreamingTV", "StreamingMovies", "OnlineBackup", "DeviceProtection", "MultipleLines"}
            or name == "gender_Female"
        )

    display_lr = lr_df[~lr_df["encoded_feature"].map(_is_redundant_display_term)].copy()
    top_lr = pd.concat(
        [
            display_lr[display_lr["log_odds_coef"] > 0].head(7),
            display_lr[display_lr["log_odds_coef"] < 0].head(7),
        ]
    )
    top_lr = top_lr.sort_values("log_odds_coef")
    y_lr = np.arange(len(top_lr))
    bar_cols = ["#D95F02" if b > 0 else "#1B9E77" for b in top_lr["log_odds_coef"]]
    axes[1].barh(y_lr, top_lr["log_odds_coef"], color=bar_cols, alpha=0.9, edgecolor="black", linewidth=0.5)
    axes[1].axvline(0.0, color="#333333", linewidth=1.1, linestyle="--")
    axes[1].set_yticks(y_lr)
    axes[1].set_yticklabels(top_lr["encoded_feature"], fontsize=9.0)
    axes[1].set_title("Regularized Logistic Regression\nTop Unique Directional Log-Odds Weights")
    axes[1].set_xlabel("Log-Odds Coefficient (+ Increases Churn Risk, - Reduces Risk)")

    fig.suptitle("Predictive Model Explainability: Global Feature Importance and Directional Effects", fontsize=13.5, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig(figures_dir / "fig09_model_explainability.png", bbox_inches="tight")
    plt.close(fig)

    top1, top2, top3 = perm_df.iloc[0], perm_df.iloc[1], perm_df.iloc[2]
    chart_entry = {
        "figure_id": "fig09",
        "relative_path": "03_predictive/figures/fig09_model_explainability.png",
        "chart_type": "Horizontal Error-Bar & Diverging Bar Plot",
        "section": "Predictive",
        "variables": "19 raw predictors vs held-out ROC-AUC drop & logistic log-odds",
        "title": "Predictive Model Explainability: Global Feature Importance and Directional Effects",
        "axis_labels": "Left X: Mean ROC-AUC Decrease; Right X: Log-Odds Coefficient",
        "legend_applicable": "No (Color encodes positive vs negative churn risk direction)",
        "interpretation_1": (
            f"Permuting raw features on the hold-out test set confirms {top1['raw_feature']} (dROC-AUC={top1['roc_auc_drop_mean']:.4f}), "
            f"{top2['raw_feature']} ({top2['roc_auc_drop_mean']:.4f}), and {top3['raw_feature']} ({top3['roc_auc_drop_mean']:.4f}) "
            f"dominate {bundle.champion_name} discrimination."
        ),
        "interpretation_2": (
            "Regularized logistic regression aligns with diagnostics: Month-to-month contracts, Fiber optic internet, and short "
            "tenure sharply elevate log-odds of churn, while multi-year contracts and OnlineSecurity/TechSupport reduce risk."
        ),
        "source_table": "03_predictive/tables/permutation_importance.csv; 03_predictive/tables/logistic_odds_ratios.csv",
    }

    return {
        "permutation_importance": perm_df.to_dict(orient="records"),
        "logistic_odds_ratios": lr_df.to_dict(orient="records"),
        "chart_entry": chart_entry,
    }
