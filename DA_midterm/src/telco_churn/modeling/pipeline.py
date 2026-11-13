"""Training-only scikit-learn preprocessing pipelines matching raw feature schema."""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from telco_churn.config import BINARY_INT_FEATURES, CATEGORICAL_FEATURES, NUMERIC_FEATURES


def build_preprocessor(scale_numeric: bool = True, drop_first: bool = False) -> ColumnTransformer:
    """Construct a leak-free ColumnTransformer operating strictly on raw predictor columns."""
    num_steps: list[tuple[str, object]] = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        num_steps.append(("scaler", StandardScaler()))

    ohe_kwargs: dict[str, object] = {
        "handle_unknown": "ignore",
        "sparse_output": False,
    }
    if drop_first:
        ohe_kwargs["drop"] = "first"

    return ColumnTransformer(
        transformers=[
            ("num", Pipeline(num_steps), NUMERIC_FEATURES),
            ("bin", SimpleImputer(strategy="most_frequent"), BINARY_INT_FEATURES),
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("ohe", OneHotEncoder(**ohe_kwargs)),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
    )
