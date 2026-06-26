from Objects.System import System, Grid
from Objects.Cell import Tile, BinaryCell, BinaryTile
from Objects.Condition import Condition, HasAlive, FalseCondition
from collections.abc import Callable, Sequence, Iterable, Collection
from typing import Any, Generic, TypeVar
from time_debug import timer
from functools import reduce
from constants import APPLICABLE_STATES

SystemType = TypeVar('SystemType')
TileType = TypeVar('TileType')
CellType = TypeVar('CellType')
StateType = TypeVar('StateType')

class Rule(Generic[SystemType, TileType, CellType, StateType]):
    def __init__(
            self, 
            get_nbhd: Callable[[SystemType, Any], Iterable[TileType]],
            cond: Condition[TileType, StateType],
            outcome: Callable[[CellType], None]
    ):
        self.get_nbhd = get_nbhd
        self.condition = cond
        self.outcome = outcome
        self.applicable_states = APPLICABLE_STATES[outcome]
    
    @timer
    def get_nbhds(self, system: SystemType) -> dict[Any, Iterable[TileType]]:
        nbhds = dict()
        if not isinstance(system, System):
            raise ValueError(f'system must be a System, not {type(system)}!')
        for key, cell in system.zone.items():
            cell_nbhd = self.get_nbhd(system, key)
            nbhds.update({key: cell_nbhd})
    
        return nbhds
    
    def get_states(
            self,
            system: SystemType
    ) -> dict[Any, StateType]:
        if not isinstance(system, System):
            raise ValueError(f'system must be a System, not {type(system)}!')
        
        state_dict = dict()

        nbhds = self.get_nbhds(system)

        for key, nbhd in nbhds.items():
            if key not in system.zone.keys():
                raise ValueError(f'get_nbhds` somehow created an invalid key: {key}')
            state = self.condition.get_state(nbhd)
            state_dict.update({key: state})
        
        return state_dict
    
    def check_states(
            self,
            system: SystemType,
            state_dict: dict[Any, StateType]
    ):
        if not isinstance(system, System):
            raise ValueError(f'system must be a System, not {type(system)}!')
        
        bool_dict = dict()

        for key, state in state_dict.items():    
            if system[key].state not in self.applicable_states:
                bool_dict.update({key: False})
            else:
                condition_met = self.condition.check_state(state)
                bool_dict.update({key: condition_met})
        
        return bool_dict

    @timer
    def condition_met(
            self,
            system: SystemType
    ) -> dict[Any, bool]:
        state_dict = self.get_states(system)
        bool_dict = self.check_states(system, state_dict)
        return bool_dict

    @timer
    def apply(
            self,
            system: SystemType,
            conditions_met: dict[Any, bool]
        ) -> None:
        if not isinstance(system, System):
            raise ValueError(f'system must be a System, not {type(system)}!')
        if not hasattr(system.cell_type, self.outcome.__name__):
            raise ValueError(f'The outcome must be a valid method of the cell type!')

        for key, bool in conditions_met.items():
            if bool:    
                if key not in system.zone.keys():
                    raise ValueError(f'conditions_met somehow created an invalid key: {key}')
                self.outcome(system.zone[key])

    def force_apply(self, system: SystemType):
        condition_met = self.condition_met(system)
        self.apply(system, condition_met)


class RuleSet(Generic[SystemType, TileType, CellType, StateType], dict[str, list[Rule[SystemType, TileType, CellType, StateType]]]):
    def __init__(self, rules: Sequence[Rule[SystemType, TileType, CellType, StateType]]):
        if len(rules):
            self.num_rules = len(rules)
        else:
            raise ValueError(f'A RuleSet must have at least one rule!')
        
        state_descriptions = set()

        for rule in rules:
            state_descriptions.add(rule.condition.state_description)
        
        state_descriptions = list(state_descriptions)

        rule_categories_by_description: list[list[Rule[SystemType, TileType, CellType, StateType]]] = []
        
        for sd in state_descriptions:
            compatible_rules: list[Rule[SystemType, TileType, CellType, StateType]] = []
            for rule in rules:
                if rule.condition.state_description == sd:
                    compatible_rules.append(rule)
            rule_categories_by_description.append(compatible_rules)
        
        super().__init__(zip(state_descriptions, rule_categories_by_description))
            

    def is_consistent(self):
        return True
    
    @timer
    def apply(self, system: SystemType):
        conditions_met = dict()
        for rule_category in self.values():
            system_state = rule_category[0].get_states(system)
            for rule in rule_category:
                bool_dict = rule.check_states(system, system_state)
                conditions_met.update({rule: bool_dict})
        
        for r, b in conditions_met.items():
            r.apply(system, b)

# Some particular rulesets

class BS(RuleSet[Grid, BinaryTile, BinaryCell, int]):
    def __init__(self, birth: Collection[int], survival: Collection[int], looping: bool=True):
        for num in birth:
            if not isinstance(num, int):
                raise ValueError('Birth and survival numbers must be integers!')
            if not 0 <= num <= 8:
                raise ValueError('Birth and survival numbers must be between 0 and 8!')
        for num in survival:
            if not isinstance(num, int):
                raise ValueError('Birth and survival numbers must be integers!')
            if not 0 <= num <= 8:
                raise ValueError('Birth and survival numbers must be between 0 and 8!')

        possible_states = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        death = [x for x in possible_states if (
            x not in birth and x not in survival
        )]

        birth_condition = reduce(lambda a, b: a | b, [HasAlive(i) for i in birth], FalseCondition())
        death_condition = reduce(lambda a, b: a | b, [HasAlive(i) for i in death], FalseCondition())

        if looping: 
            def nbhd(system: Grid, key: tuple[int, int]):
                nb = []
                i = key[0]
                j = key[1]
                for J in range(j - 1, j + 1 + 1):
                    for I in range(i - 1, i + 1 + 1):
                        if (I,J) != (i,j):
                            nb.append(system[(I % system.width, J % system.height)])
                return nb
        else:
            def nbhd(system: Grid, key: tuple[int, int]):
                nb = []
                i = key[0]
                j = key[1]
                for J in range(j - 1, j + 1 + 1):
                    for I in range(i - 1, i + 1 + 1):
                        if (I,J) != (i,j):
                            nb.append(system[(I, J)])
                return nb

        birth_rule = Rule(get_nbhd=nbhd, cond=birth_condition, outcome=BinaryCell.turn_on)
        death_rule = Rule(get_nbhd=nbhd, cond=death_condition, outcome=BinaryCell.turn_off)

        super().__init__(rules=[birth_rule, death_rule])

class Conway(BS):
    def __init__(self, looping=True):
        super().__init__([3], [2, 3], looping)
