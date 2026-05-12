# Game of Life Project

## Object descriptions

- A state is a number, generally between zero and one
- A tile is the smallest unit of the program
- A grid (maybe find something more general?) is a set of tiles arranged in a geometric pattern
- A dud tile is a tile whose state cannot change
- A cell tile is a tile whose state can change according to a list of predefined outcomes, defined using class methods on that cell
- A neighborhood function is a function from a tile to a list of tiles (from a cell to a list of cells?), called a neighborhood
- A condition is a function from a neighborhood to either True or False
- A rule is (still deciding):
    - a function from one grid to another based on the cells' outcomes
    - a function from a grid to a set of outcomes with the same shape as the grid
    - a function from one cell to another based on its outcomes
- A rule checks a single condition for each cell, then applies a single outcome to each cell that meets that condition (in a single step)