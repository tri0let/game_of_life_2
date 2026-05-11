from enum import Enum

class State(Enum):
    OFF = 0
    ON = 1

    def __str__(self):
        return self.name
    
    def __add__(self, other):
        return State((self.value + other.value) % 2)
    
    def __mul__(self, other):
        return State(self.value * other.value)

class Cell:
    def __init__(self, state: State):
        self.state = state

    def __str__(self):
        if self.state == State.ON:
            return '■'
        else:
            return '.'

class Dud:
    def __init__(self):
        pass
    def __str__(self):
        return '~'