from abc import ABC, abstractmethod

from structure.abilities.Ability import Ability
from structure.character.Character import Character
from structure.effects.AbilityContext import AbilityContext
from structure.enums.ObjectType import ObjectType


class ICharacterManager(ABC):
    @abstractmethod
    def create(self, character: Character, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new character
        :param character: Character object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created character
        """
        pass


    @abstractmethod
    def update(self, character: Character) -> None:
        """
        Update spell in database
        :param character: Character object with new data
        """
        pass


    @abstractmethod
    def delete(self, character_id: int) -> None:
        """
        Delete character from database and from translate
        :param character_id: id of character
        """
        pass


    @abstractmethod
    def get(self, character_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Character:
        """
        Get Character , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param character_id: id of Character
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Character object
        """
        pass


    @abstractmethod
    def get_all(self, lang: str = None) -> list:
        """
        Get list of characters for selected lang
        :param lang: lang of characters
        :return: list of characters
        """
        pass


    @abstractmethod
    def create_empty(self, lang: str) -> Character:
        pass
