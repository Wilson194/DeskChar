from abc import ABC, abstractmethod

from structure.effects.Effect import Effect
from structure.effects.Modifier import Modifier
from structure.spells.Spell import Spell


class IEffectDAO(ABC):
    @abstractmethod
    def create(self, effect: Effect) -> int:
        pass


    @abstractmethod
    def update(self, effect: Effect) -> None:
        pass


    @abstractmethod
    def delete(self, effect_id: int) -> None:
        pass


    @abstractmethod
    def get(self, effect_id: int, lang: str) -> Effect:
        pass


    @abstractmethod
    def get_all(self) -> list:
        pass
