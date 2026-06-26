from Objects.System import *
from Objects.Cell import *
from Objects.Condition import *
from Objects.Rule import *
from time import sleep, perf_counter

grid = Grid(20, 20, on_init=[(0,0), (0,2), (1,2), (1,1), (2,1)])
# grid = Grid(50, 50, on_init=0.3)

def nbhd(system: Grid, key: tuple[int, int]):
    nb = []
    i = key[0]
    j = key[1]
    for J in range(j - 1, j + 1 + 1):
        for I in range(i - 1, i + 1 + 1):
            if (I,J) != (i,j):
                nb.append(system[(I % system.width, J % system.height)])
    return nb

r1 = Rule(nbhd, HasLessAlive(2), BinaryCell.turn_off)
r2 = Rule(nbhd, HasMoreAlive(3), BinaryCell.turn_off)
r3 = Rule(nbhd, HasAlive(3), BinaryCell.turn_on)

rs = RuleSet([r1, r2, r3])

times = []
grid_sizes = []

@timer
def main():
    grid.display()
    rs.apply(grid)  

t = 100

while t > 0:
    start = perf_counter()
    main()
    stop = perf_counter()
    # sleep(0.3 - (stop - start)) 
    t -= 1

