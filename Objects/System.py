from random import random
from Objects.Cell import Tile, BinaryTile, BinaryCell, BinaryDud
from typing import Any, Generic, TypeVar


class System(dict[Any, Any]):

    def __init__(self, keys: list[Any], tiles: list, tile_type: type, cell_type: type) -> None:
        if len(set(keys)) < len(tiles):
            raise ValueError('There must a unique key for every tile!')
        if len(set(keys)) > len(tiles):
            raise ValueError('There must be a tile for every unique key!')
        for tile in tiles:
            if not isinstance(tile, tile_type):
                raise ValueError('All tiles must be of the same type!')
        super().__init__(zip(keys, tiles))
        
        self.tile_type = tile_type
        self.cell_type = cell_type
    
    @property
    def zone(self) -> dict:
        return {k: c for k, c in self.items() if isinstance(c, self.cell_type)}

class Grid(System):
    def __init__(self, width: int=10, height: int=10, border_width: int=1, on_init: list|float=[], loop: bool=True):        
        self.bw = border_width

        xrange0 = range(-self.bw, width + self.bw)
        yrange0 = range(-self.bw, height + self.bw)

        keys = [(i,j) for i in xrange0 for j in yrange0]
        active_keys0 = [(i,j) for i in xrange0 if 0 <= i < width for j in yrange0 if 0 <= j < height]

        cells = []

        if isinstance(on_init, float):
            for i in xrange0:
                for j in yrange0:
                    if (i,j) in active_keys0:
                        cells.append(BinaryCell(on_init > random()))
                    else: cells.append(BinaryDud())
        elif isinstance(on_init, list):
            for i in xrange0:
                for j in yrange0:
                    if (i,j) not in active_keys0:
                        cells.append(BinaryDud())
                    elif (i,j) in on_init:
                        cells.append(BinaryCell(1))
                    else:
                        cells.append(BinaryCell(0))
        else:
            raise ValueError("on_init must be a float or a list of tuples!")
        
        super().__init__(keys, cells, BinaryTile, BinaryCell)
    
    def xrange(self, IncludeBorder: bool=False):
        return sorted({i for (i,j), c in self.items() if IncludeBorder or not isinstance(c, BinaryDud)})
    
    def yrange(self, IncludeBorder: bool=False):
        return sorted({j for (i,j), c in self.items() if IncludeBorder or not isinstance(c, BinaryDud)})

    def __str__(self):
        return str([[str(self[(i,j)].state) for i in self.xrange()] for j in self.yrange()])
    
    def display(self, DisplayBorder: bool=True):
        for j in self.yrange(IncludeBorder=DisplayBorder):
            for i in self.xrange(IncludeBorder=DisplayBorder):
                if i == max(self.xrange(IncludeBorder=DisplayBorder)):
                    print(self[(i,j)])
                else:
                    print(f'{self[(i,j)]} ', end='')
        
        print('=' * 50)
    
    def nbhd(self, i: int, j: int, radius: int=1, exclude_center: bool=True):
        nb = []
        for J in range(j - radius, j + radius + 1):
            for I in range(i - radius, i + radius + 1):
                if not exclude_center or (I,J) != (i,j):
                    nb.append(self[(I,J)])
        return nb
    
    def check(self):
        #Check the grid is the correct data structure
        if not isinstance(self, dict):
            raise ValueError('This grid is somehow not a dictionary!')
        for key, cell in self.items():
            if not isinstance(cell, BinaryTile):
                raise ValueError(f'Non-BinaryTile object in the grid: {cell}')
            if not isinstance(key, tuple):
                raise ValueError(f'Non-tuple object in keys: {key}')
            if not isinstance(key[0], int) or not isinstance(key[1], int):
                raise ValueError(f'Non-int tuple in keys: {key}')
            
        #Check the actual dimensions match the stored dimensions (I think this might be useless
        # because xrange and yrange update themselves):
        actual_xmax = max({i for (i,j) in self.keys()})
        actual_ymax = max({j for (i,j) in self.keys()})
        actual_xmin = min({i for (i,j) in self.keys()})
        actual_ymin = min({j for (i,j) in self.keys()})

        if max(self.xrange(True)) != actual_xmax:
            raise ValueError(f'Actual xmax ({actual_xmax}) doesn\'t match stored xmax ({max(self.xrange(True))})')
        if max(self.yrange(True)) != actual_ymax:
            raise ValueError(f'Actual ymax ({actual_ymax}) doesn\'t match stored ymax ({max(self.yrange(True))})')
        if min(self.xrange(True)) != actual_xmin:
            raise ValueError(f'Actual xmin ({actual_xmin}) doesn\'t match stored xmin ({min(self.xrange(True))})')
        if min(self.yrange(True)) != actual_ymin:
            raise ValueError(f'Actual ymin ({actual_ymin}) doesn\'t match stored ymin ({min(self.yrange(True))})')
        
        #Check the grid is a rectangle
        for i in self.xrange(True):
            for j in self.xrange(True):
                if (i,j) not in self.keys():
                    raise ValueError(f'The grid is not rectangular: {(i,j)} is empty')
        
        #Check if the border width is correct
        border = [key for key, cell in self.items() if isinstance(cell, BinaryDud)]

        theoretical_border_num = (
            (max(self.xrange(True)) - min(self.xrange(True)) + 1) *
            (max(self.yrange(True)) - min(self.yrange(True)) + 1) -
            (max(self.xrange(True)) - min(self.xrange(True)) + 1 - 2 * self.bw) *
            (max(self.yrange(True)) - min(self.yrange(True)) + 1 - 2 * self.bw)
        )
        
        if len(border) != theoretical_border_num:
            raise ValueError(f'The border doesn\'t have the correct shape! \nActual: {len(border)}\nExpected: {theoretical_border_num}')


