from __future__ import annotations

from enum import Enum


class State(str, Enum):
    ENTRY = "entry"
    START = "start"
    ROUTE_MAP = "route_map"
    NODE = "node"
    SETTLEMENT = "settlement"


def next_state(current: State, step: int) -> State:
    if current == State.ENTRY:
        return State.START
    if current == State.START:
        return State.ROUTE_MAP
    if step >= 10:
        return State.SETTLEMENT
    return State.NODE if step % 2 == 0 else State.ROUTE_MAP
