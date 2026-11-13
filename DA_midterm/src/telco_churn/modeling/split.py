"""Stratified random train/test partitioning with strict ID/target isolation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from telco_churn.config import (
    ID_COL,
    POSITIVE_LABEL,
    RANDOM_STATE,
    RAW_PREDICTORS,
    TABLES_DIR,
    TARGET_COL,
    TEST_SIZE,
)


@dataclass(frozen=True)
class DatasetSplit:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    ids_train: pd.Series
    ids_test: pd.Series
    summary_df: pd.DataFrame


def make_stratified_split(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
    tables_dir: Path = TABLES_DIR,
    save_table: bool = True,
) -> DatasetSplit:
    """Partition data via stratified random split without chronological leakage."""
    y_all = (df[TARGET_COL] == POSITIVE_LABEL).astype(int)

    train_idx, test_idx = train_test_split(
        df.index,
        test_size=test_size,
        random_state=random_state,
        stratify=y_all,
    )

    train_df = df.loc[train_idx].copy()
    test_df = df.loc[test_idx].copy()

    ids_train = train_df[ID_COL].reset_index(drop=True)
    ids_test = test_df[ID_COL].reset_index(drop=True)
    overlap = set(ids_train).intersection(set(ids_test))
    if overlap:
        raise AssertionError(f"Train/test split leakage: {len(overlap)} overlapping IDs")

    X_train = train_df[RAW_PREDICTORS].reset_index(drop=True)
    X_test = test_df[RAW_PREDICTORS].reset_index(drop=True)
    y_train = (train_df[TARGET_COL] == POSITIVE_LABEL).astype(int).reset_index(drop=True)
    y_test = (test_df[TARGET_COL] == POSITIVE_LABEL).astype(int).reset_index(drop=True)

    summary_rows = []
    for name, y_vec in [("Full Dataset", y_all), ("Train (5-Fold CV Dev)", y_train), ("Hold-Out Test (Sealed)", y_test)]:
        n = len(y_vec)
        n_pos = int(y_vec.sum())
        summary_rows.append(
            {
                "partition": name,
                "n_rows": n,
                "pct_of_total": round(n / len(df) * 100.0, 2),
                "churn_yes_count": n_pos,
                "churn_no_count": n - n_pos,
                "churn_rate_pct": round(n_pos / n * 100.0, 4),
                "random_state": random_state,
                "split_strategy": "Stratified Random (Cross-Sectional Snapshot)",
            }
        )
    summary_df = pd.DataFrame(summary_rows)

    if save_table:
        tables_dir.mkdir(parents=True, exist_ok=True)
        summary_df.to_csv(tables_dir / "split_class_balance.csv", index=False)

    return DatasetSplit(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        ids_train=ids_train,
        ids_test=ids_test,
        summary_df=summary_df,
    )
