from abc import ABC, abstractmethod


class IAbilityDAO(ABC):
    @abstractmethod
    def create(self, ability) -> int:
        pass


    @abstractmethod
    def update(self, ability) -> None:
        pass


    @abstractmethod
    def delete(self, ability_id: int) -> None:
        pass


    @abstractmethod
    def get(self, ability_id: int):
        pass


    @abstractmethod
    def get_all(self) -> list:
        pass
