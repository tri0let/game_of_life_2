from Objects.Cell import *
from Objects.Grid import *

print(State.ON)

print(State.OFF + State.OFF)

print(State.ON * State.ON)

g = Grid(border_width=1, on_init=[(5,5), (6,6)])

g.display()

print(g.nbhd(5,5))

