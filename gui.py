import copy
import os.path
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from tkinter.font import Font
from typing import IO, Callable, Dict, List, Optional, Tuple
# import pyglet

X = int

Y = int

Coord = Tuple[X, Y]


class FileButton:
    __PAD_X = 10
    __PAD_Y = 6
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

        self.label = ctk.CTkLabel(self.master, text=self.name,
                              padx=FileButton.__PAD_X, pady=FileButton.__PAD_Y,
                              justify=tk.LEFT)
        self.label.grid(column=coord[1], row=coord[0], sticky=tk.W)

        self.button = ctk.CTkButton(
            self.master, text="Carregar", command=self.open_dialog)
        self.button.grid(
            column=coord[1] + 1, row=coord[0],
            padx=FileButton.__PAD_X, pady=FileButton.__PAD_Y)

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
        "relief": "solid"
    }

    def __init__(self, start: Callable[[IO, IO], None]):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.start = start
        # self.window = tk.Tk()
        self.window = ctk.CTk()
        self.window.title("Simplificador de Autômatos")
        self.window.geometry("600x400+200+200")
        self.window.iconbitmap(True, "assets/icon.ico")

        Gui.__set_font()

        self.file_subject: List[IO] = []
        self.fbtn_afd = self.make_file_btn("do AFD", (0, 0))
        self.fbtn_words = self.make_file_btn("da lista de palavras", (1, 0))

        self.start_btn = ctk.CTkButton(self.window, text="Iniciar",
                                   state=tk.DISABLED, command=self.__gui_start)
        self.start_btn.grid(row=2, columnspan=2)

        self.window.mainloop()

    def __gui_start(self):
        self.start(self.fbtn_afd.file, self.fbtn_words.file, self)

    def display_empty(self):
        tk.Label(self.window, text="A linguagem gerada é vazia.").grid(
            columnspan=2)

    def display_valid(self, words_dict: Dict[str, bool]):
        ValidWordGui(self.window, words_dict).render()

    def make_file_btn(self, name: str, coord: Coord):
        new_button = FileButton(name, self.window, coord,
                                self.update_subject, Gui.DEFAULT_PROPS)
        self.file_subject.append(new_button)
        return new_button

    def file_label(self, complement):
        return f"Selecionar o arquivo do {complement}"

    def update_subject(self):
        enable_start = True

        for observer in self.file_subject:
            enable_start = enable_start and observer.file

        if enable_start:
            self.start_btn.configure(state=ctk.NORMAL)
        else:
            self.start_btn.configure(state=ctk.DISABLED)

        print(self.start_btn["state"])

    @staticmethod
    def __set_font():
        Gui.__DEFAULT_FONT = Font(
            family="Comic Sans MS",
            size=12,
            weight="normal"
        )

        Gui.DEFAULT_PROPS["font"] = Gui.__DEFAULT_FONT


class ValidWordGui(ctk.CTkFrame):
    def __init__(self, master, valid_words: Dict[str, bool]):
        super().__init__(master)

        self.valid_words = valid_words
        self.grid(columnspan=2)

        self.header_name = "Resultado das palavras"
        self.header = ctk.CTkLabel(self, text=self.header_name)
        self.header.grid(row=0, column=0, padx=10, pady=10)

    def render(self):
        ctk.CTkLabel(self, text="Palavra").grid(column=0, row=1)
        ctk.CTkLabel(self, text="Pertinência").grid(column=1, row=1)

        i = 2
        for key, value in self.valid_words.items():
            ctk.CTkLabel(self, text=key).grid(column=0, row=i)
            ctk.CTkLabel(self, text=ValidWordGui.get_validation(
                value)).grid(column=1, row=i)
            i += 1

    def get_validation(value: bool):
        if value:
            return "Percente"
        else:
            return "Não pertence"


if __name__ == "__main__":
    Gui(None)
