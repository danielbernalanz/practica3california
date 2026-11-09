# Brief para David - Practica 3

Documento local de trabajo. No se sube a git ni se incluye en el ZIP.

## Modo de trabajo

Ejecuta este brief de principio a fin. No pidas confirmacion para pasos ya
definidos aqui. Si algo falla, intenta la alternativa indicada antes de
preguntar.

Pregunta al usuario solo cuando sea imprescindible:

- Falta `sudo` o un paquete del sistema.
- Hace falta login manual en GitHub o Render.
- Hay que pegar URLs publicas o confirmar que un servicio esta Live.
- Faltan nombres, DNI, la teoria UD3 o el scaffold de Daniel.
- No puedes tomar capturas y necesitas que las tome el usuario.
- Hay una preferencia real de estilo o formato no fijada aqui.

Nunca pidas contrasenas, tokens ni claves. Si hace falta login, pide al usuario
que lo haga en el navegador y que confirme.

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

Cuando Daniel avise de que el scaffold esta en `main`:

```bash
git fetch origin
git rebase origin/main
```

Si `recursos/ejercicio_e/codigo/app.py` no existe, no lo crees: pregunta a Daniel
o espera al scaffold. Tu solo aportas `streamlit_app.py`.

## Archivos que te pertenecen

- `recursos/ejercicio_e/codigo/streamlit_app.py`
- `recursos/ejercicio_b/`
- `recursos/ejercicio_c/`
- `recursos/ejercicio_d/`
- Memoria DOCX/PDF: apartados b, c y d

No edites `app.py`, `requirements.txt`, `modelo_california.pkl`, el `README.md`
del codigo ni los recursos de los apartados a y e: son de Daniel.

## Entorno

Comprueba herramientas:

```bash
python3 --version
python3 -m venv .venv && echo VENV_OK || echo NEED_VENV
command -v soffice libreoffice pdftotext pdftoppm pdfinfo pdftohtml
command -v chromium chromium-browser google-chrome firefox
```

Si falta algo:

```bash
sudo apt-get update
sudo apt-get install -y python3-venv poppler-utils libreoffice fonts-liberation
```

Si no hay navegador headless para capturas, pregunta si instalarlo o si el
usuario prefiere hacer las capturas manualmente.

Crea el entorno dentro de `.trabajo/` o de la carpeta de codigo, nunca lo subas:

```bash
python3 -m venv .trabajo/venv
.trabajo/venv/bin/pip install -r recursos/ejercicio_e/codigo/requirements.txt
```

## Tareas

### 1. Completar `streamlit_app.py`

Parte de la plantilla. Completa solo los TODO sin cambiar el resto:

- `AUTORES = "David Araiz Saez, Daniel Bernal Anzano"`.
- TODO 0:
  ```python
  import os
  API_URL = os.getenv("API_URL", "http://localhost:8000")
  ```
- TODO 1: `response = requests.post(api_url + "/predict", json=payload, timeout=TIMEOUT)`.
- TODO 2: `find_missing()`: falta si `payload.get(nombre) is None`; `0.0` es
  valido. Devuelve la lista de nombres que faltan.
- TODO 3: `format_price()`: multiplica por `100000` y devuelve
  `f"${precio:,.0f}"`.
- TODO 4: muestra `st.metric("Precio estimado", format_price(med_house_val))` y
  un `st.caption` con el valor crudo devuelto por la API.
- TODO 5a: mensaje claro si falla la comunicacion, indicando que se compruebe la
  URL o que la API puede estar arrancando.
- TODO 5b: un solo `st.error` con el codigo y `response.text`; no llames a
  `response.json()` en errores 500.
- TODO 6: `st.number_input` para `AveRooms` con etiqueta
  "Numero medio de habitaciones por vivienda", `min_value=1.0`,
  `max_value=15.0`, `value=5.2`, `step=0.1`.

No introduzcas estilos nuevos ni toques el payload ni los defaults.

### 2. Prueba local

Necesitas la API local de Daniel o la URL publica de Render. Si Daniel no la
tiene arrancada, puedes arrancar la API del scaffold en otra terminal:

```bash
cd recursos/ejercicio_e/codigo
../../../.trabajo/venv/bin/uvicorn app:app --reload --port 8000
```

Y en otra:

```bash
cd recursos/ejercicio_e/codigo
../../../.trabajo/venv/bin/streamlit run streamlit_app.py
```

Pruebas obligatorias:

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

Si hay navegador headless, automatiza:

```bash
mkdir -p recursos/ejercicio_b recursos/ejercicio_c recursos/ejercicio_d
chromium --headless --disable-gpu --window-size=1400,1000 \
  --screenshot=recursos/ejercicio_d/ui.png \
  http://localhost:8501
```

Si no, pide al usuario las capturas. Todas deben incluir nombre de autor y `P3`.

### 4. Memoria

Parte del DOCX original. No reescribas el enunciado ni cambies el orden.

Usa la skill `replicar-pdf` si esta disponible en tu opencode. Si no, sigue este
flujo:

```bash
mkdir -p .trabajo/memoria
cp dawm2d_opia_practica_3.docx .trabajo/memoria/base.docx
soffice --headless --convert-to pdf --outdir .trabajo/memoria .trabajo/memoria/base.docx
pdfinfo .trabajo/memoria/base.pdf
pdffonts .trabajo/memoria/base.pdf
pdftohtml -xml -hidden -stdout .trabajo/memoria/base.pdf > .trabajo/memoria/base.xml
pdftoppm -png -r 150 .trabajo/memoria/base.pdf .trabajo/memoria/base
```

Genera `dawm2d_opia_p3.docx` con `python-docx`, copiando del original:

- Tamano de pagina y margenes exactos.
- Fuente, cuerpo y colores.
- Todos los parrafos del enunciado literales.
- Respuestas nuevas despues de cada apartado, sin mover el original.
- Nombres y DNI en la cabecera.

Convierte y verifica:

```bash
soffice --headless --convert-to pdf --outdir . dawm2d_opia_p3.docx
pdfinfo dawm2d_opia_p3.pdf
pdftohtml -xml -hidden -stdout dawm2d_opia_p3.pdf > .trabajo/memoria/nuevo.xml
pdftoppm -png -r 150 dawm2d_opia_p3.pdf .trabajo/memoria/nuevo
```

Criterios obligatorios:

- 0 palabras del original ausentes.
- Mismo numero de paginas.
- Desviacion vertical maxima en pagina 1 <= 2 pt.
- Mismo conjunto de estilos `(tamano, color)`.
- Enlaces, imagenes y tablas correctos.
- Reejecutar la generacion produce los mismos artefactos.

Comprueba palabras ausentes:

```bash
python3 - <<'PY'
import difflib, re
import xml.etree.ElementTree as ET

def palabras(xml):
    root = ET.parse(xml).getroot()
    txt = " ".join("".join(p.itertext()) for p in root.iter("page"))
    return re.sub(r"\s+", " ", txt.replace("\u00ad", "")).split()

ow = palabras(".trabajo/memoria/base.xml")
nw = palabras(".trabajo/memoria/nuevo.xml")
perdidas = [w for tag, i1, i2, _, _ in difflib.SequenceMatcher(a=ow, b=nw, autojunk=False).get_opcodes() if tag == "delete" for w in ow[i1:i2]]
print("Palabras ausentes:", len(perdidas))
PY
```

Tus apartados: b, c y d. Coordina con Daniel para que solo uno edite el DOCX a
la vez. Si el PDF no cumple, corrige y repite; no entregues uno peor.

### 5. Coordinacion

- Necesitas la URL publica de la API (`API_URL`) para la captura final y la
  memoria. Pidesela a Daniel cuando Render este listo.
- Si David empieza antes de que exista el scaffold, avisa y espera.
- Antes de tocar la memoria, confirma que Daniel no la esta editando.

### 6. Verificacion final

```bash
git status
git diff --stat origin/main...HEAD
git config user.name
git config user.email
git log --format='%an <%ae>' origin/main..HEAD
```

El email debe estar verificado en tu cuenta de GitHub. Solo deben entrar tus
archivos. Nunca `practica2/`, `.trabajo/`, `.venv/`, `__pycache__/`, la guia, la
teoria ni artefactos temporales.

### 7. Cierre de rama

Antes del PR, borra tu brief de la rama:

```bash
git rm BRIEF_DAVID.md
git commit -m "Elimina notas locales de trabajo"
git push origin david
```

Abre PR `david` -> `main`, pide revision a Daniel y mergea tras aprobacion.
Verifica en GitHub: Insights -> Contributors deben aparecer las dos cuentas.
