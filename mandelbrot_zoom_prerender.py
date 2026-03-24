from mandelbrot_zoom import generarImagenSector

def recursivePreRender(reps):
    if reps == 0:
        return
    
    cc = 2**reps
    co = 0
    com = cc**2

    for x in range(cc):
        for y in range(cc):
            generarImagenSector(x, y, reps)
            co += 1
            print(f"Pre-rendering lvl {reps}: {co}/{com}")
    
    recursivePreRender(reps-1)

if __name__ == '__main__':
    reps = int(input("Nombre de capes renderitzades: "))
    recursivePreRender(reps)
