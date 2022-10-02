from typing import IO
from file_parser import FileParser
from gui import Gui
from menu import menu
from word_parser import WordParser


def start(file_afd: IO, file_words: IO, gui:Gui):
     processed_afd = FileParser(file_afd).process_afd()
     processed_words = WordParser(file_words).process()

     print("AFD sem simplificações:")
     print(processed_afd)
     processed_afd.generate_graphviz(f'{processed_afd.name}_not_minimized')

     if processed_afd.check_empty_language():
          print("A linguagem é vazia.")
          gui.display_empty()
     else:
          processed_afd.minimize()

          print("AFD com simplificações:")
          print(processed_afd)
          processed_afd.generate_graphviz(f'{processed_afd.name}_minimized')

          valid_word_dict = processed_afd.validate_words(processed_words)
          print("Validade de palavras:")
          print(valid_word_dict)

          gui.display_valid(valid_word_dict)



if __name__ == '__main__':
#     menu(show=True)
     gui = Gui(start)

     '''
     M = 'AFDexemplo1'
     S = ['q0', 'q1', 'q2', 'q3']
     A = ['a', 'b']
     i = 'q0'
     F = ['q2', 'q3']
     T = [('q0', 'a', 'q1'), ('q0', 'b', 'q3'), ('q1', 'a', 'q2'), ('q1', 'b', 'q1'), ('q2', 'a', 'q2'),
          ('q3', 'b', 'q2')]
     My_Afd = Afd(M, S, A, i, F, T)

     My_Afd.generate_graphviz(f'{My_Afd.name}_not_minimized')
     My_Afd.minimize()
     My_Afd.generate_graphviz(f'{My_Afd.name}_minimized')

     M = 'AFDexemplo2'
     S = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
     A = ['a', 'b']
     i = 'q0'
     F = ['q0', 'q4', 'q5']
     T = [('q0', 'a', 'q2'), ('q0', 'b', 'q1'), ('q1', 'a', 'q1'), ('q1', 'b', 'q0'), ('q2', 'a', 'q4'),
          ('q2', 'b', 'q5'), ('q3', 'a', 'q5'), ('q3', 'b', 'q4'), ('q4', 'a', 'q3'), ('q4', 'b', 'q2'),
          ('q5', 'a', 'q2'), ('q5', 'b', 'q3')]
     My_Afd = Afd(M, S, A, i, F, T)

     My_Afd.generate_graphviz(f'{My_Afd.name}_not_minimized')
     My_Afd.minimize()
     My_Afd.generate_graphviz(f'{My_Afd.name}_minimized')

     M = 'AFDforno'
     S = ['q0', 'q1', 'q2', 'q3', 'q4']
     A = ['A', 'F', 'C', 'R', 'T', 'Z', 'L']
     i = 'q0'
     F = ['q0', 'q3', 'q4']
     T = [('q0', 'Z', 'q0'), ('q0', 'T', 'q0'), ('q0', 'L', 'q0'), ('q0', 'A', 'q1'), ('q1', 'F', 'q0'),
          ('q1', 'Z', 'q1'), ('q1', 'T', 'q1'), ('q1', 'C', 'q2'), ('q2', 'R', 'q1'), ('q2', 'Z', 'q2'),
          ('q2', 'T', 'q2'), ('q2', 'F', 'q3'), ('q3', 'A', 'q2'), ('q3', 'Z', 'q3'), ('q3', 'T', 'q3'),
          ('q3', 'L', 'q4'), ('q4', 'A', 'q2'), ('q4', 'Z', 'q4'), ('q4', 'T', 'q4'), ('q4', 'L', 'q4')]
     My_Afd = Afd(M, S, A, i, F, T)

     accepted_words_list = ['ACFL', 'ZTACFL', 'LACFLL', 'AZCTFL', 'LZT']
     rejected_words_list = ['AR', 'ACFR', 'F', 'ACA', 'ACL']
     print(My_Afd.validate_words(accepted_words_list))
     print(My_Afd.validate_words(rejected_words_list))

     My_Afd.generate_graphviz(f'{My_Afd.name}_not_minimized')
     My_Afd.minimize()
     My_Afd.generate_graphviz(f'{My_Afd.name}_minimized')
     '''
