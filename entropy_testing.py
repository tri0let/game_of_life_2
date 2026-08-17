from Objects.Cell import *
from Objects.System import *
from Objects.Rule import *
from Objects.Condition import *
from interesting import get_entropy
from time import sleep
import matplotlib.pyplot as plt

# @timer
def nbhd(system: Grid, key: tuple[int, int]):
    nb = []
    i, j = key
    for J in range(j - 1, j + 1 + 1):
        for I in range(i - 1, i + 1 + 1):
            if (I,J) != (i,j):
                nb.append(system[(I % system.width, J % system.height)])
    return nb

rs = Conway()
g = Grid(20, 20, on_init=0.2)

# rs = BS([2, 3, 4], [])
# g = Grid(20, 20, on_init=[(9,9), (9,10), (10,9), (10,10)])

entropies = []

@timer
def main():
    # g.display() 
    entropy = get_entropy(g)  
    # print(entropy)
    entropies.append(entropy)
    rs.apply(g)
    # sleep(0.5)
    
t = 100

while t > 0:
    main()
    t -= 1
    print(t)

plt.plot(entropies)
plt.show()
