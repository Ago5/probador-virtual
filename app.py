from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
import numpy as np
import cv2
import base64
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

CARPETA_ZAPATOS = Path("static/zapatos")

def detectar_pies(frame):
    alto, ancho = frame.shape[:2]
    zona_pies = frame[alto//2:, :]
    gris = cv2.cvtColor(zona_pies, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gris, (5, 5), 0)
    bordes = cv2.Canny(blur, 30, 100)
    kernel = np.ones((5, 5), np.uint8)
    dilatado = cv2.dilate(bordes, kernel, iterations=2)
    contornos, _ = cv2.findContours(dilatado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return None, None
    contornos_validos = [c for c in contornos if cv2.contourArea(c) > 3000]
    if not contornos_validos:
        return None, None
    contornos_validos.sort(key=cv2.contourArea, reverse=True)
    pies = []
    for c in contornos_validos[:2]:
        x, y, w, h = cv2.boundingRect(c)
        cy_real = y + alto // 2
        pies.append({
            "talon": {"x": x + w // 2, "y": cy_real + h, "vis": 0.9},
            "punta": {"x": x + w, "y": cy_real + h // 2, "vis": 0.9},
            "bbox": {"x": x, "y": cy_real, "w": w, "h": h}
        })
    if len(pies) == 0:
        return None, None
    elif len(pies) == 1:
        return pies[0], None
    else:
        pies.sort(key=lambda p: p["talon"]["x"])
        return pies[0], pies[1]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/widget")
def widget():
    return render_template("widget.html")

@app.route("/zapatos")
def listar_zapatos():
    if not CARPETA_ZAPATOS.exists():
        return jsonify([])
    zapatos = [
        {
            "nombre": f.stem.replace("-", " ").replace("_", " ").title(),
            "archivo": f.name,
            "url": f"/static/zapatos/{f.name}"
        }
        for f in sorted(CARPETA_ZAPATOS.glob("*.png"))
    ]
    return jsonify(zapatos)

@app.route("/procesar-frame", methods=["POST"])
def procesar_frame():
    datos = request.get_json()
    if not datos or "frame" not in datos:
        return jsonify({"error": "Frame no recibido"}), 400
    frame_b64 = datos["frame"]
    if "," in frame_b64:
        frame_b64 = frame_b64.split(",")[1]
    frame_bytes = base64.b64decode(frame_b64)
    frame_np = np.frombuffer(frame_bytes, dtype=np.uint8)
    frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
    if frame is None:
        return jsonify({"detectado": False}), 200
    pie_izq, pie_der = detectar_pies(frame)
    if pie_izq is None and pie_der is None:
        return jsonify({"detectado": False}), 200
    respuesta = {
        "detectado": True,
        "pie_izquierdo": pie_izq,
        "pie_derecho": pie_der
    }
    return jsonify(respuesta)

@app.route("/static/zapatos/<nombre>")
def servir_zapato(nombre):
    return send_from_directory(CARPETA_ZAPATOS, nombre)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("Probador Virtual corriendo en http://localhost:" + str(port))
    app.run(host="0.0.0.0", port=port, debug=False)