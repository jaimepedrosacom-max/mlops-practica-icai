"""Frontend Streamlit que llama a la API de inferencia (variable de entorno API_URL)."""
import os

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:5000/predict")
CLASSES = {0: "Iris setosa", 1: "Iris versicolor", 2: "Iris virginica"}

st.title("Clasificador de flores Iris")
st.write("Introduce las medidas de la flor y pulsa **Predecir**.")

col1, col2 = st.columns(2)
with col1:
    sepal_length = st.number_input("Longitud del sépalo (cm)", 0.0, 10.0, 5.1, 0.1)
    petal_length = st.number_input("Longitud del pétalo (cm)", 0.0, 10.0, 1.4, 0.1)
with col2:
    sepal_width = st.number_input("Anchura del sépalo (cm)", 0.0, 10.0, 3.5, 0.1)
    petal_width = st.number_input("Anchura del pétalo (cm)", 0.0, 10.0, 0.2, 0.1)

if st.button("Predecir"):
    payload = {"features": [sepal_length, sepal_width, petal_length, petal_width]}
    try:
        resp = requests.post(API_URL, json=payload, timeout=10)
        resp.raise_for_status()
        pred = resp.json()["prediction"]
        st.success(f"Predicción: **{CLASSES.get(pred, pred)}** (clase {pred})")
    except Exception as exc:
        st.error(f"Error llamando a la API ({API_URL}): {exc}")
