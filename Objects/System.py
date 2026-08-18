from random import random, randint
from typing import Any, Sequence
from time_debug import timer

class System:
    def __init__(self, keys: Sequence[Any], cell_bitmap: int=0, num_bits_per_cell: int=1) -> None:

        if not isinstance(cell_bitmap, int):
            raise TypeError(f'cell_bitmap must be an integer. Value: {cell_bitmap}')
        if cell_bitmap < 0: 
            raise ValueError(f'cell_bitmap must be non-negative. Value: {cell_bitmap}')
        if not isinstance(keys, Sequence):
            raise TypeError(f'keys must be an ordered collection. Value: {keys}')
        if not isinstance(num_bits_per_cell, int):
            raise TypeError(f'num_bits_per_cell must be an integer. Value: {num_bits_per_cell}')

        if cell_bitmap >= (1 << num_bits_per_cell) << (len(keys) - 1):
            raise ValueError(f'Not enough keys to support the bitmap: {cell_bitmap} vs. {(1 << num_bits_per_cell) << (len(keys) - 1)}')
        for key in keys:
            if keys.count(key) > 1:
                raise ValueError(f'Duplicate key: {key}')

        self.keys = keys
        self.bitmap = cell_bitmap
        self.num_bits_per_cell = num_bits_per_cell

    def set_bitmap(self, new_bitmap: int):
        if new_bitmap >= (1 << self.num_bits_per_cell) << (len(self.keys) - 1):
            raise ValueError('Not enough keys to support the new bitmap!')
        self.bitmap = new_bitmap

    def get_value(self, bit_position: int) -> int:
        if bit_position >= len(self.keys):
            raise ValueError(f'Bit position too large: {bit_position}')
        return (self.bitmap >> (bit_position * self.num_bits_per_cell)) & ((1 << self.num_bits_per_cell) - 1)

    def index_value(self, key) -> int:
        bit_position = self.keys.index(key)
        return self.get_value(bit_position)
                

class Grid(System):
    def __init__(self, width: int=10, height: int=10):

        keys = [(i,j) for i in range(width) for j in range(height)]

        super().__init__(keys=keys, cell_bitmap=0, num_bits_per_cell=1)
        
        self.keys = keys
        self.num_cells = len(self.keys)
        self.width = width
        self.height = height
        self.xrange = sorted({i for (i,j) in self.keys})
        self.yrange = sorted({j for (i,j) in self.keys})
    
    def __str__(self):
        return str([[str(self.index_value((i,j))) for i in self.xrange] for j in self.yrange])

    def initialize_random(self, on_fraction: float) -> None:
        new_bitmap = 0
        for key in self.keys:
            new_bitmap <<= 1
            new_bitmap += randint(0, 1)
    
    @timer
    def display(self, bitmap=-1, border_width: int=1) -> None:
        grid_str = ''

        grid_str += '=' * (self.width + 2 * border_width + 5) * 2 + '\n'
        grid_str += ('~ ' * (self.width + border_width * 2) + '\n') * border_width + '~ ' * border_width

        if bitmap < 0:
            bitmap = self.bitmap
        bitmap_remaining = bitmap
        counter = 0

        while counter < len(self.keys):
            cell_state = bitmap_remaining & 1
            if cell_state:
                grid_str += '■ '
            else:
                grid_str += '. '
            bitmap_remaining >>= 1
            counter += 1
            if counter % self.width == 0:
                grid_str += '~ ' * border_width + '\n' + '~ ' * border_width

        if border_width: grid_str += '~ ' * (self.width + border_width)
        grid_str += ('\n' + '~ ' * (self.width + border_width * 2)) * (border_width - 1)
        
        print(grid_str)
    
    def check(self):
        #Check the grid is the correct data structure
            
        #Check the actual dimensions match the stored dimensions (I think this might be useless
        # because xrange and yrange update themselves):
        
        #Check the grid is a rectangle
        
        #Check if the border width is correct

        print('TODO: implement the check() function')


