"""Prescriptive analytics: risk tiers, capacity targeting lift, scenario simulation, and traceable recommendations."""

from telco_churn.recommendations.prescriptive import (
    build_capacity_lift_table,
    build_risk_tiers,
    compute_prescriptive_analytics,
    simulate_retention_scenario,
)

__all__ = [
    "build_capacity_lift_table",
    "build_risk_tiers",
    "compute_prescriptive_analytics",
    "simulate_retention_scenario",
]
