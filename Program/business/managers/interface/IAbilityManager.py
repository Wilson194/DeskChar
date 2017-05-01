from abc import ABC, abstractmethod

from structure.abilities.Ability import Ability
from structure.effects.AbilityContext import AbilityContext
from structure.enums.ObjectType import ObjectType


class IAbilityManager(ABC):
    @abstractmethod
    def create(self, ability: Ability, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new ability
        :param ability: Ability object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created ability
        """
        pass


    @abstractmethod
    def update_ability(self, ability: Ability) -> None:
        """
        Update ability in database
        :param ability: Ability object with new data
        """
        pass


    @abstractmethod
    def delete(self, ability_id: int) -> None:
        """
        Delete ability from database and from translate
        :param ability_id: id of ability
        """
        pass


    @abstractmethod
    def get(self, ability_id: int, lang=None, nodeId: int = None, contextType: ObjectType = None) -> Ability:
        """
        Get ability , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param ability_id: id of ability
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Ability object
        """
        pass


    @abstractmethod
    def get_all(self, lang: str) -> list:
        """
        Get list of abilities for selected lang
        :param lang: lang of abilities
        :return: list of abilities
        """
        pass


    @abstractmethod
    def create_empty(self, lang: str) -> Ability:
        pass
