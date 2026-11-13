# How to Reproduce All Analytical Artifacts & Launch the Dashboard

All paths and commands operate from the `DA_midterm/` project root without developer-specific absolute paths.

## 1. Environment Setup
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install setuptools wheel
.\.venv\Scripts\python.exe -m pip install -e . --no-build-isolation --no-deps
```

## 2. Regenerate Complete Analytical Pipeline (Phases 1-4)
```powershell
.\.venv\Scripts\python.exe -m telco_churn.cli run-all
```
This deterministic command (seed `42`) verifies `data/raw/Telco-Customer-Churn.csv` (SHA-256 `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`), executes descriptive/diagnostic layers (`fig01`–`fig06`), runs Stratified 5-Fold CV and single-pass test evaluation (`fig07`–`fig09`), computes prescriptive tiers & scenario grids (`fig10`), and saves `outputs/results_summary.json`.

## 3. Run Automated Verification & Lint Checks
```powershell
.\.venv\Scripts\python.exe -m ruff check src app tests
.\.venv\Scripts\python.exe -m pytest -v
```

## 4. Launch Interactive Streamlit Dashboard
```powershell
.\.venv\Scripts\streamlit.exe run app/streamlit_app.py
```

## 5. Export and Validate Self-Contained Transfer Package
```powershell
.\.venv\Scripts\python.exe -m telco_churn.cli export-package
```
