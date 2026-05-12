from enum import Enum
from typing import Any

  
class Tile:             #Base class for categorization purposes
    def __init__(self, state: float):
        self.state = state        

class BinaryTile(Tile):
    def __init__(self, state: int):
        super().__init__(state)
        if not isinstance(self.state, int):
            raise ValueError(f'BinaryTile must have an integer state (state: {self.state})')
        if self.state not in {0, 1}:
            raise ValueError(f'BinaryTile must have a state of 0 or 1 (state: {self.state})')
    
    def check_state(self):
        if not isinstance(self.state, int):
            raise ValueError(f'BinaryTile must have an integer state (state: {self.state})')
        if self.state not in {0, 1}:
            raise ValueError(f'BinaryTile must have a state of 0 or 1 (state: {self.state})')

class BinaryCell(BinaryTile):
    def __init__(self, state: int):
        super().__init__(state)

    def __str__(self):
        if self.state == 1:
            return '■'
        else:
            return '.'
    
    # def set_state(self, value: int):
    #     self.state = value
    #     self.check_state()

    def turn_on(self):
        self.state = 1

    def turn_off(self):
        self.state = 0
    
    def flip(self):
        self.state = (self.state + 1) % 2

class BinaryDud(BinaryTile):
    def __init__(self) -> None:
        super().__init__(0)

    def __str__(self):
        return '~'