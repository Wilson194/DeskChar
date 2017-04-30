from abc import ABC, abstractmethod
from structure.items.Item import *
from structure.map.Map import Map


class IMapDAO(ABC):
    @abstractmethod
    def create(self, map: Map, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new map and create empty map image, because of exporting        
        :param map: Map object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created map
        """
        pass


    @abstractmethod
    def update(self, map: Map):
        """
        Update map in database
        :param map: Location object with new data
        """
        pass


    @abstractmethod
    def delete(self, map_id: int):
        """
        Delete Map from database and from translate and delete all maps linked with map
        :param map_id: id of Map
        """
        pass


    @abstractmethod
    def get(self, map_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Map:
        """
        Get Map , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param map_id: id of Map
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Map object
        """
        pass


    @abstractmethod
    def get_all(self, lang: str = None):
        """
        Get list of maps for selected lang
        :param lang: lang of maps
        :return: list of maps
        """
        pass
