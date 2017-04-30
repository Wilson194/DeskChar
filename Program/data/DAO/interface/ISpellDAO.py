from abc import ABC, abstractmethod

from structure.enums.ObjectType import ObjectType
from structure.spells.Spell import Spell


class ISpellDAO(ABC):
    @abstractmethod
    def create(self, spell: Spell, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new Spell
        :param spell: Spell object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created Spell
        """
        pass


    @abstractmethod
    def update(self, spell: Spell) -> None:
        """
        Update spell in database
        :param spell: Spell object with new data
        """
        pass


    @abstractmethod
    def delete(self, spell_id: int) -> None:
        """
        Delete spell from database and all his translates
        :param spell_id: id of spell
        """
        pass


    @abstractmethod
    def get(self, spell_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Spell:
        """
        Get Spell , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param spell_id: id of Spell
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Spell object
        """
        pass


    @abstractmethod
    def get_all(self, lang=None) -> list:
        """
        Get list of Spell for selected lang
        :param lang: lang of Spell
        :return: list of Spell
        """
        pass
