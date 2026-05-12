from Objects.Cell import Tile, BinaryTile, BinaryCell, BinaryDud
from collections.abc import Callable, Sequence, Iterable
from typing import Generic, TypeVar

TileType = TypeVar('TileType')

class Condition(Generic[TileType]):
    def __init__(self, func: Callable[[Iterable[TileType]], bool]) -> None:
        self.met = func

#Some special conditions:

def HasMoreAlive(threshold: int, nbhd: Iterable[BinaryTile]) -> bool:
    num_alive = sum([cell.state for cell in nbhd])
    return num_alive > threshold
