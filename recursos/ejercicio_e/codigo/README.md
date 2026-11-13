# Aplicación Streamlit para el precio de casas en California

La aplicación estima el precio medio de la vivienda en una zona censal de California a partir de
ocho variables (renta mediana, edad de las casas, habitaciones, población, latitud, etc.). Está
formada por dos servicios independientes: una **API FastAPI** (`app.py`) que carga el modelo
`modelo_california.pkl` y expone `POST /predict`, y una **interfaz Streamlit** (`streamlit_app.py`)
con un formulario que envía los datos a la API mediante `requests` y muestra el precio devuelto.
La interfaz no contiene el modelo: solo conoce la URL de la API, que se indica en la barra lateral.

Autores: David Araiz Saez, Daniel Bernal Anzano

## Servicios desplegados en Render

| Servicio | Qué es | URL |
|----------|--------|-----|
| API | FastAPI con el modelo (`app.py`) | <https://practica3-api-5qnf.onrender.com> |
| Interfaz | Streamlit (`streamlit_app.py`), que llama a la API | <https://practica3-streamlit.onrender.com> |

## Cómo ejecutarla en local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Terminal 1: API (http://localhost:8000, documentación en /docs)
uvicorn app:app --reload --port 8000

# Terminal 2: interfaz (http://localhost:8501)
streamlit run streamlit_app.py
```

En la barra lateral de la interfaz, la URL de la API en local es `http://localhost:8000`.

## Despliegue en Render

Ambos son Web Services Python (plan Free, región Frankfurt) sobre el repositorio `danielbernalanz/practica3california`, rama `main`. El código está en `recursos/ejercicio_e/codigo`, por eso los comandos entran en esa carpeta.

**API** (`practica3-api`)

- Build Command: `pip install -r recursos/ejercicio_e/codigo/requirements.txt`
- Start Command: `cd recursos/ejercicio_e/codigo && uvicorn app:app --host 0.0.0.0 --port $PORT`

**Interfaz** (`practica3-streamlit`)

- Build Command: `pip install -r recursos/ejercicio_e/codigo/requirements.txt`
- Variable de entorno: `API_URL=https://practica3-api-5qnf.onrender.com`
- Start Command: `cd recursos/ejercicio_e/codigo && streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
- La URL de la API se cambia en la barra lateral de la propia interfaz (campo «URL de la API»),
  poniendo la URL pública del servicio API de Render.

## Documentación de la API

URL base: <https://practica3-api-5qnf.onrender.com> (en local, `http://localhost:8000`)

### `POST /predict`

Recibe un JSON con las 8 variables de una zona censal (todas numéricas) y devuelve el precio
medio estimado en `MedHouseVal`, expresado en cientos de miles de dólares. `GET /` devuelve
`{"status": "ok"}` y sirve de comprobación de que el servicio está activo.

**Ejemplo de petición**

```json
{
  "MedInc": 8.3252,
  "HouseAge": 41,
  "AveRooms": 6.984127,
  "AveBedrms": 1.02381,
  "Population": 322,
  "AveOccup": 2.555556,
  "Latitude": 37.88,
  "Longitude": -122.23
}
```

**Ejemplo de respuesta correcta (200)**

```json
{"MedHouseVal": 4.881880465116272}
```

**Errores**

| Código | Cuándo ocurre | Qué muestra la aplicación |
|--------|---------------|---------------------------|
| 422 | Falta un campo o tiene un tipo incorrecto (p. ej. `"MedInc": "abc"`) | `Error 422 devuelto por la API:` seguido del detalle JSON de FastAPI (`float_parsing`, `missing`...) |
| Sin respuesta | La API no está disponible o tarda demasiado | «No se pudo contactar con la API. Comprueba que la URL sea correcta y que el servicio esté activo (si está arrancando en Render, puede tardar más de un minuto).» |
