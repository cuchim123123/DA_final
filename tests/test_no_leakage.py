"""
Automated Anti-Leakage & Chronological Split Verification Suite (Phase 6).

Enforces strict exclusion of `cnt`, `casual`, `registered`, `instant`, `dteday`,
and target-derived `high_demand` from regression predictors, and verifies
strict chronological ordering (`max(train_date) < min(test_date)`).
"""

import pytest
from src.load_validate import load_and_validate_data
from src.regression import (
    FORBIDDEN_LEAKAGE_FEATURES,
    PRIMARY_PREDICTOR_ALLOWLIST,
    build_preprocessing_transformer,
    chronological_train_test_split,
    validate_feature_allowlist,
)


def test_regression_feature_allowlist() -> None:
    """Verify no target, component, index, or target-derived features enter X."""
    validate_feature_allowlist(PRIMARY_PREDICTOR_ALLOWLIST)

    for forbidden in ["cnt", "casual", "registered", "instant", "dteday", "high_demand"]:
        assert forbidden not in PRIMARY_PREDICTOR_ALLOWLIST
        with pytest.raises(ValueError, match="CRITICAL LEAKAGE DETECTED"):
            validate_feature_allowlist(PRIMARY_PREDICTOR_ALLOWLIST + [forbidden])

    df, _ = load_and_validate_data(save_outputs=False)
    train_df, _ = chronological_train_test_split(df)
    pre = build_preprocessing_transformer()
    pre.fit(train_df[PRIMARY_PREDICTOR_ALLOWLIST])
    out_names = list(pre.get_feature_names_out())

    for out_col in out_names:
        for forbidden in ["cnt", "casual", "registered", "instant", "high_demand"]:
            assert forbidden not in out_col


def test_chronological_split() -> None:
    """Verify strict chronological 80/20 split without shuffling or date overlap."""
    df, _ = load_and_validate_data(save_outputs=False)
    train_df, test_df = chronological_train_test_split(df, train_fraction=0.80)

    assert len(train_df) == 584
    assert len(test_df) == 147
    assert len(train_df) + len(test_df) == 731

    assert train_df["dteday_parsed"].is_monotonic_increasing
    assert test_df["dteday_parsed"].is_monotonic_increasing
    assert train_df["dteday_parsed"].max() < test_df["dteday_parsed"].min()
    assert str(train_df["dteday"].iloc[0]) == "2011-01-01"
    assert str(train_df["dteday"].iloc[-1]) == "2012-08-06"
    assert str(test_df["dteday"].iloc[0]) == "2012-08-07"
    assert str(test_df["dteday"].iloc[-1]) == "2012-12-31"
