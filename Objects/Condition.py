from Objects.Cell import Tile, BinaryTile, BinaryCell, BinaryDud
from collections.abc import Callable, Sequence, Iterable
from typing import Generic, TypeVar

class Condition:
    def __init__(self, func: Callable[[Iterable], bool]) -> None:
        self.met = func

    def __not__(self):
        def not_met(nbhd):
            return not self.met(nbhd) 
        return Condition(not_met)
    
    def __and__(self, other):
        def both_met(nbhd):
            return self.met(nbhd) and other.met(nbhd)
        return Condition(both_met)
    
    def __or__(self, other):
        def either_met(nbhd):
            return self.met(nbhd) or (other.met(nbhd))
        return Condition(either_met)

#Some special conditions:

class HasMoreAlive(Condition):
    def __init__(self, threshold: int):
        def func(nbhd: Iterable) -> bool:
            num_alive = sum([cell.state for cell in nbhd])
            return num_alive > threshold
        super().__init__(func)

class HasLessAlive(Condition):
    def __init__(self, threshold: int):
        def func(nbhd: Iterable) -> bool:
            num_alive = sum([cell.state for cell in nbhd])
            return num_alive < threshold
        super().__init__(func)

class HasAlive(Condition):
    def __init__(self, threshold: int):
        def func(nbhd: Iterable) -> bool:
            num_alive = sum([cell.state for cell in nbhd])
            return num_alive == threshold
        super().__init__(func)
