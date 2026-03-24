from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import filedialog
import math
import os
import re
from mandelbrot import mandelbrot


def mostrar_imagen(root, ruta):
    for widget in root.winfo_children():
        widget.destroy()
    imgtk = ImageTk.PhotoImage(Image.open(ruta))
    root.img_ref = imgtk
    tk.Label(root, image=imgtk).pack()

def validar_imagen(ruta):
    # Comprobar si el archivo existe
    if not os.path.exists(ruta):
        return False
    try:
        # Intentar abrir la imagen
        with Image.open(ruta) as img:
            # Comprobar tamaño exacto
            return img.size == (500, 500)
    except Exception:
        # Si no se puede abrir como imagen, también es inválida
        return False

def coords_a_xyn(inx, iny, dst):
    n = math.ceil(math.log2(4 / dst))
    cell = 4 / (2 ** n)
    x = math.floor((inx + 2) / cell)
    y = math.floor((iny + 2) / cell)
    return x, y, n

def generarImagen(inx, iny, dst):
    x, y, n = coords_a_xyn(inx, iny, dst)
    cell = 4 / (2 ** n)
    imgs = [[],[]]
    imgb = Image.new("RGB", (1000, 1000))
    for i in range(2):
        for j in range(2):
            img, _ = generarImagenSector(x+j, y+i, n)
            imgs[i].append(img)
            imgb.paste(imgs[i][j], (j*500, (1-i)*500))

    origen_x = x * cell - 2
    origen_y = y * cell - 2
    escala = 1000 / (2 * cell)  # px por unidad

    size = int(dst * escala)
    px0 = int((inx - origen_x) * escala)
    py0 = int((iny - origen_y) * escala)
    py0_img = 1000 - py0 - size

    return imgb.crop((px0, py0_img, px0 + size, py0_img + size)).resize((500, 500))

def generarImagenSector(x, y, n):
    cell = 4 / (2 ** n)
    ruta = f"img/{n}/mbz_{n}_{x}_{y}.png"
    os.makedirs(f"img/{n}", exist_ok=True)
    if validar_imagen(ruta):
        return Image.open(ruta), ruta
    else:
        img = mandelbrot(0.5, 100, ((x)*cell) - 2, ((x+1)*cell) - 2, ((y)*cell) - 2, ((y+1)*cell) - 2)
        img.save(ruta)
        return img, ruta

def generarOverlay(cc, sx, sy, tm):
    imgc = Image.new("RGBA", (500,500), (0,0,0,0))
    imgcd = ImageDraw.Draw(imgc)
    tc = 500 / cc
    x1 = (sx - 1) * tc
    x2 = x1 + tm * tc
    y1 = (cc - tm - (sy - 1)) * tc
    y2 = (cc - sy + 1) * tc
    imgcd.rectangle((x1, y1, x2, y2), fill=(0,255,0,100))
    for i in range(1, cc):
        pas = (500*i)//cc
        #print(f"Pas: {pas}")
        imgcd.line((pas, 0, pas, 500), fill=(255, 0, 0, 100))
        imgcd.line((0, pas, 500, pas), fill=(255, 0, 0, 100))
    return imgc

def actualizarOverlay(root, img, cc, sx, sy, tm):
    imgc = Image.alpha_composite(img.convert("RGBA"), generarOverlay(cc, sx, sy, tm))
    imgc.save("temp.png")
    mostrar_imagen(root, "temp.png")

def loadImagen():
    while True:
        ruta = filedialog.askopenfilename( title="Selecciona un arxiu PNG", filetypes=[("Imatges PNG", "*.png")] )
        if ruta and validar_imagen(ruta):
            nom = os.path.basename(ruta)
            patron = r"^mdbt_zoom_([-+]?\d*\.?\d+)_([-+]?\d*\.?\d+)_([-+]?\d*\.?\d+)\.png$"
            m = re.match(patron, nom)
            if not m:
                continue
            inx, iny, dst = map(float, m.groups())
            img = Image.open(ruta)
            img.save(nom)
            return img, nom, inx, iny, dst
                


if __name__ == '__main__':

    root = tk.Tk()

    dst = 3
    inx = -2
    iny = -1.5

    cc = 1
    sx = 1
    sy = 1
    tm = 1

    img = None

    menu = "r"


    while menu != "s":
        if len(menu) > 1 and menu[0] == "c":
            if menu[1:] == "+":
                cc += 1
            elif menu[1:] == "-":
                if cc > 1:
                    cc -= 1
            else:
                try:
                    cc = int(menu[1:])
                except:
                    pass
            actualizarOverlay(root, img, cc, sx, sy, tm)
        elif len(menu) > 1 and  menu[0] == "x":
            if menu[1:] == "+":
                sx += 1
            elif menu[1:] == "-":
                if sx > 1:
                    sx -= 1
            else:
                try:
                    sx = float(menu[1:])
                except:
                    pass
            actualizarOverlay(root, img, cc, sx, sy, tm)
        elif len(menu) > 1 and  menu[0] == "y":
            if menu[1:] == "+":
                sy += 1
            elif menu[1:] == "-":
                if sy > 1:
                    sy -= 1
            else:
                try:
                    sy = float(menu[1:])
                except:
                    pass
            actualizarOverlay(root, img, cc, sx, sy, tm)
        elif len(menu) > 1 and  menu[0] == "t":
            if menu[1:] == "+":
                tm += 1
            elif menu[1:] == "-":
                if tm > 1:
                    tm -= 1
            else:
                try:
                    tm = float(menu[1:])
                except:
                    pass
            actualizarOverlay(root, img, cc, sx, sy, tm)
        elif menu == "r":
            tc = dst / cc
            inx = inx + ((sx-1) * tc)
            iny = iny + ((sy-1) * tc)
            dst = tc * tm
            img = generarImagen(inx, iny, dst)
            img.save(f"temp.png")
            mostrar_imagen(root, "temp.png")
            cc = 1
            sx = 1
            sy = 1
            tm = 1
        menu = input(f"\n\nDades:\n\nCuadricula: {cc}\nX: {sx}\nY: {sy}\nTamany: {tm}\n\nMenu:\n\nC<n/+/-> - Cuadricula\nX<n/+/-> - Set x\nY<n/+/-> - Set y\nT<n/+/-> - Set tamany\nR - Renderitzar\n\nAccio: ").lower().strip()

if os.path.exists("temp.png"):
    os.remove("temp.png")

