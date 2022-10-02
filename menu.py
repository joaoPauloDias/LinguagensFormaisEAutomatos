from file_parser import FileParser


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
