from Objects.System import *
from Objects.Cell import *
from Objects.Condition import *
from Objects.Rule import *
from time import sleep

grid = Grid(10, 10, on_init=[(0,0), (0,2), (1,2), (1,1), (2,1)])
grid1 = Grid(10, 10, on_init=0.3)

def nbhd(system: Grid, key: tuple[int, int]):
    nb = []
    i = key[0]
    j = key[1]
    for J in range(j - 1, j + 1 + 1):
        for I in range(i - 1, i + 1 + 1):
            if (I,J) != (i,j):
                nb.append(system[(I % len(system.xrange()), J % len(system.yrange()))])
    return nb

r1 = Rule(nbhd, HasLessAlive(2), BinaryCell.turn_off)
r2 = Rule(nbhd, HasMoreAlive(3), BinaryCell.turn_off)
r3 = Rule(nbhd, HasAlive(3), BinaryCell.turn_on)

rs = RuleSet([r1, r2, r3])

t = 100

while t > 0:
     grid.display()
     rs.apply(grid)
     sleep(0.1)
     t -= 1
