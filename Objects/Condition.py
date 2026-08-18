from Objects.Cell import Tile, BinaryTile, BinaryCell, BinaryDud
from collections.abc import Callable, Sequence, Iterable
from typing import Generic, TypeVar
from bitmap_operations import *

class Condition:
    def __init__(self, get_state: Callable[[int], int], check_state: Callable[[int], bool]) -> None:
        def met(nbhd: int): # nbhd is the system bitmap "and"-ed with another bitmap
            return check_state(get_state(nbhd))
        
        self.get_state = get_state
        self.check_state = check_state
        self.met = met
        self.valid_num_of_bits = {}

    def __not__(self):
        def not_met(state):
            return not self.check_state(state)
        return Condition(self.get_state, not_met)
    
    def __and__(self, other):
        def both_met(state):
            return self.check_state(state) and other.check_state(state)
        return Condition(self.get_state, both_met)
    
    def __or__(self, other):
        def either_met(state):
            return self.check_state(state) or (other.check_state(state))
        return Condition(self.get_state, either_met)

#Some special conditions:

class CountAliveCells(Condition):
    def __init__(self, check_state: Callable[[int], bool]):
        def sum_of_states(nbhd):
            return sum_bits(bitmap=nbhd)
        super().__init__(get_state=sum_of_states, check_state=check_state)
        self.state_description = 'sum of states'
        self.valid_num_of_bits = {1}

class FalseCondition(CountAliveCells):
    def __init__(self):
        def check_state(state: int) -> bool:
            return False
        super().__init__(check_state)

class HasMoreAlive(CountAliveCells):
    def __init__(self, threshold: int):
        def check_state(alive_cells: int) -> bool:
            return alive_cells > threshold
        super().__init__(check_state)

class HasLessAlive(CountAliveCells):
    def __init__(self, threshold: int):
        def check_state(alive_cells: int) -> bool:
            return alive_cells < threshold
        super().__init__(check_state)

class HasAlive(CountAliveCells):
    def __init__(self, threshold: int):
        def check_state(alive_cells: int) -> bool:
            return alive_cells == threshold
        super().__init__(check_state)
