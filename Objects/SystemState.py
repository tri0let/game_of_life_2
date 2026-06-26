from Objects.Cell import Tile, BinaryTile, BinaryCell, BinaryDud
from collections.abc import Callable, Sequence, Iterable
from typing import Any, Generic, TypeVar

StateType = TypeVar('StateType')

class SystemState(Generic[StateType], dict[Any, StateType]):
    def __init__(self, d: dict[Any, StateType]) -> None:
        super().__init__(d)
        self.type = StateType

