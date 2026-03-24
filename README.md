# Mandelbrot & Julia Explorer

Explorador interactivo del conjunto de Mandelbrot y conjuntos de Julia mediante un sistema de tiles generados bajo demanda.

## Estructura

- `server.py` — API Flask que genera y sirve las imágenes
- `index.html` — Explorador interactivo del Mandelbrot (zoom, pan, tiles progresivos)
- `julia.html` — Explorador de conjuntos de Julia
- `lvl.html` — Visor de progreso por nivel
- `count.php` — Endpoint PHP que devuelve estadísticas de imágenes generadas
- `mandelbrot.py` / `mandelbrot_zoom.py` — Lógica de generación de Mandelbrot
- `julia.py` — Lógica de generación de Julia
- `mandelbrot_calc.cpp` — Motor de cálculo en C++ (compilado como `.dll` / `.so`)

## Requisitos

- Python 3 con `flask`, `flask-cors`, `Pillow`
- PHP (para `count.php`)
- Compilador C++ (para recompilar la librería nativa si es necesario)

## Ejecución

```bash
python server.py
```

El servidor arranca en `0.0.0.0:5000`.

## Despliegue en Linux

> [!IMPORTANT]
> Para que el servidor web pueda escribir las imágenes generadas, hay que dar permisos a la carpeta `img/`:
> ```bash
> chmod 755 img
> chown user:user img
> ```
> Sustituye `user:user` por el usuario y grupo bajo el que corre el servidor web.
