"""
recortar_zapatos.py
-------------------
Usá este script PRIMERO para eliminar el fondo de tus fotos de zapatos.
Procesá todas las imágenes de una carpeta de entrada y las guarda como PNG
con fondo transparente en la carpeta de salida.

Uso:
    python recortar_zapatos.py --entrada fotos_originales --salida static/zapatos
"""

import argparse
import os
from pathlib import Path
from PIL import Image
from rembg import remove
import sys


EXTENSIONES_VALIDAS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def recortar_fondo(ruta_entrada: Path, ruta_salida: Path) -> None:
    """Elimina el fondo de una imagen y la guarda como PNG transparente."""
    print(f"  Procesando: {ruta_entrada.name} ...", end=" ")
    
    with open(ruta_entrada, "rb") as f:
        datos_entrada = f.read()
    
    datos_salida = remove(datos_entrada)
    
    # Guardar como PNG para mantener transparencia
    nombre_salida = ruta_salida / (ruta_entrada.stem + ".png")
    with open(nombre_salida, "wb") as f:
        f.write(datos_salida)
    
    # Recortar espacio vacío alrededor del zapato
    imagen = Image.open(nombre_salida)
    bbox = imagen.getbbox()
    if bbox:
        imagen_recortada = imagen.crop(bbox)
        imagen_recortada.save(nombre_salida)
    
    print(f"✓  Guardado en {nombre_salida.name}")


def procesar_carpeta(carpeta_entrada: str, carpeta_salida: str) -> None:
    entrada = Path(carpeta_entrada)
    salida = Path(carpeta_salida)
    
    if not entrada.exists():
        print(f"Error: la carpeta '{carpeta_entrada}' no existe.")
        sys.exit(1)
    
    salida.mkdir(parents=True, exist_ok=True)
    
    imagenes = [
        f for f in entrada.iterdir()
        if f.suffix.lower() in EXTENSIONES_VALIDAS
    ]
    
    if not imagenes:
        print(f"No se encontraron imágenes en '{carpeta_entrada}'.")
        sys.exit(1)
    
    print(f"\n🥿  Probador Virtual — Procesador de zapatos")
    print(f"   Imágenes encontradas: {len(imagenes)}")
    print(f"   Salida: {salida.resolve()}\n")
    
    for imagen in sorted(imagenes):
        recortar_fondo(imagen, salida)
    
    print(f"\n✅  Listo. {len(imagenes)} zapato(s) procesado(s).")
    print(f"   Ahora podés correr: python app.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Elimina el fondo de fotos de zapatos para el probador virtual."
    )
    parser.add_argument(
        "--entrada",
        default="fotos_originales",
        help="Carpeta con las fotos originales (default: fotos_originales)"
    )
    parser.add_argument(
        "--salida",
        default="static/zapatos",
        help="Carpeta de salida con PNG transparentes (default: static/zapatos)"
    )
    args = parser.parse_args()
    procesar_carpeta(args.entrada, args.salida)
