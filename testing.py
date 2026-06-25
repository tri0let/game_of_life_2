from Objects.Cell import *
from Objects.System import *
from Objects.Rule import *
from Objects.Condition import *
from time import sleep


g = Grid(width=4, height=4, border_width=1, on_init=[(0,0), (1,1), (1,0)])
g1 = Grid(width=10, height=10, on_init=0.4)

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
                nb.append(system[(I % len(system.xrange()), J % len(system.yrange()))])
    return nb



r1 = Rule(nbhd, HasLessAlive(10) or HasMoreAlive(0), BinaryCell.turn_off)
r2 = Rule(nbhd, HasMoreAlive(3), BinaryCell.id)


rs = RuleSet({r1, r2})

g.display()

t = 100

while t > 0:
     g1.display()
     rs.apply(g1)
     sleep(0.2)
     t -= 1






