from tkinter import filedialog

frequency = {}
dic_encode = {}


class Node:
    def __init__(self, value: int, letter: str = "", left=None, rigth=None):
        self.value = value
        self.letter = letter
        self.left = left
        self.rigth = rigth

    def __str__(self):
        return f"Node({self.value})"


def compress():

    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo de texto",
        filetypes=[("Archivos de texto", "*.txt")],  # Filtra solo archivos .txt
    )

    # Verifica si se ha seleccionado un archivo
    if file_path:
        try:
            with open(file_path, "r") as archivo:
                for row in archivo:
                    row = row.strip()
                    for char in row:
                        if char in frequency:
                            frequency[char] += 1
                        else:
                            frequency[char] = 1

        except Exception as e:
            print(f"Error al leer el archivo: {e}")
    else:
        print("No se ha seleccionado ningún archivo.")

    # conver frequency in tuple
    list_frequency = list(frequency.items())

    # sorted list
    list_frequency = sorted(list_frequency, key=lambda x: x[1])

    # Lista de nodos
    list_nodes = []

    for i in range(len(list_frequency)):
        list_nodes.append(Node(list_frequency[i][1], list_frequency[i][0]))

    while len(list_nodes) > 1:
        first = list_nodes.pop(0)
        second = list_nodes.pop(0)

        # print([str(obj) for obj in list_frequency])
        node = Node(value=first.value + second.value, left=first, rigth=second)

        append_list(list_nodes, node)

    print([str(obj) for obj in list_nodes])


def append_list(list_huffman: list, node: Node):
    flag = False

    for i in range(len(list_huffman) - 1):

        if list_huffman[i].value <= node.value < list_huffman[i + 1].value:
            list_huffman.insert(i, node)
            flag = True
            break

    if not flag:
        list_huffman.append(node)


def encrypt(encode: str, node: Node):
    if node.rigth == None and node.left == None:
        dic_encode = {node.letter, encode}
