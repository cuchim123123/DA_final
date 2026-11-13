"""Executable Walkthrough Notebook Generator (`notebooks/analysis.ipynb`)."""

from __future__ import annotations

from pathlib import Path
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook
from nbclient import NotebookClient

from src.load_validate import PROJECT_ROOT

NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "analysis.ipynb"


def build_and_execute_notebook(execute: bool = True) -> Path:
    """Create and optionally execute `notebooks/analysis.ipynb`."""
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook()

    nb["cells"] = [
        new_markdown_cell(
            "# Statistical Analysis and Visualization of Daily Bike-Rental Demand\n"
            "**Dataset:** UCI Bike Sharing Dataset (`data/raw/day.csv`, DOI: `10.24432/C5W894`)"
        ),
        new_code_cell(
            "import sys\nfrom pathlib import Path\nimport pandas as pd\nfrom IPython.display import display\n\n"
            "PROJECT_ROOT = Path.cwd().resolve()\n"
            "if PROJECT_ROOT.name == 'notebooks':\n    PROJECT_ROOT = PROJECT_ROOT.parent\n"
            "if str(PROJECT_ROOT) not in sys.path:\n    sys.path.insert(0, str(PROJECT_ROOT))\n\n"
            "from src.load_validate import load_and_validate_data\n"
            "from src.descriptive_eda import run_exploratory_data_analysis\n"
            "from src.probability import run_probability_analysis\n"
            "from src.hypothesis_tests import run_all_hypothesis_tests\n"
            "from src.correlations import run_correlation_analysis\n"
            "from src.regression import run_regression_analysis"
        ),
        new_markdown_cell("## Phase 1: Dataset Provenance & Validation"),
        new_code_cell(
            "df, audit = load_and_validate_data(save_outputs=False)\n"
            "print('Dimensions:', audit['dimensions'], '| SHA-256 Verified:', audit['provenance']['day_csv_checksum_verified'])\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/data_dictionary_summary.csv'))"
        ),
        new_markdown_cell("## Phase 2: Exploratory Data Analysis (EDA) & Outlier Audit"),
        new_code_cell(
            "eda_res = run_exploratory_data_analysis(df, save_outputs=False)\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/eda_continuous_summary.csv'))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/eda_group_by_season.csv'))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/eda_outlier_audit.csv'))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/eda_outlier_handling_sensitivity.csv'))"
        ),
        new_markdown_cell("## Phase 3: Probability Distribution Analysis"),
        new_code_cell(
            "prob_res = run_probability_analysis(df, save_outputs=False)\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/probability_distribution_summary.csv'))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/cnt_overdispersion_and_fit.csv'))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/temp_distribution_diagnostics.csv'))"
        ),
        new_markdown_cell("## Phase 4: Hypothesis Testing (H1 t-Test, H2 ANOVA, H3 Chi-Square)"),
        new_code_cell(
            "ht_res = run_all_hypothesis_tests(df, save_outputs=False)\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/hypothesis_tests_summary.csv'))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/h1_ttest_workingday.csv'))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/h2_anova_season_posthoc.csv'))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/h3_chisq_contingency_table.csv'))"
        ),
        new_markdown_cell("## Phase 5: Pearson & Spearman Correlation Analysis"),
        new_code_cell(
            "corr_res = run_correlation_analysis(df, save_outputs=False)\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/pearson_correlation_matrix.csv', index_col=0))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/spearman_correlation_matrix.csv', index_col=0))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/correlation_pairwise_tests.csv'))"
        ),
        new_markdown_cell("## Phase 6: Multiple Linear Regression (OLS) & Diagnostics"),
        new_code_cell(
            "reg_res = run_regression_analysis(df, save_outputs=False)\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/regression_model_comparison.csv'))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/regression_vif_diagnostics.csv'))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/regression_ols_coefficients.csv'))\n"
            "display(pd.read_csv(PROJECT_ROOT / 'outputs/tables/regression_residual_diagnostics.csv'))"
        ),
    ]
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.14"},
    }

    if execute:
        NotebookClient(nb, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(PROJECT_ROOT)}}).execute()
    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    return NOTEBOOK_PATH
