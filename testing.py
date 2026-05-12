from Objects.Cell import *
from Objects.Grid import *
g = Grid(border_width=1, on_init=[(5,5), (6,4), (6,6)])
g1 = Grid(on_init=0.2)

g.display()
g1.display()

g.check()
g1.check()





