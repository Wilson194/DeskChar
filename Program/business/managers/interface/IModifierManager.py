from abc import ABC, abstractmethod

from structure.abilities.Ability import Ability
from structure.effects.AbilityContext import AbilityContext
from structure.effects.Effect import Effect
from structure.effects.Modifier import Modifier
from structure.enums.ObjectType import ObjectType
from structure.general.Lang import Lang
from structure.map.Map import Map


class IModifierManager(ABC):
    @abstractmethod
    def create(self, modifier: Modifier, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new Modifier
        :param modifier: Modifier object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created Modifier
        """
        pass


    @abstractmethod
    def update(self, modifier: Modifier) -> None:
        """
        Update modifier in database
        :param modifier: Modifier object with new data
        """
        pass


    @abstractmethod
    def delete(self, modifier_id: int) -> None:
        """
        Delete Modifier from database and all his translates
        :param modifier_id: id of Modifier
        """
        pass


    @abstractmethod
    def get(self, modifier_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Modifier:
        """
        Get Modifier , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param modifier_id: id of Modifier
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Modifier object
        """
        pass


    @abstractmethod
    def get_all(self) -> list:
        """
        Get list of modifiers for selected lang
        :param lang: lang of modifiers
        :return: list of modifiers
        """
        pass


    @abstractmethod
    def create_empty(self, lang: str) -> Modifier:
        pass
