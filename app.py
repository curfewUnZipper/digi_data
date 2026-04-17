# =========================
# 📦 IMPORTS
# =========================
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import io

app = Flask(__name__)

# =========================
# LOAD MODEL + SCALER
# =========================
model = load_model("lstm_model.h5")
scaler = joblib.load("scaler.pkl")

WINDOW = 50

features = [
    "fan1","fan2",
    "cpu_temp","gpu_temp","nvidia_temp",
    "cpu_usage",
    "current","power"
]


# =========================
# HELPER: MAKE PREDICTION
# =========================
def predict_rul(df):

    df = df.copy()

    # scale
    df[features] = scaler.transform(df[features])

    # take last window
    if len(df) < WINDOW:
        return None

    window = df[features].values[-WINDOW:]
    window = np.expand_dims(window, axis=0)

    pred = model.predict(window)[0][0]

    return float(pred)


# =========================
# SINGLE INPUT
# =========================
@app.route("/predict_single", methods=["POST"])
def predict_single():

    data = request.json
    df = pd.DataFrame([data])

    rul = predict_rul(df)

    return jsonify({"RUL": rul})


# =========================
# MULTIPLE JSON INPUT
# =========================
@app.route("/predict_batch", methods=["POST"])
def predict_batch():

    data = request.json  # list of dicts
    df = pd.DataFrame(data)

    rul = predict_rul(df)

    return jsonify({"RUL": rul})


# =========================
# CSV INPUT
# =========================
@app.route("/predict_csv", methods=["POST"])
def predict_csv():

    file = request.files["file"]
    df = pd.read_csv(file)

    rul = predict_rul(df)

    return jsonify({"RUL": rul})


# =========================
# RETURN CSV OUTPUT
# =========================
@app.route("/predict_csv_output", methods=["POST"])
def predict_csv_output():

    file = request.files["file"]
    df = pd.read_csv(file)

    rul = predict_rul(df)

    df["predicted_RUL"] = rul

    output = io.StringIO()
    df.to_csv(output, index=False)

    return output.getvalue()


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)