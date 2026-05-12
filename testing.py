from Objects.Cell import *
from Objects.System import *
from Objects.Rule import *
from Objects.Condition import *


g = Grid(width=4, height=4, border_width=1, on_init=[(0,0), (1,1), (1,0)])

g.display()

g.check()

for c in g.zone.values():
    c.flip()

g.display()

def nbhd(system: Grid, key: tuple[int, int]):
        nb = []
        i = key[0]
        j = key[1]
        for J in range(j - 1, j + 1 + 1):
            for I in range(i - 1, i + 1 + 1):
                if (I,J) != (i,j):
                    nb.append(system[(I,J)])
        return nb


cond = Condition[BinaryTile](lambda nbhd: HasMoreAlive(5, nbhd))

r = Rule[Grid, BinaryTile, BinaryCell](nbhd, cond, BinaryCell.flip)

r.apply(g)

g.display()





