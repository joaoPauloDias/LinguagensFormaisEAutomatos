from afd import Afd
from file_parser import FileParser
from gui import Gui


def show_options():
    options = ["Sair", "Abrir automato", "Processar lista de palavras", "Minimizar automato",
               "Checar se linguagem é vazia",
               "Gerar imagem do automato", "Exibir automato"]
    for i in range(len(options)):
        print(f'{i + 1} - {options[i]}')


def menu(afd=None, words=None, show=False):
    if show:
        show_options()
    user_entry = input("Digite sua opção:\n")

    if user_entry == '1':  # Sair
        return
    elif user_entry == '2':  # Abrir automato
        file_location = input("Digite local do arquivo .txt do afd\n")
        try:
            arquivo = open(file_location, mode="r")
            my_parser = FileParser(arquivo)
            afd = my_parser.process_afd()
            print("AFD carregado com sucesso")
        except:
            print("Erro ao carregar arquivo")
    elif user_entry == '3':  # Processar lista de palavras
        if afd is None:
            print("Afd não carregado")
        else:
            file_location = input("Digite local do arquivo .txt da lista de palavras\n")
            try:
                arquivo = open(file_location, mode="r")
                my_parser = FileParser(arquivo)
                words = my_parser.process_words()
                response = afd.validate_words(words)
                for word in response:
                    response_string = "valido" if response[word] == True else "invalido"
                    print(f'{word} - {response_string}')
            except:
                print("Erro ao carregar arquivo")
    elif user_entry == '4':  # Minimizar automato
        if afd is None:
            print("Afd não carregado")
        else:
            afd.minimize()
            print("Afd minimizado com sucesso")
    elif user_entry == '5':  # Checar se linguagem é vazia
        if afd is None:
            print("Afd não carregado")
        else:
            if afd.check_empty_language() is True:
                print("Linguagem vazia")
            else:
                print("Linguagem não vazia")
    elif user_entry == '6':  # Gerar imagem do automato
        if afd is None:
            print("Afd não carregado")
        else:
            png_name = input("Digite o nome que deseja dar para o arquivo (nao coloque a extensao):\n")
            afd.generate_graphviz(png_name)
    elif user_entry == '7':  # Exibir automato
        if afd is None:
            print("Afd não carregado")
        else:
            afd.print_afd()
    else:
        print("Opcao invalida")
    menu(afd, words, False)


if __name__ == '__main__':
    menu(show=True)
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
