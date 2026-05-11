from random import random
from Objects.Cell import State, Cell, Dud


class Grid(dict):
    def __init__(self, width: int=10, border_width: int=1, height: int=10, on_init=[], loop=True):
        self.bw = border_width
    
        # self.min_x = -self.bw
        # self.max_x = width + self.bw - 1
        # self.min_y = -self.bw
        # self.max_y = height + self.bw - 1

        # self.xrange = range(self.min_x, self.max_x + 1, 1)
        # self.yrange = range(self.min_y, self.max_y + 1, 1)

        # self.active_xrange = range(width)
        # self.active_yrange = range(height)

        # keys = [(i,j) for i in self.xrange for j in self.yrange]

        # self.active_keys = [(i,j) for i in self.xrange if 0 <= i < width for j in self.yrange if 0 <= j < height]

        xrange0 = range(-self.bw, width + self.bw)
        yrange0 = range(-self.bw, height + self.bw)

        keys = [(i,j) for i in xrange0 for j in yrange0]
        active_keys0 = [(i,j) for i in xrange0 if 0 <= i < width for j in yrange0 if 0 <= j < height]

        values = []

        if isinstance(on_init, float):
            for i in xrange0:
                for j in yrange0:
                    if (i,j) in active_keys0:
                        values.append(Cell(State(on_init > random())))
                    else: values.append(Dud())
        elif isinstance(on_init, list):
            for i in xrange0:
                for j in yrange0:
                    if (i,j) not in active_keys0:
                        values.append(Dud())
                    elif (i,j) in on_init:
                        values.append(Cell(State.ON))
                    else:
                        values.append(Cell(State.OFF))
        else:
            raise ValueError("on_init must be a float or a list of tuples!")
        super().__init__(zip(keys, values))

    @property
    def min_x(self):
        return min([i for (i,j) in self.keys()])
    
    @property
    def max_x(self):
        return max([i for (i,j) in self.keys()])
    
    @property
    def min_y(self):
        return min([j for (i,j) in self.keys()])
    
    @property
    def max_y(self):
        return max([j for (i,j) in self.keys()])
    
    @property
    def xrange(self):
        return range(self.min_x, self.max_x + 1)
    
    @property
    def yrange(self):
        return range(self.min_y, self.max_y + 1)
    
    @property
    def zone_keys(self):
        return {(i,j) for (i,j) in self.keys() if not isinstance(self[(i,j)], Dud)}
    
    @property
    def zone(self):
        return [self[k] for k in self.zone_keys]

    @property
    def z_min_x(self):
        return min([i for (i,j) in self.zone_keys])
    
    @property
    def z_max_x(self):
        return max([i for (i,j) in self.zone_keys])
    
    @property
    def z_min_y(self):
        return min([j for (i,j) in self.zone_keys])
    
    @property
    def z_max_y(self):
        return max([j for (i,j) in self.zone_keys])
    
    @property
    def z_xrange(self):
        return range(self.z_min_x, self.z_max_x + 1)
    
    @property
    def z_yrange(self):
        return range(self.z_min_y, self.z_max_y + 1)

    def __str__(self):
        return str([[str(self[(i,j)].state) for i in self.z_xrange] for j in self.z_yrange])
    
    def display(self):
        for j in self.yrange:
            for i in self.xrange:
                if i == self.max_x:
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


