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

    def __not__(self):
        def not_met(state):
            return not self.met(state)
        return Condition(self.get_state, not_met)
    
    def __and__(self, other):
        def both_met(state):
            return self.met(state) and other.met(state)
        return Condition(self.get_state, both_met)
    
    def __or__(self, other):
        def either_met(state):
            return self.met(state) or (other.met(state))
        return Condition(self.get_state, either_met)

#Some special conditions:

class HasMoreAlive(Condition[BinaryTile, int]):
    def __init__(self, threshold: int):
        def get_state(nbhd: Iterable[BinaryTile]) -> int:
            num_alive = sum([cell.state for cell in nbhd])
            if not isinstance(num_alive, int):
                raise ValueError(f'num_alive must be an integer! Value: {num_alive}')
            return num_alive
        def check_met(state: int) -> bool:
            return state > threshold
        super().__init__(get_state, check_met)

class HasLessAlive(Condition[BinaryTile, int]):
    def __init__(self, threshold: int):
        def get_state(nbhd: Iterable[BinaryTile]) -> int:
            num_alive = sum([cell.state for cell in nbhd])
            if not isinstance(num_alive, int):
                raise ValueError(f'num_alive must be an integer! Value: {num_alive}')
            return num_alive
        def check_met(state: int) -> bool:
            return state < threshold
        super().__init__(get_state, check_met)

class HasAlive(Condition[BinaryTile, int]):
    def __init__(self, threshold: int):
        def get_state(nbhd: Iterable[BinaryTile]) -> int:
            num_alive = sum([cell.state for cell in nbhd])
            if not isinstance(num_alive, int):
                raise ValueError(f'num_alive must be an integer! Value: {num_alive}')
            return num_alive
        def check_met(state: int) -> bool:
            return state == threshold
        super().__init__(get_state, check_met)
