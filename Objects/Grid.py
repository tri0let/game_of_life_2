from random import random
from Objects.Cell import State, Cell, Dud


class Grid(dict):
    def __init__(self, width: int=10, border_width: int=1, height: int=10, on_init=[], loop=True):
        self.bw = border_width

        self.min_x = -self.bw
        self.max_x = width + self.bw - 1
        self.min_y = -self.bw
        self.max_y = height + self.bw - 1

        self.xrange = range(self.min_x, self.max_x + 1, 1)
        self.yrange = range(self.min_y, self.max_y + 1, 1)

        self.active_xrange = range(width)
        self.active_yrange = range(height)

        keys = [(i,j) for i in self.xrange for j in self.yrange]

        self.active_keys = [(i,j) for i in self.xrange if 0 <= i < width for j in self.yrange if 0 <= j < height]

        values = []

        if isinstance(on_init, float):
            for i in self.xrange:
                for j in self.yrange:
                    if (i,j) in self.active_keys:
                        values.append(Cell(State(on_init > random())))
                    else: values.append(Dud())
        elif isinstance(on_init, list):
            for i in self.xrange:
                for j in self.yrange:
                    if (i,j) not in self.active_keys:
                        values.append(Dud())
                    elif (i,j) in on_init:
                        values.append(Cell(State.ON))
                    else:
                        values.append(Cell(State.OFF))
        else:
            raise ValueError("on_init must be a float or a list of tuples!")
        super().__init__(zip(keys, values))

    def __str__(self):
        return str([[str(self[(i,j)].state) for i in self.active_xrange] for j in self.active_yrange])
    
    def display(self):
        for j in self.yrange:
            for i in self.xrange:
                if i == self.max_x:
                    print(self[(i,j)])
                else:
                    print(f'{self[(i,j)]} ', end='')
        
        print('=========================================')
    
    def nbhd(self, i: int, j: int, radius: int=1, exclude_center: bool=True):
        nb = []
        for I in range(i - radius, i + radius + 1):
            for J in range(j - radius, j + radius + 1):
                if not exclude_center or (I,J) != (i,j):
                    nb.append(self[(i,j)])
        return nb


