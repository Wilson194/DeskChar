from abc import ABC, abstractmethod
from structure.items.Item import *


class IItemDAO(ABC):
    @abstractmethod
    def create_item(self, item: Item):
        pass


    @abstractmethod
    def update_item(self, item: Item):
        pass


    @abstractmethod
    def delete_item(self, item_id: int):
        pass


    @abstractmethod
    def get_item(self, item_id: int):
        pass


    @abstractmethod
    def get_all_items(self):
        pass
