from abc import ABC, abstractmethod

from structure.character.PartyCharacter import PartyCharacter
from structure.effects.Modifier import Modifier
from structure.enums.ObjectType import ObjectType
from structure.monster.Monster import Monster
from structure.spells.Spell import Spell


class IPartyCharacterDAO(ABC):
    @abstractmethod
    def create(self, character: PartyCharacter, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new PartyCharacter, if character given, linked with character and create character
                                   if character is not given, only party character created and liked with scenario
        :param character: PartyCharacter object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created character
        """
        pass


    @abstractmethod
    def update(self, character: PartyCharacter):
        """
        Update party PartyCharacter in database, update only party character, not Character
        :param character: PartyCharacter object with new data
        """
        pass


    @abstractmethod
    def delete(self, character_id: int):
        """
        Delete party character from database and all his translates
        :param character_id: id of party character
        """
        pass


    @abstractmethod
    def get(self, character_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> PartyCharacter:
        """
        Get Party Character , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param character_id: id of Party Character
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Party Character object
        """
        pass


    @abstractmethod
    def get_by_id(self, partyCharacterId: int, lang: str = None)->PartyCharacter:
        pass


    @abstractmethod
    def get_all(self, lang: str = None) -> list:
        pass
