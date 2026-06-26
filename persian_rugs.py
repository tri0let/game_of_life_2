from Objects.Cell import *
from Objects.System import *
from Objects.Rule import *
from Objects.Condition import *
from time import perf_counter, sleep

grid = Grid(26, 26, on_init=[(12,12), (12,13), (13,12), (13,13)])
# grid = Grid(26, 26, on_init=0.2)

persian_rugs = BS([2, 3, 4], [], looping=True)

@timer
def main():
    grid.display()
    persian_rugs.apply(grid)  

t = 10000

while t > 0:
    start = perf_counter()
    main()
    stop = perf_counter()
    sleep(max(0, 0.3 - (stop - start))) 
    t -= 1