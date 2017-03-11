from abc import ABC, abstractmethod
from structure.items.Item import *


class IItemDAO(ABC):
    @abstractmethod
    def create(self, item: Item):
        pass


    @abstractmethod
    def update(self, item: Item):
        pass


    @abstractmethod
    def delete(self, item_id: int):
        pass


    @abstractmethod
    def get(self, item_id: int):
        pass


    @abstractmethod
    def get_all(self):
        pass
