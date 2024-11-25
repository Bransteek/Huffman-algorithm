import tkinter as tk
from tkinter import ttk
import Huffmans_algorithm as ha


# Funciones que se ejecutarán al presionar los botones
def compress():
    ha.compress()


def decompress():
    ha.decompress_file()


window = tk.Tk()
window.title("Mimic")
window.geometry("300x200")  # Tamaño de la ventana
window.configure(bg="#f0f0f0")  # Color de fondo

# Crear un estilo personalizado para los botones usando ttk
style = ttk.Style()
style.configure(
    "TButton", font=("Arial", 12), foreground="gray", background="purple", padding=10
)

# Crear dos botones con estilo ttk
boton1 = ttk.Button(window, text="Comprimir", style="TButton", command=compress)
boton1.pack(padx=20, pady=10)

boton2 = ttk.Button(window, text="Descomprimir", style="TButton", command=decompress)
boton2.pack(padx=20, pady=10)

# Ejecutar el loop principal de la ventana
window.mainloop()
