from typing import IO, List, Optional, TypeVar

from afd import Afd
from afd_types import State, Symbol, Transition, Transitions

T = TypeVar("T")


class FileParser():
    def __init__(self, file: Optional[IO]) -> None:
        self.file: Optional[IO] = file.read()
        self.lines = str(self.file).split("\n")

    def process(self) -> Afd:

        return Afd(
            self.__get_name(),
            self.__get_states(),
            self.__get_alphabet(),
            self.__get_initial_state(),
            self.__get_final_states(),
            self.__get_transitions()
        )

    def __get_name(self) -> str:
        return self.lines[0]

    def __get_sublist(self, index) -> str:
        return self.lines[index].split(" ")[1]

    def __get_states(self) -> List[State]:
        state_substr: State = self.__get_sublist(1)
        return FileParser.parse_to_list(state_substr)

    def __get_alphabet(self) -> List[Symbol]:
        symbol_substr: State = self.__get_sublist(2)
        return FileParser.parse_to_list(symbol_substr)

    def __get_initial_state(self) -> State:
        symbol_substr: State = self.__get_sublist(2)
        return symbol_substr[1]

    def __get_final_states(self) -> List[State]:
        state_substr: State = self.__get_sublist(4)
        return FileParser.parse_to_list(state_substr)

    def __get_transitions(self) -> Transitions:
        break_point = self.lines.index("")
        transitions_in_str = self.lines[break_point + 1:]

        return list(
            map
            (lambda s: FileParser.parse_transition(s),
             transitions_in_str)
        )

    @staticmethod
    def parse_to_list(str_list: T) -> List[T]:
        return str_list.split(",")

    @staticmethod
    def parse_transition(transition: str) -> Transition:
        transition.replace("(", "").replace(")", "")
        return tuple(transition.split(","))


if __name__ == "__main__":
    arquivo = open("exemplo.txt", mode="r")
    meu_processador = FileParser(arquivo)
    afd_gerado = meu_processador.process()
    