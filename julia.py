from PIL import Image
import os
from mandelbrot import julia


# Sectors: 0=top-left, 1=top-right, 2=bottom-left, 3=bottom-right
# (x_min, x_max, y_min, y_max) per sector
SECTORS = [
    (-2, 0, 0, 2),
    (0, 2, 0, 2),
    (-2, 0, -2, 0),
    (0, 2, -2, 0),
]

def validar_imagen(ruta):
    if not os.path.exists(ruta):
        return False
    try:
        with Image.open(ruta) as img:
            return img.size == (5000, 5000)
    except Exception:
        return False

def generarImagenJulia(x, y, s):
    ruta = f"img/julia/jl_{x}_{y}_{s}.png"
    os.makedirs("img/julia", exist_ok=True)
    if validar_imagen(ruta):
        return Image.open(ruta), ruta
    else:
        x_min, x_max, y_min, y_max = SECTORS[s]
        img = julia(5, 100, x_min, x_max, y_min, y_max, x, y)
        img.save(ruta)
        return img, ruta
