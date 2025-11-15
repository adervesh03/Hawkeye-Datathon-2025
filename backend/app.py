import os, json, joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

MODEL_DIR = os.getenv("MODEL_DIR", "models")

# Load model + schema
model = joblib.load(os.path.join(MODEL_DIR, "freq_sev_xgboost/xgb_model.pkl"))
with open(os.path.join(MODEL_DIR, "feature_columns.json"), "r") as f:
    FEATURE_COLUMNS = json.load(f)

# Risk segmentation
with open(os.path.join(MODEL_DIR, "risk_quantiles.json"), "r") as f:
    quantiles = json.load(f)

kmeans = joblib.load(os.path.join(MODEL_DIR, "freq_sev_xgboost/kmeans_clusters.pkl"))

q33 = quantiles["q33"]
q66 = quantiles["q66"]

def classify_quantile(pred_per_exposure, type="kmeans"):
    if type == "kmeans":
        cluster = kmeans.predict(np.array([[pred_per_exposure]]))[0]
        cluster_map = {
            0: "Low",
            1: "Medium",
            2: "High"
        }
        risk = cluster_map[cluster]
        return risk
    # else use quantile method
    else:
        if pred_per_exposure <= q33:
            return "Low"
        elif pred_per_exposure <= q66:
            return "Medium"
        else:
            return "High"
        

# Flask API
app = Flask(__name__)

# Enable CORS for all origins
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=False,                 # must be False when using "*"
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)

def to_dataframe(payload: dict) -> pd.DataFrame:
    # Build a 1-row DataFrame with the exact training columns and order.
    # Missing columns -> error; extra fields -> ignored.
    missing = [c for c in FEATURE_COLUMNS if c not in payload]
    if missing:
        raise ValueError(f"Missing required feature(s): {missing}")
    # Use only known columns, in order
    row = {c: payload[c] for c in FEATURE_COLUMNS}
    return pd.DataFrame([row], columns=FEATURE_COLUMNS)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True)
        df = to_dataframe(payload)
        for col in df.select_dtypes("object"):
            df[col] = df[col].astype("category").cat.codes

        # Predict
        pred = float(model.predict(df)[0])
        body = {"expected_loss": round(pred, 4)}
        return jsonify(body), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"[ERROR] {e}", flush=True)
        return jsonify({"error": "prediction failed"}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)), debug=True)