# 🥿 Probador Virtual de Zapatos — Tienda Nube

Probador virtual con cámara en tiempo real usando MediaPipe + Flask.
Detecta los pies del cliente y superpone el zapato elegido en vivo.

---

## Estructura del proyecto

```
probador-virtual/
├── app.py                  ← Backend Flask (API + servidor)
├── recortar_zapatos.py     ← Script para procesar tus fotos
├── requirements.txt
├── templates/
│   ├── index.html          ← Página de demo
│   └── widget.html         ← Widget embebible en Tienda Nube
├── static/
│   └── zapatos/            ← Tus PNG con fondo transparente (se generan sólos)
└── fotos_originales/       ← Poné acá tus fotos con fondo
```

---

## Paso 1 — Instalación

```bash
# Clonar / descomprimir el proyecto
cd probador-virtual

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## Paso 2 — Preparar fotos de zapatos

1. Creá una carpeta llamada `fotos_originales/`
2. Copiá tus fotos de zapatos ahí (JPG, PNG, WEBP — con o sin fondo)
3. Corré el script de recorte:

```bash
python recortar_zapatos.py --entrada fotos_originales --salida static/zapatos
```

Esto elimina el fondo automáticamente y guarda los PNG transparentes en `static/zapatos/`.

---

## Paso 3 — Probar local

```bash
python app.py
```

Abrí tu navegador en: **http://localhost:5000**

Vas a ver la demo con el widget funcionando. Activá la cámara y apuntá a tus pies.

---

## Paso 4 — Deploy en Render (gratis)

1. Subí el proyecto a GitHub
2. Entrá a [render.com](https://render.com) y creá una cuenta gratuita
3. Nuevo servicio → **Web Service** → conectá tu repo
4. Configuración:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
   - **Environment:** Python 3
5. Deploy → Render te da una URL como `https://tu-app.onrender.com`

---

## Paso 5 — Embeber en Tienda Nube

En tu panel de Tienda Nube:
1. Ir a **Personalización → Editar código del tema**
2. En `snippets/` crear `probador.html`
3. Pegar el código que aparece en http://localhost:5000 (sección "Cómo embeber")
4. En la plantilla de producto (`product.html`) agregar: `{% include 'probador' %}`

Reemplazá `https://TU-APP.onrender.com` con la URL que te dio Render.

---

## Cómo funciona internamente

```
Cámara del cliente (browser)
        ↓ frame cada 125ms (JPEG base64)
POST /procesar-frame (Flask)
        ↓ MediaPipe detecta landmarks de pies
        ↓ Devuelve coordenadas talón + punta
Canvas API superpone el PNG del zapato
        ↓ rotado y escalado según los landmarks
Resultado: zapato virtual sobre los pies en tiempo real
```

---

## Comandos útiles

```bash
# Ver zapatos cargados
curl http://localhost:5000/zapatos

# Correr en modo desarrollo (auto-reload)
FLASK_ENV=development python app.py

# Recortar solo una foto
python recortar_zapatos.py --entrada mis_fotos --salida static/zapatos
```

---

## Dependencias principales

| Librería | Para qué |
|----------|----------|
| Flask | Servidor web / API |
| MediaPipe | Detección de pies en tiempo real |
| rembg | Eliminar fondo de fotos |
| OpenCV | Procesamiento de imágenes |
| Pillow | Manipulación de PNG |
