from abc import ABC, abstractmethod

from structure.effects.Modifier import Modifier
from structure.enums.ObjectType import ObjectType
from structure.monster.Monster import Monster
from structure.spells.Spell import Spell


class IMonsterDAO(ABC):
    @abstractmethod
    def create(self, monster: Monster, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new Monster
        :param monster: Modifier object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created monster
        """
        pass


    @abstractmethod
    def update(self, monster: Monster):
        """
        Update monster in database
        :param monster: Monster object with new data
        """
        pass


    @abstractmethod
    def delete(self, monster_id: int):
        """
        Delete Monster from database and all his translates
        :param monster_id: id of Monster
        """
        pass


    @abstractmethod
    def get(self, monster_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Monster:
        """
        Get Monster , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param monster_id: id of Monster
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Monster object
        """
        pass


    @abstractmethod
    def get_all(self, lang: str = None) -> list:
        """
        Get list of Monsters for selected lang
        :param lang: lang of Monsters
        :return: list of Monsters
        """
        pass
