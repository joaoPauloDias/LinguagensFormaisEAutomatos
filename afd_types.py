import typing

State = str
Symbol = str
DistinctionTable = typing.Dict[State, typing.Dict[State, typing.List[State]]]
Transitions = typing.List[typing.Tuple[State, Symbol, State]]
StringList = typing.List[str]
StateGraph = typing.Dict[State, typing.List[State]]
