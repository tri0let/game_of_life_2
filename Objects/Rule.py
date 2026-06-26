from Objects.System import System
from Objects.Cell import Tile
from Objects.Condition import Condition
from collections.abc import Callable, Sequence, Iterable
from typing import Any, Generic, TypeVar

class Rule:
    def __init__(
            self, 
            get_nbhd: Callable[[System, Any], Iterable[Tile]],
            cond: Condition,
            outcome: Callable[[Tile], None]
    ):
        self.get_nbhd = get_nbhd
        self.condition = cond
        self.outcome = outcome
    
    def get_nbhds(self, system: System) -> dict[Any, Iterable[Tile]]:
        nbhds = dict()
        if not isinstance(system, System):
            raise ValueError(f'system must be a System, not {type(system)}!')
        for key, cell in system.zone.items():
            cell_nbhd = self.get_nbhd(system, key)
            nbhds.update({key: cell_nbhd})
    
        return nbhds
    
    def check_condition(
            self,
            system: System
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

    def apply(
            self,
            system: System,
            conditions_met: dict[Any, bool]
        ) -> None:
        if not isinstance(system, System):
            raise ValueError(f'system must be a System, not {type(system)}!')
        if not hasattr(system.cell_type, self.outcome.__name__):
            raise ValueError(f'The outcome must be a valid method of the cell type!')

        for key, bool in conditions_met.items():
            if key not in system.zone:
                raise ValueError(f'conditions_met somehow created an invalid key: {key}')
            if bool:
                self.outcome(system.zone[key])

    def force_apply(self, system: System):
        conditions_met = self.check_condition(system)
        self.apply(system, conditions_met)


class RuleSet(list[Rule]):
    def __init__(self, rules: Iterable[Rule]):
        super().__init__(rules)
        if len(self):
            self.num_rules = len(self)
        else:
            raise ValueError(f'A RuleSet must have at least one rule!')

    def is_consistent(self):
        return True
    
    def apply(self, system: System):
        conditions_met = dict()
        for rule in self:
            bool_dict = rule.check_condition(system)
            conditions_met.update({rule: bool_dict})
        
        for r, b in conditions_met.items():
            r.apply(system, b)
