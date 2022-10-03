import copy
from typing import List, Dict

import pydot

from afd_types import State, Symbol, Transitions, StateGraph, DistinctionTable
from utils import dfs


class Afd:
    # name: str = ""
    # states: List[State] = []
    # alphabet: List[Symbol] = []
    # initial: State = str(None)
    # finals: List[State] = []
    # transitions: Transitions = []

    def __init__(self, name: str, states: List[State], alphabet: List[Symbol],
                 initial: State, finals: List[State], transitions: Transitions):
        self.name = name
        self.states = states
        self.alphabet = alphabet
        self.initial = initial
        self.finals = finals
        self.transitions = transitions

    def __repr__(self) -> str:
        new_line = "\n"
        return f"""
{self.name}
S: {self.states}
A: {self.alphabet}
i: {self.initial}
F: {self.finals}

{new_line.join(map(lambda t: t.__repr__(), self.transitions))}
        """

    def remove_state(self, state: State):
        if state in self.states:
            self.states.remove(state)
        if state in self.finals:
            self.finals.remove(state)
        self.transitions = list(filter(lambda transition: state not in transition, self.transitions))

    # basicamente remove os estados que não são finais e não levam a algum final
    def remove_useless_states(self):
        graph = {}

        # inicializa lista de adjacência
        for state in self.states:
            graph[state] = []
        for transition in self.transitions:
            if transition[2] not in graph[transition[0]]:
                graph[transition[0]].append(transition[2])

        useless_states = []

        # para cada estado
        for state in self.states:
            # se estado for final ignora
            if state in self.finals:
                continue
            # caso contrario inicia dfs partindo desse estado
            visited = set()
            dfs(visited, graph, state)
            # caso nenhum dos visitados pela dfs for final, o estado e inutil
            if not (visited & set(self.finals)):
                useless_states.append(state)
        # remove estados inuteis
        for useless_state in useless_states:
            self.remove_state(useless_state)

    def remove_unreachable_states(self) -> None:
        graph: StateGraph = {}

        # inicializa lista de adjacencia
        for state in self.states:
            graph[state] = []

        for transition in self.transitions:
            if transition[2] not in graph[transition[0]]:
                graph[transition[0]].append(transition[2])

        visited = set()

        # inicia dfs partindo do início
        dfs(visited, graph, self.initial)
        # todos estados não visitados sao considerados inalcancaveis e excluidos
        unreachable_states = list(filter(lambda s: s not in visited, self.states))
        for unreachable_state in unreachable_states:
            self.remove_state(unreachable_state)

    # checa se automato e total
    def check_total(self):
        # para cada estado do afd
        for state in self.states:
            # pega os caracteres das transicoes que tem como origem o estado atual
            filtered = [transition[1] for transition in self.transitions if transition[0] == state]
            # e ve se esses caracteres correspondem à totalidade dos símbolos do alfabeto aceito
            not_included = list(filter(lambda char: char not in filtered, self.alphabet))
            # caso nao o automato e considerado nao total
            if len(not_included) > 0:
                return False
        # caso todos estados passem pelo teste retorna automato total
        return True

    # torna automato total
    def make_total(self):
        DUMP_STATE: State = 'dump'
        # se automato e total retorna
        if self.check_total():
            return
        # se não for total, prosseguimos com sua transformação
        # adiciona estado de dump nos estados do automato
        elif DUMP_STATE not in self.states:
            self.states.append(DUMP_STATE)
        # para cada estado do automato
        for state in self.states:
            # pega os caracteres das transicoes que tem como origem o estado atual
            filtered = [transition[1] for transition in self.transitions if transition[0] == state]
            # e pega todos simbolos do alfabeto que nao estao nessa lista
            not_included = list(filter(lambda symbol: symbol not in filtered, self.alphabet))
            # para cada simbolo nao abrangido por esse estado cria uma transicao que tem como origem ele e o destino
            # o estado de dump
            for char in not_included:
                self.transitions.append((state, char, DUMP_STATE))

    def mark_distinct_table(self, table: DistinctionTable, q1: State, q2: State):
        # para cada celula da tabela de distincao
        for key in table:
            for key_aux in table[key]:
                # se a celula conter o par de estados recebido como parametro
                if (q1, q2) in table[key][key_aux] or (q2, q1) in table[key][key_aux]:
                    # marca a celula como distinta
                    table[key][key_aux] = ['X']
                    # e marca todas as celulas que contem a celula recem marcada
                    self.mark_distinct_table(table, key, key_aux)

    def find_transition(self, origem, caracter):
        # retorna primeira ocorrencia de transicao que contem a origem e o simbolo recebidos como parametro
        # caso ocorrencia nao existir retorna 'invalido'
        return next(
            (transition[2] for transition in self.transitions if transition[0] == origem and transition[1] == caracter),
            'invalido')

    def check_empty_language(self):
        minimized_automata = copy.deepcopy(self)
        # minimiza automato
        minimized_automata.minimize()
        # caso o automato minimo nao tenha nenhum estado retorna True, e vazio, caso contrario retorna False,
        # linguagem nao vazia
        return True if len(minimized_automata.states) == 0 else False

    def make_distict_table(self):
        """
        Monta a tabela triangular de distinção dos estados.
        É arranjada do seguinte modo:
        I s
        I s s
        I s s s
          J J J
        """
        table: DistinctionTable = {}
        column_i = self.states[:-1]  # Pega todos menos o último estado
        line_j = self.states[1:]  # Pega todos menos o primeiro estado

        # inicializa tabela de distincão
        for index in range(len(line_j)):
            table[column_i[index]] = {}
            for aux_state in line_j[index:]:
                # Adiciona o estado da coluna i, e cria uma lista de dependências ligada ao estado da coluna j
                table[column_i[index]][aux_state] = []

        # marca finais != iniciais
        for key in table:
            for key_aux in table[key]:
                if (key in self.finals) != (key_aux in self.finals):
                    table[key][key_aux].append('X')

        # para cada celula da tabela
        for key in table:
            for key_aux in table[key]:
                # caso a celula esteja vazia
                if not table[key][key_aux]:
                    # para cada simbolo do alfabeto
                    for character in self.alphabet:
                        # encontra os estados destino tendo como origem os dois estados que identificam a celula (linha e coluna)
                        destiny_key = self.find_transition(key, character)
                        destiny_key_aux = self.find_transition(key_aux, character)
                        # caso os estados destino sejam iguais ignora
                        if destiny_key == destiny_key_aux:
                            continue
                        # caso a celula esteja com linha e coluna trocadas na tabela,
                        # apenas inverte elas
                        try:
                            table[destiny_key][destiny_key_aux]
                        except:
                            destiny_key, destiny_key_aux = destiny_key_aux, destiny_key

                        # se a celula de destino da tabela estiver marcada
                        if 'X' in table[destiny_key][destiny_key_aux]:
                            # marca a celula atual
                            table[key][key_aux] = ['X']
                            # e marca todas celulas que contenham a celula atual
                            self.mark_distinct_table(table, key, key_aux)
                            break
                        else:
                            # caso contrario, adiciona a celula destino como uma dependencia da celula atual
                            table[key][key_aux].append((destiny_key, destiny_key_aux))

        return table

    def unify_states(self) -> None:
        # cria a tabela de distincao preenchida
        table: DistinctionTable = self.make_distict_table()
        # para cada celula da tabela
        for key in table:
            for key_aux in table[key]:
                # se a celula nao tiver sido marcada como distinta
                if 'X' not in table[key][key_aux]:
                    # assume que os estados que identificam a celula são iguais e cria um estado a partir da
                    # união deles
                    new_state = key + key_aux
                    # troca estados anteriores pela uniao dos mesmos e substitui todas suas ocorrencias no automato
                    self.states = list(filter(lambda state: state != key and state != key_aux, self.states))
                    self.states.append(new_state)
                    if key in self.finals or key_aux in self.finals:
                        self.finals = list(filter(lambda state: state != key and state != key_aux, self.finals))
                        self.finals.append(new_state)
                    if key == self.initial or key_aux == self.initial:
                        self.initial = new_state
                    new_transitions = []
                    for transition in self.transitions:
                        if transition[0] == key or transition[0] == key_aux:
                            transition = (new_state, transition[1], transition[2])
                        if transition[2] == key or transition[2] == key_aux:
                            transition = (transition[0], transition[1], new_state)
                        new_transitions.append(transition)

                    self.transitions = list(dict.fromkeys(new_transitions))

    def minimize(self) -> None:
        # remove estados inalcacaveis do automato
        self.remove_unreachable_states()
        # torna ele total
        self.make_total()
        # unifica estados equivalentes
        self.unify_states()
        # remove estados inuteis
        self.remove_useless_states()

    def print_afd(self) -> None:
        print(f"S: {self.states}")
        print(f"A: {self.alphabet}")
        print(f"i: {self.initial}")
        print(f"F: {self.finals}")
        print("Transicoes:")
        for transition in self.transitions:
            print(transition)

    def validate_word(self, word: str) -> bool:
        state = self.initial

        for char in word:
            state = self.find_transition(state, char)
            if state == 'invalido':
                return False

        return False if state not in self.finals else True

    def validate_words(self, words: List[str]):
        response: Dict[str, bool] = {}

        for word in words:
            response[word] = self.validate_word(word)

        return response

    def generate_graphviz(self, name: str = None) -> None:
        if name is None:
            name = self.name
        # só colar o graph_txt no https://dreampuf.github.io/GraphvizOnline
        graph_txt = f'digraph {{\nranksep=0.5 size=\"8, 8\"\nrankdir=LR\nlabelloc="t"\nlabel={name}\nInitial [label="" fontsize=14.0 shape=point]\n'

        for state in self.states:
            if state in self.finals:
                graph_txt += f'{state} [fontsize=14.0 shape=doublecircle]\n'
            else:
                graph_txt += f'{state} [fontsize=14.0 shape=circle]\n'

        graph_txt += f"Initial -> {self.initial} [arrowsize=0.85]\n"

        for transition in self.transitions:
            graph_txt += f'	{transition[0]} -> {transition[2]} [label=\" {transition[1]} \" arrowsize=0.85 fontsize=14.0]\n'

        graph_txt += '}'
        graph = pydot.graph_from_dot_data(graph_txt)[0]
        graph.write_png(f'./images/{name}.png')
