from typing import IO
from file_parser import FileParser
from gui import Gui
from menu import menu
from word_parser import WordParser


def start(file_afd: IO, file_words: IO, gui_i: Gui):
    processed_afd = FileParser(file_afd).process_afd()
    processed_words = WordParser(file_words).process()

    file_afd.seek(0)
    file_words.seek(0)

    print("AFD sem simplificações:")
    print(processed_afd)
    processed_afd.generate_graphviz(f'{processed_afd.name}_not_minimized')

    if processed_afd.check_empty_language():
        print("A linguagem é vazia.")
        gui_i.display_empty()
    else:
        processed_afd.minimize()

        print("AFD com simplificações:")
        print(processed_afd)
        processed_afd.generate_graphviz(f'{processed_afd.name}_minimized')

        valid_word_dict = processed_afd.validate_words(processed_words)
        print("Validade de palavras:")
        print(valid_word_dict)

        gui_i.display_valid(valid_word_dict)


if __name__ == '__main__':
    #     menu(show=True)
    gui = Gui(start)
