from abc import ABC, abstractmethod
from structure.abilities.Ability import *


class IAbilityDAO(ABC):
    @abstractmethod
    def create_ability(self, ability: Ability) -> int:
        pass


    @abstractmethod
    def update_ability(self, ability: Ability) -> None:
        pass


    @abstractmethod
    def delete_ability(self, ability_id: int) -> None:
        pass


    @abstractmethod
    def get_ability(self, ability_id: int) -> Ability:
        pass


    @abstractmethod
    def get_all_abilities(self) -> list:
        pass
