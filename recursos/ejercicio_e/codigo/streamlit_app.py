"""Interfaz Streamlit para estimar el precio de casas en California.

Llama a la API FastAPI (POST /predict) con los datos de la zona y enseña el precio.

Autores: David Araiz Saez, Daniel Bernal Anzano
"""
import logging
import os
import time

import requests
import streamlit as st

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("app")

AUTORES = "David Araiz Saez, Daniel Bernal Anzano"
API_URL = os.getenv("API_URL", "http://localhost:8000")
TIMEOUT = 90

FEATURE_NAMES = [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms",
    "Population", "AveOccup", "Latitude", "Longitude",
]

DEFAULTS = {
    "HouseAge": 29.0,
    "AveBedrms": 1.05,
    "Population": 1166.0,
    "AveOccup": 2.8,
    "Latitude": 34.26,
    "Longitude": -118.49,
}


def find_missing(payload: dict) -> list[str]:
    """Devuelve las variables de FEATURE_NAMES que faltan en `payload`."""
    return [nombre for nombre in FEATURE_NAMES if payload.get(nombre) is None]


def format_price(med_house_val: float) -> str:
    """Convierte la salida del modelo a un texto legible en dólares."""
    precio = med_house_val * 100_000
    return f"${precio:,.0f}"


st.set_page_config(page_title="Precio de casas en California")
st.title("Precio de casas en California")
st.caption(f"{AUTORES} - P3")
st.write("Introduce los datos de la zona y estima el precio medio de sus viviendas.")

# Barra lateral: URL de la API y casillas de prueba
api_url = st.sidebar.text_input("URL de la API", API_URL).rstrip("/")
simulate_missing = st.sidebar.checkbox("Prueba: omitir HouseAge de la petición")
skip_validation = st.sidebar.checkbox(
    "Prueba: saltar la validación local (provoca un 422 de la API)"
)

# Datos que mete el usuario
med_inc = st.number_input(
    "Ingreso medio de la zona (decenas de miles de $)",
    min_value=0.0, max_value=15.0, value=3.5, step=0.1,
)
ave_rooms = st.number_input(
    "Número medio de habitaciones por vivienda",
    min_value=1.0, max_value=15.0, value=5.2, step=0.1,
)

if st.button("Estimar precio"):
    payload = {
        **DEFAULTS,
        "MedInc": med_inc,
        "AveRooms": ave_rooms,
    }
    if simulate_missing:
        payload.pop("HouseAge", None)

    # Comprobar que no falta nada antes de enviar
    missing = find_missing(payload)
    if skip_validation and missing:
        logger.warning("Validación local saltada (prueba). Faltan: %s", missing)
    elif missing:
        logger.warning("Petición no enviada, faltan: %s", missing)
        st.error(f"Faltan variables obligatorias: {', '.join(missing)}")
        st.stop()

    try:
        start = time.perf_counter()
        with st.spinner("Consultando la API (la primera vez puede tardar más de un minuto)..."):
            response = requests.post(f"{api_url}/predict", json=payload, timeout=TIMEOUT)
        elapsed_ms = (time.perf_counter() - start) * 1000
    except requests.RequestException as exc:
        logger.error("Fallo de comunicación con %s: %s", api_url, exc)
        st.error(
            "No se pudo contactar con la API. Comprueba que la URL sea correcta y que "
            "el servicio esté activo (si está arrancando en Render, puede tardar más de un minuto)."
        )
    else:
        logger.info("POST %s/predict -> HTTP %s en %.0f ms", api_url, response.status_code, elapsed_ms)
        if response.status_code == 200:
            med_house_val = response.json()["MedHouseVal"]
            st.metric("Precio estimado", format_price(med_house_val))
            st.caption(f"Valor devuelto por la API (sin formatear): {med_house_val}")
        else:
            st.error(f"Error {response.status_code} devuelto por la API: {response.text}")
