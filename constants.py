from Objects.Cell import *
from typing import Callable, Collection


APPLICABLE_STATES: dict[Callable, Collection] = {
    BinaryCell.turn_on: {0},
    BinaryCell.turn_off: {1},
    BinaryCell.flip: {0, 1},
    BinaryCell.id: {0, 1},
}