from PIL import Image
import os
from mandelbrot import julia


NUM_SECTORS = 4  # 4x4 grid = 16 sectors
SECTOR_PX = 2500  # each sector is 2500x2500


def get_sector_bounds(s):
    """Calcula els limits del sector s (0-15) en una grid 4x4 sobre [-2,2]x[-2,2]"""
    col = s % NUM_SECTORS
    row = s // NUM_SECTORS
    step = 4 / NUM_SECTORS  # = 1
    x_min = -2 + col * step
    x_max = x_min + step
    y_max = 2 - row * step
    y_min = y_max - step
    return (x_min, x_max, y_min, y_max)


def validar_imagen(ruta):
    if not os.path.exists(ruta):
        return False
    try:
        with Image.open(ruta) as img:
            return img.size == (SECTOR_PX, SECTOR_PX)
    except Exception:
        return False

def generarImagenJulia(x, y, s):
    ruta = f"img/julia/jl_{x}_{y}_{s}.png"
    os.makedirs("img/julia", exist_ok=True)
    if validar_imagen(ruta):
        return Image.open(ruta), ruta
    else:
        x_min, x_max, y_min, y_max = get_sector_bounds(s)
        scale = SECTOR_PX / 1000
        img = julia(scale, 100, x_min, x_max, y_min, y_max, x, y)
        img.save(ruta)
        return img, ruta
