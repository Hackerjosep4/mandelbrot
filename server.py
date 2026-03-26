from flask import Flask, jsonify, abort
from flask_cors import CORS
from mandelbrot_zoom import generarImagenSector
from julia import generarImagenJulia
import os

app = Flask(__name__)
CORS(app)

os.makedirs("img", exist_ok=True)

@app.route('/tile/<int:n>/<int(signed=True):x>/<int(signed=True):y>')
def get_tile(n, x, y):
    try:
        generarImagenSector(x, y, n)
        return jsonify({"ok": True})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/julia/<x>/<y>/<int:s>')
def get_julia(x, y, s):
    try:
        generarImagenJulia(float(x), float(y), s)
        return jsonify({"ok": True})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/julias')
def get_julias():
    seen = set()
    julias = []
    if not os.path.exists("img/julia"):
        return jsonify({"julias": julias})
    for f in os.listdir("img/julia"):
        if not f.endswith(".png"):
            continue
        # Format fitxer: jl_X_Y_S.png
        parts = f[3:-4].split("_")  # treu "jl_" i ".png" -> ["X","Y","S"]
        if len(parts) == 3:
            key = (parts[0], parts[1])
            if key not in seen:
                seen.add(key)
                julias.append({"x": float(parts[0]), "y": float(parts[1])})
    return jsonify({"julias": julias})

@app.route('/check/<int:n>/<int:x>/<int:y>')
def check_tile(n, x, y):
    ruta = f"img/{n}/mbz_{n}_{x}_{y}.png"
    return jsonify({"exists": os.path.isfile(ruta)})

@app.route('/level/<int:n>')
def get_level(n):
    tiles = []
    os.makedirs(f"img/{n}", exist_ok=True)
    for f in os.listdir(f"img/{n}"):
        if not f.endswith(".png"):
            continue
        # Format fitxer: mbz_N_X_Y.png
        parts = f[4:-4].split("_")  # treu "mbz_" i ".png" -> ["N","X","Y"]
        if len(parts) == 3 and parts[0] == str(n):
            tiles.append({"x": int(parts[1]), "y": int(parts[2])})
    return jsonify({"n": n, "tiles": tiles})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
