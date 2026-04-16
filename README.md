# digi_data

https://chatgpt.com/share/69e0abb9-2ca0-8320-85db-4c3087e41b2c


train+anomaly detection

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# ===== LOAD DATA =====
df = pd.read_csv("new.csv")

# ===== FEATURES / TARGET =====
feature_cols = [c for c in df.columns if c not in [
    'timestamp','time','load','fan1','fan2','stage'
]]

X = df[feature_cols].fillna(0)
y = df[['fan1','fan2','stage']]

# ===== SPLIT =====
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# ===== TRAIN MODEL =====
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# ===== SAVE MODEL =====
joblib.dump(model, "fan_model.pkl")

# ===== PREDICT =====
y_pred = model.predict(X_test)
y_pred = pd.DataFrame(y_pred, columns=['fan1_pred','fan2_pred','stage_pred'])

# ===== ERROR =====
error_fan1 = abs(y_test['fan1'].values - y_pred['fan1_pred'])
error_fan2 = abs(y_test['fan2'].values - y_pred['fan2_pred'])
error_stage = abs(y_test['stage'].values - y_pred['stage_pred'])

total_error = error_fan1 + error_fan2 + error_stage

# ===== METRIC =====
mae = mean_absolute_error(y_test, y_pred)
print("MAE:", mae)

# ===== THRESHOLD =====
mean_error = total_error.mean()
std_error = total_error.std()
threshold = mean_error + 3 * std_error

print("Mean error:", mean_error)
print("Threshold:", threshold)

# ===== ANOMALY =====
anomaly = (total_error > threshold).astype(int)

# ===== HEALTH =====
health = 1 / (1 + total_error)

# ===== SAVE OUTPUT =====
output = X_test.copy()
output['fan1'] = y_test['fan1'].values
output['fan2'] = y_test['fan2'].values
output['stage'] = y_test['stage'].values

output['error'] = total_error
output['anomaly'] = anomaly
output['health'] = health

output.to_csv("anomaly_output.csv", index=False)











degradation injection+anomaly test

import pandas as pd
import joblib
import numpy as np

# ===== LOAD =====
df = pd.read_csv("new.csv")
model = joblib.load("fan_model.pkl")

# ===== FEATURES =====
feature_cols = [c for c in df.columns if c not in [
    'timestamp','time','load','fan1','fan2','stage'
]]

X = df[feature_cols].fillna(0)
y_actual = df[['fan1','fan2','stage']]

# =========================================================
# 🔥 DEGRADATION INJECTION (PHYSICS-BASED)
# =========================================================

df_deg = df.copy()

# --- 1. Cooling inefficiency (dust / airflow loss)
# Same load → higher temp
df_deg["cpu_temp"] *= 1.10
df_deg["gpu_temp"] *= 1.08

# --- 2. Thermal paste degradation
# Faster heating (simulate via temp drift)
df_deg["cpu_temp"] += np.linspace(0, 5, len(df_deg))

# --- 3. Fan inefficiency
# Needs more fan to achieve same cooling
df_deg["fan1"] *= 1.15
df_deg["fan2"] *= 1.15

# --- 4. Control delay (VERY IMPORTANT)
# Fan reacts late
df_deg["fan1"] = df_deg["fan1"].shift(3).fillna(method="bfill")
df_deg["fan2"] = df_deg["fan2"].shift(3).fillna(method="bfill")

# --- 5. Slight power inefficiency
df_deg["power"] *= 1.05

# =========================================================
# 🔥 RUN MODEL ON DEGRADED SYSTEM
# =========================================================

X_deg = df_deg[feature_cols].fillna(0)

y_pred = model.predict(X_deg)
y_pred = pd.DataFrame(y_pred, columns=['fan1_pred','fan2_pred','stage_pred'])

# =========================================================
# 🔥 ERROR (ANOMALY SIGNAL)
# =========================================================

df_deg['error_fan1'] = abs(df_deg['fan1'] - y_pred['fan1_pred'])
df_deg['error_fan2'] = abs(df_deg['fan2'] - y_pred['fan2_pred'])
df_deg['error_stage'] = abs(df_deg['stage'] - y_pred['stage_pred'])

df_deg['total_error'] = (
    df_deg['error_fan1'] +
    df_deg['error_fan2'] +
    df_deg['error_stage']
)

# =========================================================
# 🔥 HEALTH SCORE
# =========================================================

df_deg['health'] = 1 / (1 + df_deg['total_error'])

# =========================================================
# 🔥 OPTIONAL: ANOMALY FLAG (reuse threshold)
# =========================================================

# recompute baseline threshold from original data
baseline_pred = model.predict(X)
baseline_error = abs(y_actual.values - baseline_pred)
baseline_error = baseline_error.sum(axis=1)

threshold = baseline_error.mean() + 3 * baseline_error.std()

df_deg['anomaly'] = (df_deg['total_error'] > threshold).astype(int)

# =========================================================
# SAVE
# =========================================================

df_deg.to_csv("degraded_output.csv", index=False)

print("🔥 Degradation simulation complete")
print("Threshold:", threshold)
print("Avg degraded error:", df_deg['total_error'].mean())






RUL estimation

FAILURE_THRESHOLD = threshold * 2

df_deg['error_smooth'] = df_deg['total_error'].rolling(10).mean()

import numpy as np
from sklearn.linear_model import LinearRegression

t = np.arange(len(df_deg)).reshape(-1, 1)
y = df_deg['error_smooth'].fillna(method='bfill').values

model_trend = LinearRegression()
model_trend.fit(t, y)

slope = model_trend.coef_[0]
current_error = y[-1]

if slope > 0:
    RUL = (FAILURE_THRESHOLD - current_error) / slope
else:
    RUL = float('inf')

print("Slope:", slope)
print("Current error:", current_error)
print("RUL (seconds):", max(0, RUL))
print("RUL (minutes):", max(0, RUL)/60)



