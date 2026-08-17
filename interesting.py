from Objects.Cell import *
from Objects.System import *
from Objects.Condition import *
from Objects.Rule import *
import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np
import math

def EvaluateRuleset(ruleset: RuleSet) -> dict[str, float]:
    t = 100
    gs = 20
    densities = [d / 10 for d in range(1, 10, 2)]
    random_dict = dict()
    for d in densities:
        random_grid = Grid(gs, gs, on_init=d)
        grids: list = simulate_ruleset(ruleset, system=random_grid, timesteps=t)
        metrics: dict = score_grid_simulation(grids)
        random_dict.update({d: metrics})
    return dict()

def simulate_ruleset(ruleset: RuleSet, system: System, timesteps: int) -> list[System]:
    t = 0
    system_history = []
    while t < timesteps:
        s_copy = deepcopy(system)
        system_history.append(s_copy)
        if isinstance(system, Grid):
            system.display()
        ruleset.apply(system)
        t += 1
    return system_history

def score_grid_simulation(grids: list[Grid]) -> dict[str, float]:
    # ...
    return dict()

def get_entropy(grid: Grid) -> float:
    num_alive = sum([c.state for c in grid.zone.values()])
    if num_alive == 0:
        return 0.0
    num_cells = grid.width * grid.height
    p = num_alive / num_cells
    if p == 1.0:
        return 0.0
    entropy = -p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)
    return entropy