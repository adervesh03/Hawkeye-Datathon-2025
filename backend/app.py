import os, json, joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# -------------- Helper Functions -------------- #

MODEL_DIR = os.getenv("MODEL_DIR", "models")

# Load model + schema
model = joblib.load(os.path.join(MODEL_DIR, "freq_sev_xgboost/xgb_model.pkl"))
with open(os.path.join(MODEL_DIR, "feature_columns.json"), "r") as f:
    FEATURE_COLUMNS = json.load(f)

# Risk segmentation
with open(os.path.join(MODEL_DIR, "risk_quantiles.json"), "r") as f:
    quantiles = json.load(f)

q33 = quantiles["q33"]
q66 = quantiles["q66"]
kmeans = joblib.load(os.path.join(MODEL_DIR, "freq_sev_xgboost/kmeans_clusters.pkl"))

# Classifies pred_per_exposure into Low, Medium, High risk categories
def classify_risk(pred_per_exposure, type="kmeans"):
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
        
# Convert incoming JSON payload to DataFrame
def to_dataframe(payload: dict) -> pd.DataFrame:
    # Build a 1-row DataFrame with the exact training columns and order.
    # Missing columns -> error; extra fields -> ignored.
    missing = [c for c in FEATURE_COLUMNS if c not in payload]
    if missing:
        raise ValueError(f"Missing required feature(s): {missing}")
    # Use only known columns, in order
    row = {c: payload[c] for c in FEATURE_COLUMNS}
    return pd.DataFrame([row], columns=FEATURE_COLUMNS)

# Encoding functions
def group_age_category(cat):
    """Groups 'agecat' into Young, Middle, Elder."""
    if cat == 1:
        return 'Young'
    elif cat == 6:
        return 'Elder'
    else:
        return 'Middle'
    
KEEP_BODIES = {'SEDAN', 'STNWG', 'SUV', 'TRUCK', 'UTE', 'HDTOP', 'PANVN', 'MIBUS', 'COUPE'}
def group_vehicle_body(body_style):
    if pd.isna(body_style):
        return 'OTHER'
    normalized_style = str(body_style).upper()
    return normalized_style if normalized_style in KEEP_BODIES else 'OTHER'


ENCODING_MAP = {
    'marital_status': {'M': 0, 'S': 1},
    'time_driven': {
        '12am - 6 am': 0,  
        '12pm - 6pm': 1,  
        '6am - 12pm': 2,  
        '6pm - 12am': 3
    },
    'area': {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5},
    'agecat_grouped': {'Elder': 0, 'Middle': 1, 'Young': 2},
    'gender': {'F': 0, 'M': 1},
    'veh_color': {
        'black': 0,  
        'blue': 1,  
        'brown': 2,  
        'gray': 3,  
        'green': 4,  
        'red': 5,  
        'silver': 6,
        'white': 7,  
        'yellow': 8},
    'engine_type': {'dissel': 0, 'electric': 1, 'hybrid': 2, 'petrol': 3},
    'veh_body_grouped': {'COUPE': 0,  'OTHER': 1,  'SEDAN': 2,  'STNWG': 3,  'SUV': 4,  'TRUCK': 5,  'UTE': 6}
}

# Function to encode dataframe into corresponding numerical values for prediction
def encode_df(df):
    df['agecat_grouped'] = df['agecat'].apply(group_age_category)
    df['veh_body_grouped'] = df['veh_body'].apply(group_vehicle_body)

    for col, mapping in ENCODING_MAP.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)
            df[col] = df[col].fillna(-1)
            df[col] = df[col].astype(int)
        else:
            print(f"[Warning] Mapped column '{col}' not in payload.")

    return df

# -------------- Flask API -------------- #
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

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True)
        df = to_dataframe(payload)
        df = encode_df(df)

        exposure = float(payload["exposure"])
        if exposure <= 0:
            raise ValueError("Exposure must be positive.")

        # Predict
        raw_pred_total = float(model.predict(df)[0])
        pred_total_loss = raw_pred_total * RESCALE_FACTOR # rescale to total loss
        pred_per_exposure = pred_total_loss / exposure  # per exposure

        # Classify risk
        risk_kmeans = classify_risk(pred_per_exposure, method="kmeans")
        risk_quantile = classify_risk(pred_per_exposure, method="quantile")

        body = {
            "pred_total_loss": round(pred_total_loss, 4),
            "pred_per_exposure": round(pred_per_exposure, 4),
            "risk_segment_kmeans": risk_kmeans,
            "risk_segment_quantile": risk_quantile,
        }
        return jsonify(body), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"[ERROR] {e}", flush=True)
        return jsonify({"error": "prediction failed"}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)), debug=True)