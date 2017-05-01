from abc import ABC, abstractmethod

from structure.abilities.Ability import Ability
from structure.effects.AbilityContext import AbilityContext
from structure.effects.Effect import Effect
from structure.enums.ObjectType import ObjectType
from structure.general.Lang import Lang
from structure.scenario.Location import Location


class ILocationManager(ABC):
    @abstractmethod
    def create(self, location: Location, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new location        
        :param location: Location object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created location
        """
        pass


    @abstractmethod
    def update_location(self, location: Location) -> None:
        """
        Update location in database
        :param location: Location object with new data
        """
        pass


    @abstractmethod
    def delete(self, location_id: int) -> None:
        """
        Delete Location from database and from translate
        :param location_id: id of Location
        """
        pass


    @abstractmethod
    def get(self, location_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Location:
        """
        Get Location , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param location_id: id of Location
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Location object
        """
        pass


    @abstractmethod
    def get_all(self, lang: str = None):
        """
        Get list of locations for selected lang
        :param lang: lang of locations
        :return: list of locations
        """
        pass


    @abstractmethod
    def create_empty(self, lang: str) -> Location:
        pass
