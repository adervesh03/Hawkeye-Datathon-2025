import os, json, joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

MODEL_DIR = os.getenv("MODEL_DIR", "models")

# Load model + schema
model = joblib.load(os.path.join(MODEL_DIR, "rf_model.pkl"))
with open(os.path.join(MODEL_DIR, "feature_columns.json"), "r") as f:
    FEATURE_COLUMNS = json.load(f)

# Risk segmentation (optional)

app = Flask(__name__)

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