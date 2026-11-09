# Brief para David - Practica 3

Documento local de trabajo. No se sube a git ni se incluye en el ZIP.

## Contexto

Practica 3 de IA: conectar una aplicacion Streamlit con un servicio de IA propio
(FastAPI) y desplegar ambos en Render usando GitHub.

Decisiones ya cerradas:

- Contrato de la API: `POST /predict` devuelve `{"MedHouseVal": <float>}` en
  cientos de miles. Streamlit multiplica por `100000` y formatea en dolares.
- Sin autenticacion adicional: se sigue el enunciado de la practica.
- Despliegue: Render nativo desde GitHub. Sin Docker salvo necesidad estricta.
- `practica2/` no se toca.
- El contenido tecnico debe ser coherente con la teoria UD3 aportada.
- Nada de rastros de IA en el repo ni en el ZIP: sin guias, prompts, XML, renders,
  scripts de comparacion, logs de opencode ni `.trabajo/`.

## Rama y arranque

```bash
git fetch origin
git switch david
git pull origin david
```

Si Daniel ya subio el scaffold, sincroniza tambien `main`:

```bash
git fetch origin
git rebase origin/main
```

## Archivos que te pertenecen

- `recursos/ejercicio_e/codigo/streamlit_app.py`
- `recursos/ejercicio_b/`
- `recursos/ejercicio_c/`
- `recursos/ejercicio_d/`
- Memoria DOCX/PDF: apartados b, c y d

No edites `app.py`, `requirements.txt`, `modelo_california.pkl`, el `README.md`
del codigo ni los recursos de los apartados a y e: son de Daniel.

## Tareas

### 1. Completar `streamlit_app.py`

Parte de la plantilla de `src_p3.zip`. Completa solo los TODO:

- `AUTORES = "David Araiz Saez, Daniel Bernal Anzano"`.
- TODO 0: `API_URL = os.getenv("API_URL", "http://localhost:8000")`.
- TODO 1: `requests.post(api_url + "/predict", json=payload, timeout=TIMEOUT)`.
- TODO 2: `find_missing()`: falta si la clave no existe o es `None`; `0.0` es
  valido.
- TODO 3: `format_price()`: multiplicar por `100000` y devolver
  `f"${precio:,.0f}"`.
- TODO 4: `st.metric("Precio estimado", format_price(...))` y `st.caption` con el
  valor crudo devuelto por la API.
- TODO 5a: mensaje claro si falla la comunicacion.
- TODO 5b: un solo `st.error` con codigo y `response.text`; no llames a
  `response.json()` en errores 500.
- TODO 6: `st.number_input` para `AveRooms`.

No introduzcas estilos nuevos ni cambies el resto de la plantilla.

Si Daniel aun no subio el scaffold, crea la carpeta y copia solo tu fichero:

```bash
mkdir -p recursos/ejercicio_e/codigo
unzip -o src_p3.zip -d /tmp/p3_src
cp /tmp/p3_src/src_p3/streamlit_app.py recursos/ejercicio_e/codigo/
```

### 2. Prueba local

Necesitas la API local de Daniel o la URL publica de Render.

```bash
cd recursos/ejercicio_e/codigo
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run streamlit_app.py
```

Pruebas:

- Peticion valida con `MedInc` y `AveRooms` reales: HTTP 200 y precio formateado.
- Campo faltante: no se envia y se indica cual falta.
- Saltar validacion con campo faltante: error 422 controlado.
- URL de API incorrecta: mensaje claro de fallo de comunicacion.
- Valor crudo y precio formateado visibles.

### 3. Evidencias de los apartados b, c y d

En `recursos/ejercicio_b/`:

- Captura de peticion valida.
- Captura de peticion con campo faltante.

En `recursos/ejercicio_c/`:

- Captura o nota con el valor crudo devuelto por la API y el precio formateado.

En `recursos/ejercicio_d/`:

- Captura de la interfaz funcionando con un caso real.

Todas las capturas deben incluir nombre de autor y `P3`.

### 4. Memoria

Usa el flujo de `.trabajo/createpdfguide.md`: analizar original, generar DOCX,
convertir con LibreOffice y verificar.

- Parte del DOCX original. No reescribas el enunciado.
- Rellena nombres y DNI.
- Inserta respuestas despues de cada apartado.
- Tus apartados: b, c y d.
- Verificacion obligatoria: 0 palabras ausentes, mismo numero de paginas,
  desviacion vertical maxima <= 2 pt, mismo conjunto de estilos, enlaces,
  imagenes y tablas correctos, y reproducibilidad.
- Un solo editor de la memoria a la vez. Coordina con Daniel.

### 5. Coordinacion con Daniel

- Necesitas la URL publica de la API (`API_URL`) para la captura final y la
  memoria. Pidesela a Daniel cuando Render este listo.
- Antes de tocar la memoria, confirma que Daniel no la esta editando.

## Antes de cada commit

```bash
git status
git diff --staged
git config user.name
git config user.email
git log --format='%an <%ae>' -1
```

El email debe estar verificado en tu cuenta de GitHub. Solo deben entrar tus
archivos. Nunca `practica2/`, `.trabajo/`, `.venv/`, `__pycache__/` ni artefactos
temporales.

## Commits y Pull Request

```bash
git add recursos/ejercicio_e/codigo/streamlit_app.py
git commit -m "Completa conexion e interfaz de Streamlit"

git add recursos/ejercicio_b recursos/ejercicio_c recursos/ejercicio_d
git commit -m "Anade pruebas y capturas de entrada, salida e interfaz"

git push -u origin david
```

Abre PR `david` -> `main`, pide revision a Daniel y haz merge tras aprobacion.
