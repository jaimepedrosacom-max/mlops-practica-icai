"""API de inferencia: POST /predict con {"features": [sl, sw, pl, pw]} -> {"prediction": int}."""
import joblib
import pandas as pd
from flask import Flask, jsonify, request

FEATURES = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
]

app = Flask(__name__)
model = joblib.load("model.pkl")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    features = data.get("features")
    if not isinstance(features, list) or len(features) != len(FEATURES):
        return jsonify({"error": f"'features' debe ser una lista de {len(FEATURES)} números"}), 400
    try:
        X = pd.DataFrame([[float(v) for v in features]], columns=FEATURES)
    except (TypeError, ValueError):
        return jsonify({"error": "Todas las features deben ser numéricas"}), 400
    prediction = int(model.predict(X)[0])
    return jsonify({"prediction": prediction})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
