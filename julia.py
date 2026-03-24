from PIL import Image
import os
from mandelbrot import julia





def validar_imagen(ruta):
    # Comprobar si el archivo existe
    if not os.path.exists(ruta):
        return False
    try:
        # Intentar abrir la imagen
        with Image.open(ruta) as img:
            # Comprobar tamaño exacto
            return img.size == (10000, 10000)
    except Exception:
        # Si no se puede abrir como imagen, también es inválida
        return False

def generarImagenJulia(x, y):
    ruta = f"img/julia/jl_{x}_{y}.png"
    os.makedirs("img/julia", exist_ok=True)
    if validar_imagen(ruta):
        return Image.open(ruta), ruta
    else:
        img = julia(10, 100, -2, 2, -2, 2, x, y)
        img.save(ruta)
        return img, ruta
