from abc import ABC, abstractmethod

from structure.abilities.Ability import Ability
from structure.effects.AbilityContext import AbilityContext
from structure.effects.Effect import Effect
from structure.enums.ObjectType import ObjectType
from structure.items.Item import Item


class IItemManager(ABC):
    @abstractmethod
    def create(self, item: Item, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new Item, depend on item type, insert correct data
        Items types:
            Item, Armor, Container, MeleeWeapon, ThrowableWeapon, RangedWeapon, Money
        :param item: Item object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created item
        """
        pass


    @abstractmethod
    def update(self, item: Item):
        """
        Update item in database
        :param item: Item object with new data
        """
        pass


    @abstractmethod
    def delete(self, item_id: int):
        """
        Delete Item from database and from translate
        :param item_id: id of Item
        """
        pass


    @abstractmethod
    def get(self, item_id: int, lang=None, nodeId: int = None, contextType: ObjectType = None) -> Item:
        """
        Get Item , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        

        Returned correct type of item, depend on database, possible classes are:
                Item, Container, Armor, Money, MeleeWeapon, RangedWeapon, ThrowableWeapon
        :param item_id: id of Item
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Item object
        """
        pass


    @abstractmethod
    def get_all(self, lang: str = None):
        """
        Get list of items for selected lang
        :param lang: lang of items
        :return: list of items
        """
        pass


    @abstractmethod
    def create_empty(self, lang: str) -> Item:
        pass
