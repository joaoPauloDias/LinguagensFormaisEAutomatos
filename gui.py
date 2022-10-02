import os.path
import tkinter as tk
from tkinter import filedialog
from typing import IO, List, Optional, Tuple

X = int

Y = int

Coord = Tuple[X, Y]


class FileButton:
    __PAD = 6
    # name: str = "Selecionar o arquivo "
    # label: tk.Label = None
    # button: tk.Button = None
    # master: tk.Tk = None
    # file: Optional[IO] = None
    # update_subject = None

    def __init__(self, name_complement: str, master: tk.Tk, coord: Coord, update_subject):
        self.master = master
        self.name = "Selecionar o arquivo " + name_complement
        self.file: Optional[IO] = None

        self.label = tk.Label(self.master, text=self.name,
                              padx=FileButton.__PAD, pady=FileButton.__PAD)
        self.label.grid(column=coord[1], row=coord[0])

        self.button = tk.Button(
            self.master, text="Carregar", command=self.open_dialog)
        self.button.grid(
            column=coord[1] + 1, row=coord[0], padx=FileButton.__PAD, pady=FileButton.__PAD)

        self.update_subject = update_subject

    def open_dialog(self):
        self.file = filedialog.askopenfile(title=self.name,
                                           initialdir=os.path.expanduser("~"),
                                           filetypes=[("Text files", "*.txt")])
        self.update_subject()


class Gui:
    # window: tk.Tk = None
    # file_afd: FileButton = None
    # file_words: FileButton = None
    # start = None
    # file_subject: List[FileButton] = []

    def __init__(self, start):
        self.start = start
        self.window = tk.Tk()
        self.window.title("Simplificador de Autômatos")
        self.window.geometry("600x400+200+200")
        self.window.iconbitmap(True, "assets/icon.ico")

        # self.file_afd = FileButton("do AFD", self.window, (0, 0), self.update_subject)
        self.file_subject: List[IO] = []
        self.file_afd = self.make_file_btn("do AFD", (0, 0))
        # self.file_words = FileButton("da lista de palavras", self.window, (1, 0), self.update_subject)
        self.file_words = self.make_file_btn("da lista de palavras", (1, 0))

        self.start = tk.Button(self.window, text="Iniciar",
                               state=tk.DISABLED, command=start)
        self.start.grid(column=0, row=2)

        self.window.mainloop()

    def make_file_btn(self, name: str, coord: Coord):
        new_button = FileButton(name, self.window, coord, self.update_subject)
        self.file_subject.append(new_button)
        return new_button

    def file_label(self, complement):
        return f"Selecionar o arquivo do {complement}"

    def update_subject(self):
        enable_start = True

        for observer in self.file_subject:
            enable_start = enable_start and observer.file

        if enable_start:
            self.start["state"] = tk.NORMAL
        else:
            self.start["state"] = tk.DISABLED


if __name__ == "__main__":
    Gui(None)
