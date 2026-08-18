from collections.abc import Callable

class Outcome:
    def __init__(self, apply_function: Callable, num_bits_per_cell: int) -> None:
        self.apply = apply_function
        self.num_bits = num_bits_per_cell