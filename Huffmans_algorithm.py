from tkinter import filedialog, messagebox
import os

codes = {}


class Node:
    def __init__(self, value: int, letter: str = "", left=None, rigth=None):
        self.value = value
        self.letter = letter
        self.left = left
        self.rigth = rigth

    def __str__(self):
        return f"Node({self.value})"


def compress():
    frequency = {}

    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo de texto",
        filetypes=[("Archivos de texto", "*.txt")],  # Filtra solo archivos .txt
    )

    # Verifica si se ha seleccionado un archivo
    if file_path:
        try:
            # recorre las lineas de texto
            with open(file_path, "r") as archivo:
                for row in archivo:
                    # toma la frecuencia de las letras
                    for char in row:
                        if char in frequency:
                            frequency[char] += 1
                        else:
                            frequency[char] = 1

        except Exception as e:
            messagebox.showinfo("Error", f"Error al leer el archivo: {e}")

    else:
        messagebox.showinfo("Error", f"No se ha seleccionado ningún archivo.")
        return

    # convierte la lista en una tupla
    list_frequency = list(frequency.items())

    # organizar la lista
    list_frequency = sorted(list_frequency, key=lambda x: x[1])

    # Lista de nodos
    list_nodes = []

    for i in range(len(list_frequency)):
        list_nodes.append(Node(list_frequency[i][1], list_frequency[i][0]))

    # organiza la lista para que solo quede un arbol
    while len(list_nodes) > 1:
        first = list_nodes.pop(0)
        second = list_nodes.pop(0)

        node = Node(value=first.value + second.value, left=first, rigth=second)

        append_list(list_nodes, node)

    # pasa las letras a su codificacion utilizando el arbol
    encrypt(list_nodes.pop(0))
    save_compress_file(file_path, compress_text(file_path), codes)
    # print(codes)
    messagebox.showinfo("Exito", "Se ha comprimido correctamente")


# Agrega el nodo donde sea mayor
def append_list(list_huffman: list, node: Node):
    flag = False

    for i in range(len(list_huffman) - 1):

        if node.value < list_huffman[i + 1].value:
            list_huffman.insert(i, node)
            flag = True
            break

    if not flag:
        list_huffman.append(node)


def encrypt(node: Node, encode=""):
    global codes

    node_aux = node
    if node.letter != "":
        codes[node.letter] = encode
        return

    encrypt(node_aux.left, encode + "0")
    encrypt(node_aux.rigth, encode + "1")


# pasa el texto en los codigos
def compress_text(file_name: str):
    global codes
    compress_txt = ""
    with open(file_name, "r") as file:
        for row in file:
            for char in row:
                compress_txt += codes[char]

    return compress_txt


def save_compress_file(file_name, compressed_txt, codes):
    new_file_name = file_name.replace(".txt", ".bin")
    with open(new_file_name, "wb") as compress_file:
        # Escribir los códigos (diccionario) en el archivo
        compress_file.write(str(codes).encode("utf-8"))

        # Convertir la secuencia binaria en bytes
        remain_bits = len(compressed_txt) % 8
        if remain_bits != 0:
            compressed_txt += "0" * (8 - remain_bits)

        byte_array = bytearray()
        for i in range(0, len(compressed_txt), 8):
            byte_array.append(int(compressed_txt[i : i + 8], 2))

        compress_file.write(bytes(byte_array))


def decompress_file():
    compress_file_path = filedialog.askopenfilename(
        title="Selecciona un archivo de texto",
        filetypes=[("Archivos de texto", "*.bin")],  # Filtra solo archivos .txt
    )

    if not compress_file_path:
        messagebox.showinfo("Error", f"No se ha seleccionado ningún archivo.")
        return

    decompress_txt = decompres(compress_file_path)
    # original_path_name = compress_file_path.replace(".hff.bin", "_descomprimido.txt")
    original_path_name = compress_file_path.replace(".bin", "_descomprimido.txt")
    with open(original_path_name, "w") as archivo:
        archivo.write(decompress_txt)

    messagebox.showinfo("Exito", "Se ha descomprimido correctamente")


# Función para descomprimir el archivo
def decompres(compress_file_path):

    with open(compress_file_path, "rb") as compress_file:
        # Leer los códigos (diccionario) del archivo
        # codigos = pickle.load(compress_file)

        # Leer los datos comprimidos en forma de bytes
        compress_bytes = compress_file.read()

        txt = compress_bytes.decode("utf-8", errors="ignore")

        # Extraer el texto del diccionario (asumiendo que empieza con '{' y termina con '}')
        start = txt.find("{")
        end = txt.rfind("}") + 1  # Asegurar que incluimos el último '}'

        enc_codes = {}

        if start != -1 and end != -1:
            dict_txt = txt[start:end]
            try:
                # Convertir el texto a un diccionario
                enc_codes = eval(dict_txt)
            except Exception as e:
                print("Error al convertir el texto en diccionario:", e)
        else:
            print("No se encontró un diccionario válido en el texto.")

        # Quitar el diccionario del contenido
        compress_bytes = compress_bytes[end:].strip()

        compresed_txt = ""
        for byte in compress_bytes:
            compresed_txt += f"{byte:08b}"

        # Revertir los códigos de Huffman para la descompresión
        invert_codes = {v: k for k, v in enc_codes.items()}

        decompres_txt = ""
        actual_code = ""

        for bit in compresed_txt:
            actual_code += bit
            if actual_code in invert_codes:
                decompres_txt += invert_codes[actual_code]
                actual_code = ""

        return decompres_txt
