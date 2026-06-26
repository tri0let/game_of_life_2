from Objects.System import *
from Objects.Cell import *
from Objects.Condition import *
from Objects.Rule import *
from time import sleep, perf_counter

# grid = Grid(20, 20, on_init=[(0,0), (0,2), (1,2), (1,1), (2,1)])
grid = Grid(40, 40, on_init=0.2)

rs = Conway()

@timer
def main():
    grid.display()
    rs.apply(grid)  

t = 10000

while t > 0:
    start = perf_counter()
    main()
    stop = perf_counter()
    # sleep(max(0, 0.1 - (stop - start))) 
    t -= 1

