from abc import ABC, abstractmethod
from structure.spells.Spell import *


class ISpellDAO(ABC):
    @abstractmethod
    def create_spell(self, spell: Spell) -> int:
        pass


    @abstractmethod
    def update_spell(self, spell: Spell) -> None:
        pass


    @abstractmethod
    def delete_spell(self, spell_id: int) -> None:
        pass


    @abstractmethod
    def get_spell(self, spell: int) -> Spell:
        pass


    @abstractmethod
    def get_all_spells(self) -> list:
        pass
