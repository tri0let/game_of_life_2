from Objects.Cell import *
from Objects.Grid import *
g = Grid(border_width=1, on_init=[(5,5), (6,4), (6,6)])

print(g.xrange(True))

print(g.yrange())


g[(0,0)] = Dud()

g.display()

g.check()



