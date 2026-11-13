"""Authoritative paths, dataset schema, and shared configuration constants."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
DATA_DIR: Path = PROJECT_ROOT / "data"
DATA_RAW_DIR: Path = DATA_DIR / "raw"
RAW_CSV_PATH: Path = DATA_RAW_DIR / "Telco-Customer-Churn.csv"
PROVENANCE_PATH: Path = DATA_RAW_DIR / "provenance.json"

OUTPUTS_DIR: Path = PROJECT_ROOT / "outputs"
TABLES_DIR: Path = OUTPUTS_DIR / "tables"
FIGURES_DIR: Path = OUTPUTS_DIR / "figures"
MODELS_DIR: Path = OUTPUTS_DIR / "models"
SCREENSHOTS_DIR: Path = OUTPUTS_DIR / "dashboard_screenshots"
DATASET_OVERVIEW_PATH: Path = OUTPUTS_DIR / "dataset_overview.json"
RESULTS_SUMMARY_PATH: Path = OUTPUTS_DIR / "results_summary.json"

DOCS_DIR: Path = PROJECT_ROOT / "docs"
REPORT_PACKAGE_DIR: Path = PROJECT_ROOT / "report_evidence_package"
REPORT_PACKAGE_ZIP: Path = PROJECT_ROOT / "report_evidence_package.zip"

IBM_DATASET_URL: str = (
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
)
IBM_REPO_URL: str = "https://github.com/IBM/telco-customer-churn-on-icp4d"
INSPIRATION_REPO_URL: str = "https://github.com/UtkarshRai-ds/telco-churn-prediction"

DATASET_CAVEAT: str = (
    "IBM identifies this CSV as sample data for a fictional telecommunications company "
    "(cross-sectional snapshot of 7,043 subscribers). Associations and model scores do not "
    "establish causality or verified live commercial revenue impacts."
)

RANDOM_STATE: int = 42
TEST_SIZE: float = 0.20
N_CV_FOLDS: int = 5

ID_COL: str = "customerID"
TARGET_COL: str = "Churn"
POSITIVE_LABEL: str = "Yes"
NEGATIVE_LABEL: str = "No"

NUMERIC_FEATURES: list[str] = ["tenure", "MonthlyCharges", "TotalCharges"]
BINARY_INT_FEATURES: list[str] = ["SeniorCitizen"]
CATEGORICAL_FEATURES: list[str] = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]
RAW_PREDICTORS: list[str] = NUMERIC_FEATURES + BINARY_INT_FEATURES + CATEGORICAL_FEATURES
FORBIDDEN_FEATURE_COLS: set[str] = {ID_COL, TARGET_COL}

PHONE_DEPENDENT_COL: str = "MultipleLines"
INTERNET_DEPENDENT_COLS: list[str] = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]


@dataclass(frozen=True)
class ColumnSpec:
    name: str
    raw_dtype: str
    scale: str
    role: str
    allowed_values: tuple[str, ...] | None
    description: str


SCHEMA_SPECS: tuple[ColumnSpec, ...] = (
    ColumnSpec("customerID", "string", "Identifier", "id", None, "Unique fictional subscriber ID; excluded from modeling."),
    ColumnSpec("gender", "string", "Nominal binary", "predictor", ("Female", "Male"), "Subscriber gender label."),
    ColumnSpec("SeniorCitizen", "int64", "Binary indicator", "predictor", ("0", "1"), "Whether subscriber is a senior citizen (1) or not (0)."),
    ColumnSpec("Partner", "string", "Nominal binary", "predictor", ("No", "Yes"), "Whether subscriber has a partner."),
    ColumnSpec("Dependents", "string", "Nominal binary", "predictor", ("No", "Yes"), "Whether subscriber has dependents."),
    ColumnSpec("tenure", "int64", "Discrete duration (months)", "predictor", None, "Number of months subscriber has stayed with the company (0 to 72)."),
    ColumnSpec("PhoneService", "string", "Nominal binary", "predictor", ("No", "Yes"), "Whether subscriber has telephone service."),
    ColumnSpec("MultipleLines", "string", "Nominal categorical", "predictor", ("No", "Yes", "No phone service"), "Multiple telephone lines status."),
    ColumnSpec("InternetService", "string", "Nominal categorical", "predictor", ("DSL", "Fiber optic", "No"), "Customer internet service provider type."),
    ColumnSpec("OnlineSecurity", "string", "Nominal categorical", "predictor", ("No", "Yes", "No internet service"), "Online security add-on."),
    ColumnSpec("OnlineBackup", "string", "Nominal categorical", "predictor", ("No", "Yes", "No internet service"), "Online backup add-on."),
    ColumnSpec("DeviceProtection", "string", "Nominal categorical", "predictor", ("No", "Yes", "No internet service"), "Device protection add-on."),
    ColumnSpec("TechSupport", "string", "Nominal categorical", "predictor", ("No", "Yes", "No internet service"), "Technical support add-on."),
    ColumnSpec("StreamingTV", "string", "Nominal categorical", "predictor", ("No", "Yes", "No internet service"), "Streaming TV add-on."),
    ColumnSpec("StreamingMovies", "string", "Nominal categorical", "predictor", ("No", "Yes", "No internet service"), "Streaming movies add-on."),
    ColumnSpec("Contract", "string", "Ordinal categorical", "predictor", ("Month-to-month", "One year", "Two year"), "Subscriber contract term."),
    ColumnSpec("PaperlessBilling", "string", "Nominal binary", "predictor", ("No", "Yes"), "Whether subscriber uses paperless billing."),
    ColumnSpec("PaymentMethod", "string", "Nominal categorical", "predictor", ("Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"), "Subscriber payment method."),
    ColumnSpec("MonthlyCharges", "float64", "Continuous ratio (USD/month)", "predictor", None, "Monthly bill amount charged to subscriber."),
    ColumnSpec("TotalCharges", "string->float64", "Continuous ratio (USD cumulative)", "predictor", None, "Cumulative charges; stored as string in raw CSV due to 11 whitespace entries at tenure=0."),
    ColumnSpec("Churn", "string", "Binary target", "target", ("No", "Yes"), "Whether customer churned within the last month (Yes = 1, No = 0)."),
)

EXPECTED_COLUMNS: list[str] = [spec.name for spec in SCHEMA_SPECS]

CONTRACT_ORDER: list[str] = ["Month-to-month", "One year", "Two year"]
INTERNET_ORDER: list[str] = ["Fiber optic", "DSL", "No"]
PAYMENT_ORDER: list[str] = [
    "Electronic check",
    "Mailed check",
    "Bank transfer (automatic)",
    "Credit card (automatic)",
]
TENURE_TIER_BINS: list[int] = [-1, 0, 12, 24, 48, 72]
TENURE_TIER_LABELS: list[str] = [
    "0 mo (New)",
    "1-12 mo",
    "13-24 mo",
    "25-48 mo",
    "49-72 mo",
]
