from tkinter import filedialog

frequency = {}


class Node:
    def __init__(self, value: int, letter: str = "", left=None, rigth=None):
        self.value = value
        self.letter = letter
        self.next = left
        self.back = rigth

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

    while len(list_frequency) > 1:
        first = list_frequency.pop(0)
        second = list_frequency.pop(0)

        # print([str(obj) for obj in list_frequency])

        if isinstance(first, tuple) and isinstance(second, tuple):
            letter_f, value_f = first
            letter_s, value_s = second

            node_f = Node(value=value_f, letter=letter_f)
            node_s = Node(value=value_s, letter=letter_s)

            node = Node(value=value_f + value_s, left=node_f, rigth=node_s)

            append_list(list_frequency, node)
        elif isinstance(first, tuple) and isinstance(second, Node):
            letter_f, value_f = first

            node_f = Node(value=value_f, letter=letter_f)

            node = Node(value=value_f + second.value, left=node_f, rigth=second)

            append_list(list_frequency, node)
        elif isinstance(first, Node) and isinstance(second, tuple):
            letter_s, value_s = second

            node_s = Node(value=value_s, letter=letter_s)

            node = Node(value=value_s + first.value, left=first, rigth=node_s)

            append_list(list_frequency, node)
        elif isinstance(first, Node) and isinstance(second, Node):
            node = Node(value=first.value + second.value, left=first, rigth=second)

            append_list(list_frequency, node)

    print([str(obj) for obj in list_frequency])


def append_list(list_huffman: list, node: Node):
    flag = False

    for i in range(len(list_huffman) - 1):

        if isinstance(list_huffman[i], tuple) and isinstance(
            list_huffman[i + 1], tuple
        ):
            if list_huffman[i][1] <= node.value < list_huffman[i + 1][1]:
                list_huffman.insert(i, node)
                flag = True
                break
        elif isinstance(list_huffman[i], tuple) and isinstance(
            list_huffman[i + 1], Node
        ):
            if list_huffman[i][1] <= node.value < list_huffman[i + 1].value:
                list_huffman.insert(i, node)
                flag = True
                break
        elif isinstance(list_huffman[i], Node) and isinstance(
            list_huffman[i + 1], tuple
        ):
            if list_huffman[i].value <= node.value < list_huffman[i + 1][1]:
                list_huffman.insert(i, node)
                flag = True
                break
        elif isinstance(list_huffman[i], Node) and isinstance(
            list_huffman[i + 1], Node
        ):
            if list_huffman[i].value <= node.value < list_huffman[i + 1].value:
                list_huffman.insert(i, node)
                flag = True
                break

    if not flag:
        list_huffman.append(node)
