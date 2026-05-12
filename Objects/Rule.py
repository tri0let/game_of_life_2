from Objects.System import System
from Objects.Cell import Tile
from Objects.Condition import Condition
from collections.abc import Callable, Sequence, Iterable
from typing import Any, Generic, TypeVar

SystemType = TypeVar('SystemType')
TileType = TypeVar('TileType')
CellType = TypeVar('CellType')

class Rule(Generic[SystemType, TileType, CellType]):
    def __init__(
            self, 
            get_nbhd: Callable[[SystemType, Any], Iterable[TileType]],
            cond: Condition[TileType],
            outcome: Callable[[CellType], None]
    ):
        self.get_nbhd = get_nbhd
        self.condition = cond
        self.outcome = outcome
    
    def get_nbhds(self, system: SystemType) -> dict[Any, Iterable[TileType]]:
        nbhds = dict()
        if not isinstance(system, System):
            raise ValueError(f'system must be a System, not {type(system)}!')
        for key, cell in system.zone.items():
            cell_nbhd = self.get_nbhd(system, key)
            nbhds.update({key: cell_nbhd})
    
        return nbhds
    
    def check_condition(
            self,
            system: SystemType
    ):
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

    def apply(
            self,
            system: SystemType
        ) -> None:
        if not isinstance(system, System):
            raise ValueError(f'system must be a System, not {type(system)}!')
        if not hasattr(system.cell_type, self.outcome.__name__):
            raise ValueError(f'The outcome must be a valid method of the cell type!')
        
        conditions_met = self.check_condition(system)

        for key, bool in conditions_met.items():
            if key not in system.zone:
                raise ValueError(f'conditions_met somehow created an invalid key: {key}')
            if bool:
                self.outcome(system.zone[key])