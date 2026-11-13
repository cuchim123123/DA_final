# Data Quality Audit & Preprocessing Decisions

1. **No Silent Row Removal (`N = 7,043` Retained):**
   - Exact row duplicates: `0` (`7,043` unique `customerID` strings).
   - Non-ID identical feature+target rows: `22` rows match another customer across all 19 predictors and target `Churn` (primarily month-1 subscribers on identical discrete base plans). Because each carries a distinct `customerID` in a cross-sectional snapshot, dropping them would distort segment prevalence. All `7,043` rows are retained.
2. **`TotalCharges` String Parsing (`11` Blank Entries = `0.1562%`):**
   - In the raw CSV, `TotalCharges` is stored as text because `11` records contain whitespace (`" "`).
   - Exact verification confirms **100% of these `11` blank entries (`all_blank_total_charges_are_tenure_zero=True`) occur when `tenure == 0` and `Churn == "No"`**.
   - **Treatment:** Parsed to `NaN` via `pd.to_numeric(..., errors="coerce")` for transparent EDA auditing; inside predictive modeling, missing numeric values are imputed using **`SimpleImputer(strategy="median")` fitted strictly inside training CV folds**, guaranteeing zero leakage to held-out test records or single-profile inputs.
3. **Identifier & Target Leakage Prevention:**
   - `customerID` is excluded from all model matrices (`X`) and used strictly to assert zero train/test overlap.
   - Exploratory binned column `tenure_tier` is computed in EDA/diagnostics only and never fed into predictive preprocessing alongside `tenure` (`RAW_PREDICTORS` contains strictly the 19 exogenous schema columns).
4. **Service Dependency Integrity:**
   - Verified 0 inconsistencies between `PhoneService == "No"` ($n=682$) and `MultipleLines == "No phone service"`, and 0 inconsistencies between `InternetService == "No"` ($n=1,526$) and `"No internet service"` across all 6 online add-ons. The interactive scoring helper enforces these exact dependency constraints automatically.
