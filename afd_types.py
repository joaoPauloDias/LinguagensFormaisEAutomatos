import typing

State = str
Symbol = str
DistinctionTable = typing.Dict[State, typing.Dict[State, typing.List[State]]]
Transition = typing.Tuple[State, Symbol, State]
Transitions = typing.List[Transition]
StringList = typing.List[str]
StateGraph = typing.Dict[State, typing.List[typing.Union[State, typing.Tuple[State, State]]]]
