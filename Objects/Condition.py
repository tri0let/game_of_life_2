from Objects.Cell import Tile, BinaryTile, BinaryCell, BinaryDud
from collections.abc import Callable, Iterable

class Condition:
    def __init__(self, func: Callable[[Iterable[Tile]], bool]) -> None:
        self.met = func

#Some special conditions:

def HasMoreAlive(threshold: int, nbhd: Iterable[BinaryTile]) -> bool:
    num_alive = sum([cell.state for cell in nbhd])
    return num_alive > threshold
