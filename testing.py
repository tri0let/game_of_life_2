from Objects.Cell import *
from Objects.System import *
from Objects.Rule import *
from Objects.Condition import *
from time import sleep, perf_counter
import matplotlib.pyplot as plt

# @timer
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
def main(grid):
    rs.apply(grid)
    # sleep(0.1)
    

for grid_size in range(2, 50):
    grid = Grid(grid_size, grid_size, on_init=0.6)
    print('=' * 100)
    print(f'Grid size: {grid_size}')
    start = perf_counter()
    main(grid)
    stop = perf_counter()
    
    times.append(stop - start)
    grid_sizes.append(grid_size)

plt.plot(grid_sizes, times)
plt.show()



