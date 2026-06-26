from Objects.System import System
from Objects.Cell import Tile
from Objects.Condition import Condition
from collections.abc import Callable, Sequence, Iterable
from typing import Any, Generic, TypeVar
from time_debug import timer

SystemType = TypeVar('SystemType')
TileType = TypeVar('TileType')
CellType = TypeVar('CellType')
StateType = TypeVar('StateType')

class Rule(Generic[SystemType, TileType, CellType]):
    def __init__(
            self, 
            get_nbhd: Callable[[SystemType, Any], Iterable[TileType]],
            cond: Condition[TileType, StateType],
            outcome: Callable[[CellType], None]
    ):
        self.get_nbhd = get_nbhd
        self.condition = cond
        self.outcome = outcome
    
    @timer
    def get_nbhds(self, system: SystemType) -> dict[Any, Iterable[TileType]]:
        nbhds = dict()
        if not isinstance(system, System):
            raise ValueError(f'system must be a System, not {type(system)}!')
        for key, cell in system.zone.items():
            cell_nbhd = self.get_nbhd(system, key)
            nbhds.update({key: cell_nbhd})
    
        return nbhds
    
    @timer
    def check_condition(
            self,
            system: SystemType
    ) -> dict[Any, bool]:
        if not isinstance(system, System):
            raise ValueError(f'system must be a System, not {type(system)}!')
        
        bool_dict = dict()

        nbhds = self.get_nbhds(system)

        for key, nbhd in nbhds.items():
            if key not in system.zone:
                raise ValueError(f'get_nbhds somehow created an invalid key: {key}')
            condition_met = self.condition.met(nbhd)
            bool_dict.update({key: condition_met})
        
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
                if key not in system.zone:
                    raise ValueError(f'conditions_met somehow created an invalid key: {key}')
                self.outcome(system.zone[key])

    def force_apply(self, system: SystemType):
        conditions_met = self.check_condition(system)
        self.apply(system, conditions_met)


class RuleSet(Generic[SystemType, TileType, CellType], list[Rule[SystemType, TileType, CellType]]):
    def __init__(self, rules: Iterable[Rule[SystemType, TileType, CellType]]):
        super().__init__(rules)
        if len(self):
            self.num_rules = len(self)
        else:
            raise ValueError(f'A RuleSet must have at least one rule!')

    def is_consistent(self):
        return True
    
    @timer
    def apply(self, system: SystemType):
        conditions_met = dict()
        for rule in self:
            bool_dict = rule.check_condition(system)
            conditions_met.update({rule: bool_dict})
        
        for r, b in conditions_met.items():
            r.apply(system, b)
