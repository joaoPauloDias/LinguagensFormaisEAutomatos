import tkinter as tk
from typing import Tuple

X = int

Y = int

Coord = Tuple[X, Y]


class FileButton():
    PAD = 6
    name: str = "Selecionar o arquivo "
    label: tk.Label = None
    button: tk.Button = None

    def __init__(self, name_complement: str, master, coord: Coord):
        self.name += name_complement
        label = tk.Label(master, text=self.name, padx=FileButton.PAD, pady=FileButton.PAD)
        label.grid(column=coord[1], row=coord[0])

        button = tk.Button(master, text="Carregar")
        button.grid(column=coord[1] + 1, row=coord[0], padx=FileButton.PAD, pady=FileButton.PAD)


class Gui():
    window: tk.Tk = None
    file_afd: FileButton = None
    file_words: FileButton = None
    start = None

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Simplificador de Autômatos")

        self.file_afd = FileButton("do AFD", self.window, (0, 0))
        self.file_words = FileButton("da lista de palavras", self.window, (1, 0))
        self.start = tk.Button(self.window, text="Iniciar")
        self.start.grid(column=0, row=2)

        self.window.mainloop()

    def file_label(self, complement):
        return f"Selecionar o arquivo do {complement}"


if __name__ == "__main__":
    Gui()
