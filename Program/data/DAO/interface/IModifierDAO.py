from abc import ABC, abstractmethod

from structure.effects.Modifier import Modifier
from structure.spells.Spell import Spell


class IModifierDAO(ABC):
    @abstractmethod
    def create(self, modifier: Modifier) -> int:
        pass


    @abstractmethod
    def update(self, modifier: Modifier) -> None:
        pass


    @abstractmethod
    def delete(self, modifier_id: int) -> None:
        pass


    @abstractmethod
    def get(self, modifier_id: int) -> Modifier:
        pass


    @abstractmethod
    def get_all(self) -> list:
        pass
