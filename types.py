from typing import Dict, List, Tuple

State = str
Symbol = str
DistinctionTable = Dict[State, Dict[State, List[State]]]
Transitions = List[Tuple[State, Symbol, State]]
StringList = List[str]
StateGraph = Dict[State, List[State]]
