def dfs(visited, graph, node):  # function for dfs
    if node not in visited:
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)


class Afd:
    states = []
    alphabet = []
    initial = None
    finals = []
    transitions = []

    def __init__(self, states, alphabet, initial, finals, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial = initial
        self.finals = finals
        self.transitions = transitions

    def remove_state(self, state):
        if state in self.states:
            self.states.remove(state)
        if state in self.finals:
            self.finals.remove(state)
        self.transitions = list(filter(lambda transition: state not in transition, self.transitions))

    def remove_useless_states(self):
        graph = {}
        for state in self.states:
            graph[state] = []
        for transition in self.transitions:
            if transition[2] not in graph[transition[0]]:
                graph[transition[0]].append(transition[2])
        useless_states = []
        for state in self.states:
            if state in self.finals:
                continue
            visited = set()
            dfs(visited, graph, state)
            if not (visited & set(self.finals)):
                useless_states.append(state)
        for useless_state in useless_states:
            self.remove_state(useless_state)

    def remove_unreachable_states(self):
        graph = {}
        for state in self.states:
            graph[state] = []
        for transition in self.transitions:
            if transition[2] not in graph[transition[0]]:
                graph[transition[0]].append(transition[2])

        visited = set()
        dfs(visited, graph, self.initial)
        unreachable_states = list(filter(lambda state: state not in visited, self.states))
        for unreachable_state in unreachable_states:
            self.remove_state(unreachable_state)

    def check_total(self):
        for state in self.states:
            filtered = [tup[1] for tup in self.transitions if tup[0] == state]
            not_included = list(filter(lambda char: char not in filtered, self.alphabet))
            if len(not_included) > 0:
                return False
        return True

    def make_total(self):
        if self.check_total():
            return
        if 'dump' not in self.states:
            self.states.append('dump')
        for state in self.states:
            filtered = [tup[1] for tup in self.transitions if tup[0] == state]
            not_included = list(filter(lambda char: char not in filtered, self.alphabet))
            for char in not_included:
                self.transitions.append((state, char, 'dump'))

    def check_distinct_table(self, table, q1, q2):
        for key in table:
            for key_aux in table[key]:
                if (q1, q2) in table[key][key_aux] or (q2, q1) in table[key][key_aux]:
                    table[key][key_aux] = ['X']
                    self.check_distinct_table(table, key, key_aux)

    def find_transition(self, origem, caracter):
        return next(
            (transition[2] for transition in self.transitions if transition[0] == origem and transition[1] == caracter),
            'invalido')

    def make_distict_table(self):
        table = {}
        column_i = self.states[:-1]
        column_j = self.states[1:]
        # montar tabela
        for i in range(len(column_j)):
            table[column_i[i]] = {}
            for aux_state in column_j[i:]:
                table[column_i[i]][aux_state] = []
        # marcar finais != iniciais

        for key in table:
            for key_aux in table[key]:
                if (key in self.finals) != (key_aux in self.finals):
                    table[key][key_aux].append('X')

        for key in table:
            for key_aux in table[key]:
                if not table[key][key_aux]:
                    for character in self.alphabet:
                        destiny_key = self.find_transition(key, character)
                        destiny_key_aux = self.find_transition(key_aux, character)
                        if destiny_key == destiny_key_aux:
                            continue
                        try:
                            table[destiny_key][destiny_key_aux]
                        except:
                            destiny_key, destiny_key_aux = destiny_key_aux, destiny_key

                        if 'X' in table[destiny_key][destiny_key_aux]:
                            # print(f'X: {(destiny_key, destiny_key_aux)} - {(key, key_aux)}')
                            table[key][key_aux] = ['X']
                            self.check_distinct_table(table, key, key_aux)
                            break
                        else:
                            # print(f'Append: {(destiny_key, destiny_key_aux)} - {table[destiny_key][destiny_key_aux]}')
                            table[key][key_aux].append((destiny_key, destiny_key_aux))
        return table

    def unify_states(self):
        table = self.make_distict_table()
        for key in table:
            for key_aux in table[key]:
                if 'X' not in table[key][key_aux]:
                    newState = key + key_aux
                    self.states = list(filter(lambda state: state != key and state != key_aux, self.states))
                    self.states.append(newState)
                    if key in self.finals or key_aux in self.finals:
                        self.finals = list(filter(lambda state: state != key and state != key_aux, self.finals))
                        self.finals.append(newState)
                    if key == self.initial or key_aux == self.initial:
                        self.initial = newState
                    new_transitions = []
                    for transition in self.transitions:
                        if transition[0] == key or transition[0] == key_aux:
                            transition = (newState, transition[1], transition[2])
                        if transition[2] == key or transition[2] == key_aux:
                            transition = (transition[0], transition[1], newState)
                        new_transitions.append(transition)
                    self.transitions = list(dict.fromkeys(new_transitions))

    def minimize(self):
        self.remove_unreachable_states()
        self.make_total()
        self.unify_states()
        self.remove_useless_states()

    def generate_graphviz(self):
        # só colar a string gerada no https://dreampuf.github.io/GraphvizOnline
        graph = 'digraph {\nranksep=0.5 size=\"8, 8\"\nrankdir=LR\nInitial [label="" fontsize=14.0 shape=point]\n'
        for state in self.states:
            if state in self.finals:
                graph += f'{state} [fontsize=14.0 shape=doublecircle]\n'
            else:
                graph += f'{state} [fontsize=14.0 shape=circle]\n'
        graph += f"Initial -> {self.initial} [arrowsize=0.85]\n"
        for transition in self.transitions:
            graph += f'	{transition[0]} -> {transition[2]} [label=\" {transition[1]} \" arrowsize=0.85 fontsize=14.0]\n'
        graph += '}'
        print(graph)


if __name__ == '__main__':
    S = ['q0', 'q1', 'q2', 'q3']
    A = ['a', 'b']
    i = 'q0'
    F = ['q2', 'q3']
    T = [('q0', 'a', 'q1'), ('q0', 'b', 'q3'), ('q1', 'a', 'q2'), ('q1', 'b', 'q1'), ('q2', 'a', 'q2'),
         ('q3', 'b', 'q2')]
    My_Afd = Afd(S, A, i, F, T)
    My_Afd.minimize()
    My_Afd.generate_graphviz()

    S = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
    A = ['a', 'b']
    i = 'q0'
    F = ['q0', 'q4', 'q5']
    T = [('q0', 'a', 'q2'), ('q0', 'b', 'q1'), ('q1', 'a', 'q1'), ('q1', 'b', 'q0'), ('q2', 'a', 'q4'),
         ('q2', 'b', 'q5'), ('q3', 'a', 'q5'), ('q3', 'b', 'q4'), ('q4', 'a', 'q3'), ('q4', 'b', 'q2'),
         ('q5', 'a', 'q2'), ('q5', 'b', 'q3')]
    My_Afd = Afd(S, A, i, F, T)
    My_Afd.minimize()
