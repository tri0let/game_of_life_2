from Objects.Cell import Tile, BinaryTile, BinaryCell, BinaryDud
from collections.abc import Callable, Sequence, Iterable
from typing import Generic, TypeVar

TileType = TypeVar('TileType')
StateType = TypeVar('StateType')

class Condition(Generic[TileType, StateType]):
    def __init__(self, get_state: Callable[[Iterable[TileType]], StateType], check_state: Callable[[StateType], bool]) -> None:
        def met(nbhd: Iterable[TileType]):
            return check_state(get_state(nbhd))
        
        self.get_state = get_state
        self.check_state = check_state
        self.met = met
        self.state_type = StateType
        self.state_description = 'unknown'

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

class CountAliveCells(Condition[BinaryTile, int]):
    def __init__(self, check_state: Callable[[int], bool]):
        def sum_of_states(nbhd):
            num_alive = sum([cell.state for cell in nbhd])
            if not isinstance(num_alive, int):
                raise ValueError(f'num_alive must be an integer! Value: {num_alive}')
            return num_alive
        super().__init__(get_state=sum_of_states, check_state=check_state)
        self.state_description = 'sum of states'

class FalseCondition(CountAliveCells):
    def __init__(self):
        def check_state(state: int) -> bool:
            return False
        super().__init__(check_state)

class HasMoreAlive(CountAliveCells):
    def __init__(self, threshold: int):
        def check_state(state: int) -> bool:
            return state > threshold
        super().__init__(check_state)

class HasLessAlive(CountAliveCells):
    def __init__(self, threshold: int):
        def check_state(state: int) -> bool:
            return state < threshold
        super().__init__(check_state)

class HasAlive(CountAliveCells):
    def __init__(self, threshold: int):
        def check_state(state: int) -> bool:
            return state == threshold
        super().__init__(check_state)
