import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from typing import IO, Dict, List, Optional, Tuple

import customtkinter as ctk

X = int

Y = int

Coord = Tuple[X, Y]


class FileButton:
    __PAD_X = 30

    def __init__(self, name_complement: str, master: tk.Tk, coord: Coord, update_subject):
        self.master = master
        self.name = "Selecionar o arquivo " + name_complement
        self.file: Optional[IO] = None

        self.label = ctk.CTkLabel(self.master, text=self.name,
                                  padx=FileButton.__PAD_X, pady=Gui.PAD_Y,
                                  justify=tk.LEFT)
        self.label.grid(column=coord[1], row=coord[0], sticky=tk.W)

        self.button = ctk.CTkButton(
            self.master, text="Carregar", command=self.open_dialog)
        self.button.grid(
            column=coord[1] + 1, row=coord[0],
            padx=FileButton.__PAD_X, pady=Gui.PAD_Y)

        self.update_subject = update_subject

    def open_dialog(self):
        self.file = filedialog.askopenfile(title=self.name,
                                           filetypes=[("Text files", "*.txt")])
        self.update_subject()


class Gui:
    PAD_Y = 12

    def __init__(self, start):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.start = start

        self.window = ctk.CTk()
        self.window.resizable(False, True)
        self.window.title("Simplificador de Autômatos")
        self.window.geometry("500x500+200+200")
        self.window.columnconfigure(0, weight=1)
        self.window.iconbitmap(True, "assets/icon.ico")

        self.file_subject: List[FileButton] = []
        self.fbtn_afd = self.make_file_btn("do AFD", (0, 0))
        self.fbtn_words = self.make_file_btn("da lista de palavras", (1, 0))

        self.start_btn = ctk.CTkButton(self.window, text="Iniciar",
                                       state=tk.DISABLED, command=self.__gui_start)
        self.start_btn.grid(row=2, columnspan=2)

        self.result = None

        self.window.mainloop()

    def __gui_start(self):
        self.start(self.fbtn_afd.file, self.fbtn_words.file, self)

    def display_empty(self):
        try:
            self.result.grid_remove()
        finally:
            self.result = ctk.CTkLabel(self.window, text="A linguagem gerada é vazia.")
            self.result.grid(columnspan=2, pady=Gui.PAD_Y)

    def display_valid(self, words_dict: Dict[str, bool]):
        try:
            self.result.grid_remove()
        finally:
            self.result = ValidWordGui(self.window, words_dict)
            self.result.render()

    def make_file_btn(self, name: str, coord: Coord):
        new_button = FileButton(name, self.window, coord,
                                self.update_subject)
        self.file_subject.append(new_button)
        return new_button

    @staticmethod
    def file_label(complement):
        return f"Selecionar o arquivo do {complement}"

    def update_subject(self):
        enable_start = True

        for observer in self.file_subject:
            enable_start = enable_start and observer.file

        if enable_start:
            self.start_btn.configure(state=ctk.NORMAL)
        else:
            self.start_btn.configure(state=ctk.DISABLED)


class ValidWordGui(ctk.CTkFrame):
    def __init__(self, master, valid_words: Dict[str, bool]):
        super().__init__(master)

        self.valid_words = valid_words
        self.grid(columnspan=2, pady=Gui.PAD_Y)

        self.table = ttk.Treeview(self, columns=(1, 2), show="headings", height=15)
        self.table.grid()

        self.table.column(1, anchor=tk.CENTER)
        self.table.column(2, anchor=tk.CENTER)

        self.table.heading(1, text="Palavra")
        self.table.heading(2, text="Pertinência")

        self.scrollbar = ctk.CTkScrollbar(self, command=self.table.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.table.configure(yscrollcommand=self.scrollbar.set)

    def render(self):
        for result in self.valid_words.items():
            self.table.insert("", "end", values=(result[0], ValidWordGui.get_validation(result[1])))
        pass

    @staticmethod
    def get_validation(value: bool):
        if value:
            return "Percente"
        else:
            return "Não pertence"


if __name__ == "__main__":
    gui = Gui(None)
