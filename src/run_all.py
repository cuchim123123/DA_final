"""Master End-to-End Execution Pipeline (`python -m src.run_all`)."""

from __future__ import annotations

import json
import time
from typing import Any, Dict

from src.artifact_generation import build_and_execute_notebook
from src.correlations import run_correlation_analysis
from src.descriptive_eda import run_exploratory_data_analysis
from src.hypothesis_tests import run_all_hypothesis_tests
from src.load_validate import OUTPUTS_DIR, load_and_validate_data
from src.probability import run_probability_analysis
from src.regression import run_regression_analysis
from src.visualizations import generate_all_visualizations


def run_all_pipeline(build_notebook: bool = True) -> Dict[str, Any]:
    """Execute the complete statistical and visualization pipeline (Phases 1–6)."""
    t0 = time.perf_counter()
    df, audit = load_and_validate_data(save_outputs=True)
    eda_res = run_exploratory_data_analysis(df=df, save_outputs=True)
    prob_res = run_probability_analysis(df=df, save_outputs=True)
    ht_res = run_all_hypothesis_tests(df=df, save_outputs=True)
    corr_res = run_correlation_analysis(df=df, save_outputs=True)
    reg_res = run_regression_analysis(df=df, save_outputs=True)
    figures_meta = generate_all_visualizations(
        df=df, prob_res=prob_res, ht_res=ht_res, corr_res=corr_res, reg_res=reg_res
    )

    payload: Dict[str, Any] = {
        "dataset_audit": audit,
        "eda": eda_res,
        "probability": prob_res,
        "hypothesis_tests": ht_res,
        "correlations": corr_res,
        "regression": reg_res,
        "figures": figures_meta,
    }
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUTS_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    if build_notebook:
        build_and_execute_notebook(execute=True)

    print(f"Pipeline completed in {time.perf_counter() - t0:.2f}s | {len(figures_meta)} figures saved.")
    return payload


if __name__ == "__main__":
    run_all_pipeline(build_notebook=True)
