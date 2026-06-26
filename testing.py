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
    BinaryCell.flip(c)

g.display()

def nbhd(system, key):
    nb = []
    i = key[0]
    j = key[1]
    for J in range(j - 1, j + 1 + 1):
        for I in range(i - 1, i + 1 + 1):
            if (I,J) != (i,j):
                nb.append(system[(I % len(system.xrange()), J % len(system.yrange()))])
    return nb



r1 = Rule(nbhd, HasAlive(4) or HasAlive(5), BinaryCell.flip)
r2 = Rule(nbhd, HasMoreAlive(3), BinaryCell.id)


rs = RuleSet({r1, r2})

t = 100

while t > 0:
     g1.display()
     rs.apply(g1)
     sleep(0.2)
     t -= 1






