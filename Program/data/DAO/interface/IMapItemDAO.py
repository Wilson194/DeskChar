from abc import ABC, abstractmethod
from structure.items.Item import *
from structure.map.Map import Map
from structure.map.MapItem import MapItem


class IMapItemDAO(ABC):
    @abstractmethod
    def create(self, mapItem: MapItem) -> int:
        """
        Create new map item        
        :param mapItem: Map object        
        :return: id of created mapItem
        """
        pass


    @abstractmethod
    def update(self, mapItem: MapItem):
        """
        Update map item in database
        :param mapItem: mapItem object with new data
        """
        pass


    @abstractmethod
    def delete(self, mapitem_id: int):
        """
        Delete Map item from database and all his translates
        :param mapitem_id: id of Map item
        """
        pass


    @abstractmethod
    def get(self, mapitem_id: int) -> MapItem:
        """
        Get map item from database
        :param mapitem_id: id of map item        
        :return: Map item object
        """
        pass


    @abstractmethod
    def get_all(self, lang: str = None):
        """
        Get list of map items for selected lang
        :param lang: lang of map items
        :return: list of map items
        """
        pass
