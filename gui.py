import os.path
import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
from typing import IO, Callable, List, Optional, Tuple
# import pyglet

X = int

Y = int

Coord = Tuple[X, Y]


class FileButton:
    __PAD = 7
    # name: str = "Selecionar o arquivo "
    # label: tk.Label = None
    # button: tk.Button = None
    # master: tk.Tk = None
    # file: Optional[IO] = None
    # update_subject = None

    def __init__(self, name_complement: str, master: tk.Tk, coord: Coord, update_subject, style):
        self.master = master
        self.name = "Selecionar o arquivo " + name_complement
        self.file: Optional[IO] = None

        self.label = tk.Label(self.master, text=self.name,
                              padx=FileButton.__PAD, pady=FileButton.__PAD,
                              **style)
        self.label.grid(column=coord[1], row=coord[0])

        self.button = tk.Button(
            self.master, text="Carregar", command=self.open_dialog,
            **style)
        self.button.grid(
            column=coord[1] + 1, row=coord[0], padx=FileButton.__PAD, pady=FileButton.__PAD)

        self.update_subject = update_subject

    def open_dialog(self):
        self.file = filedialog.askopenfile(title=self.name,
                                           filetypes=[("Text files", "*.txt")])
        self.update_subject()


class Gui:
    # window: tk.Tk = None
    # fbtn_afd: FileButton = None
    # fbtn: FileButton = None
    # start = None
    # file_subject: List[FileButton] = []
    __DEFAULT_FONT: Font = None

    DEFAULT_PROPS = {
        "bd": 2,
        "relief": "solid",
        "anchor": tk.W
    }

    def __init__(self, start: Callable[[IO, IO], None]):
        self.start = start
        self.window = tk.Tk()
        self.window.title("Simplificador de Autômatos")
        self.window.geometry("600x400+200+200")
        self.window.iconbitmap(True, "assets/icon.ico")

        Gui.__set_font()

        self.file_subject: List[IO] = []
        self.fbtn_afd = self.make_file_btn("do AFD", (0, 0))
        self.fbtn_words = self.make_file_btn("da lista de palavras", (1, 0))

        self.start_btn = tk.Button(self.window, text="Iniciar",
                                   state=tk.DISABLED, command=self.__gui_start)
        self.start_btn.grid(column=0, row=2)

        self.window.mainloop()

    def __gui_start(self):
        self.start(self.fbtn_afd.file, self.fbtn_words.file)

    def make_file_btn(self, name: str, coord: Coord):
        new_button = FileButton(name, self.window, coord,
                                self.update_subject, Gui.DEFAULT_PROPS)
        self.file_subject.append(new_button)
        return new_button

    def file_label(self, complement):
        return f"Selecionar o arquivo do {complement}"

    def update_subject(self):
        enable_start = True
        cu = r'assets\\fonts\\helvetica-neue\\HelveticaNeue-Regular.otf'
        print(cu)
        for observer in self.file_subject:
            enable_start = enable_start and observer.file

        if enable_start:
            self.start_btn["state"] = tk.NORMAL
        else:
            self.start_btn["state"] = tk.DISABLED

    @staticmethod
    def __set_font():
        Gui.__DEFAULT_FONT = Font(
            family="Verdana",
            size=12,
            weight="normal"
        )

        Gui.DEFAULT_PROPS["font"] = Gui.__DEFAULT_FONT


if __name__ == "__main__":
    Gui(None)
