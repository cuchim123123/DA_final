"""Descriptive and diagnostic analytical modules and visualization generators."""

from telco_churn.analysis.charts import (
    apply_publication_style,
    generate_descriptive_diagnostic_charts,
)
from telco_churn.analysis.descriptive import (
    add_derived_analysis_columns,
    compute_compound_segments,
    compute_descriptive_analytics,
    compute_subgroup_rates,
    wilson_ci_pct,
)
from telco_churn.analysis.diagnostic import compute_diagnostic_analytics

__all__ = [
    "add_derived_analysis_columns",
    "apply_publication_style",
    "compute_compound_segments",
    "compute_descriptive_analytics",
    "compute_diagnostic_analytics",
    "compute_subgroup_rates",
    "generate_descriptive_diagnostic_charts",
    "wilson_ci_pct",
]
