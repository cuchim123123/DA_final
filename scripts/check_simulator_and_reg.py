import sys
sys.path.insert(0, ".")
import numpy as np
import pandas as pd
from app.helpers import load_dashboard_artifacts, predict_bike_demand
from src.regression import (
    PRIMARY_PREDICTOR_ALLOWLIST,
    chronological_train_test_split,
    build_preprocessing_transformer
)
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error

art = load_dashboard_artifacts()

print("=== CHECKING SIMULATOR PREDICTIONS ===")

# Baseline Workday scenario:
# What were the exact inputs in the screenshot vs guide?
# Guide says:
# sim_yr=1, sim_season=3 (Fall), sim_daytype="Workday" (workingday=1, holiday=0), sim_weather=1 (Clear),
# temp=24.0°C, hum=55.0%, wind=14.0 km/h.
res_baseline = predict_bike_demand(
    art=art,
    yr=1,
    season=3,
    holiday=0,
    workingday=1,
    weathersit=1,
    temp_c=24.0,
    hum_pct=55.0,
    windspeed_kmh=14.0,
)
print("Baseline prediction with (yr=1, season=3, workday=1, weather=1, temp=24, hum=55, wind=14):")
print(res_baseline)

# What if yr=0 or season was different?
# In the app, what are the initial default inputs when opening tab 2 without query params?
# Let's check query defaults in streamlit_app.py:
# p_yr = 1, p_season = 3, p_daytype = "Workday", p_weather = 1, p_temp = 24.0, p_hum = 55.0, p_wind = 14.0
# Wait! In streamlit_app.py line 445:
# p_yr = int(st.query_params.get("sim_yr", 1))
# p_season = int(st.query_params.get("sim_season", 3))
# p_season_idx = max(0, min(3, p_season - 1)) # index 2
# But what if someone used default slider values before query params were added?
# In the original streamlit app before query params, what were the default values?
# Year selectbox index=0 (yr=0) or index=1 (yr=1)?
# If yr=0:
res_baseline_yr0 = predict_bike_demand(
    art=art,
    yr=0,
    season=3,
    holiday=0,
    workingday=1,
    weathersit=1,
    temp_c=24.0,
    hum_pct=55.0,
    windspeed_kmh=14.0,
)
print("\nBaseline prediction with yr=0:")
print(res_baseline_yr0)

# What if season=2 (Summer) or season=1 (Spring)?
for s in [1, 2, 3, 4]:
    r = predict_bike_demand(art, yr=1, season=s, holiday=0, workingday=1, weathersit=1, temp_c=24.0, hum_pct=55.0, windspeed_kmh=14.0)
    print(f"yr=1, season={s} (temp=24): cnt={r['predicted_cnt']}")
    r0 = predict_bike_demand(art, yr=0, season=s, holiday=0, workingday=1, weathersit=1, temp_c=24.0, hum_pct=55.0, windspeed_kmh=14.0)
    print(f"yr=0, season={s} (temp=24): cnt={r0['predicted_cnt']}")

# Adverse weather scenario:
# Guide says: yr=1, season=4 (Winter), sim_daytype="Workday", weather=3 (Light Rain/Snow), temp=4.0°C, hum=85.0%, wind=28.0 km/h.
res_adverse = predict_bike_demand(
    art=art,
    yr=1,
    season=4,
    holiday=0,
    workingday=1,
    weathersit=3,
    temp_c=4.0,
    hum_pct=85.0,
    windspeed_kmh=28.0,
)
print("\nAdverse prediction with (yr=1, season=4, workday=1, weather=3, temp=4, hum=85, wind=28):")
print(res_adverse)

# What if yr=0 for adverse?
res_adverse_yr0 = predict_bike_demand(art, yr=0, season=4, holiday=0, workingday=1, weathersit=3, temp_c=4.0, hum_pct=85.0, windspeed_kmh=28.0)
print(f"yr=0 adverse: cnt={res_adverse_yr0['predicted_cnt']}")

# What if season=1 (Spring)?
res_adverse_s1 = predict_bike_demand(art, yr=1, season=1, holiday=0, workingday=1, weathersit=3, temp_c=4.0, hum_pct=85.0, windspeed_kmh=28.0)
print(f"yr=1, season=1 adverse: cnt={res_adverse_s1['predicted_cnt']}")

print("\n=== MODEL PERFORMANCE METRICS ===")
train_df, test_df = chronological_train_test_split(art.df, train_fraction=0.80)
X_tr = train_df[PRIMARY_PREDICTOR_ALLOWLIST]
y_tr = train_df["cnt"].to_numpy()
X_te = test_df[PRIMARY_PREDICTOR_ALLOWLIST]
y_te = test_df["cnt"].to_numpy()

y_pred_tr = art.ols_pipe.predict(X_tr)
y_pred_te = art.ols_pipe.predict(X_te)

print(f"Train R2: {r2_score(y_tr, y_pred_tr):.4f}, RMSE: {root_mean_squared_error(y_tr, y_pred_tr):.2f}, MAE: {mean_absolute_error(y_tr, y_pred_tr):.2f}")
print(f"Test R2: {r2_score(y_te, y_pred_te):.4f}, RMSE: {root_mean_squared_error(y_te, y_pred_te):.2f}, MAE: {mean_absolute_error(y_te, y_pred_te):.2f}")
print(f"Test Bias: {float(np.mean(y_pred_te - y_te)):.2f}")

# What if someone computed R2 and RMSE across the WHOLE dataset (train + test)?
y_all = art.df["cnt"].to_numpy()
y_pred_all = art.ols_pipe.predict(art.df[PRIMARY_PREDICTOR_ALLOWLIST])
print(f"\nWhole dataset (Train+Test) R2: {r2_score(y_all, y_pred_all):.4f}, RMSE: {root_mean_squared_error(y_all, y_pred_all):.2f}, MAE: {mean_absolute_error(y_all, y_pred_all):.2f}")

# What if an OLS was fit on the whole dataset?
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
pipe_full = Pipeline([("pre", build_preprocessing_transformer()), ("model", LinearRegression())]).fit(art.df[PRIMARY_PREDICTOR_ALLOWLIST], y_all)
y_full_pred = pipe_full.predict(art.df[PRIMARY_PREDICTOR_ALLOWLIST])
print(f"Fit on Full dataset R2: {r2_score(y_all, y_full_pred):.4f}, RMSE: {root_mean_squared_error(y_all, y_full_pred):.2f}")
