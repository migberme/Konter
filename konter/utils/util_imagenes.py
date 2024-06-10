from PIL import ImageTk, Image

# Esta funcion lee la ruta de la imagen y el tamaño
def leer_imagen(path, size):
    #return ImageTk.PhotoImage(Image.open(path).resize(size, Image.Resampling.LANCZOS))
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ADAPTIVE))