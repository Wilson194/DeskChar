from abc import ABC, abstractmethod
from structure.spells.Spell import Spell


class ISpellDAO(ABC):
    @abstractmethod
    def create(self, spell: Spell) -> int:
        pass


    @abstractmethod
    def update(self, spell: Spell) -> None:
        pass


    @abstractmethod
    def delete(self, spell_id: int) -> None:
        pass


    @abstractmethod
    def get(self, spell: int) -> Spell:
        pass


    @abstractmethod
    def get_all(self) -> list:
        pass
