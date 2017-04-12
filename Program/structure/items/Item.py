from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object
from structure.enums.Items import Items


class Item(Object):
    TABLE_SCHEMA = ['id', 'name', 'description', 'weight', 'price', 'type']


    def __init__(self, id=None, lang=None, name=None, description=None,
                 parent_id=None, weight=None, price=None):
        super().__init__(id, lang, name, description)
        self.__parent_id = parent_id
        self.__weight = weight
        self.__price = price
        self.__type = Items.GENERIC
        self.__effects = []


    def __name__(self):
        names = super().__name__()
        names.append('Item')
        return names


    @property
    def children(self):
        from structure.items.Armor import Armor
        from structure.items.Money import Money
        from structure.items.Container import Container
        from structure.items.MeleeWeapon import MeleeWeapon
        from structure.items.RangeWeapon import RangeWeapon
        from structure.items.ThrowableWeapon import ThrowableWeapon
        return [Armor, Money, Container, MeleeWeapon, RangeWeapon, ThrowableWeapon]


    @staticmethod
    def DAO():
        from data.DAO.ItemDAO import ItemDAO
        return ItemDAO


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLItem import XMLItem
        return XMLItem


    @staticmethod
    def layout():
        from presentation.layouts.ItemLayout import ItemLayout
        return ItemLayout


    @property
    def object_type(self):
        return ObjectType.ITEM


    @property
    def icon(self):
        return 'resources/icons/tools.png'


    @property
    def treeChildren(self):
        return [ObjectType.EFFECT] + super().treeChildren


    @property
    def parent_id(self):
        return self.__parent_id


    @parent_id.setter
    def parent_id(self, value):
        self.__parent_id = value


    @property
    def weight(self):
        return self.__weight


    @weight.setter
    def weight(self, value):
        self.__weight = value


    @property
    def price(self):
        return self.__price


    @price.setter
    def price(self, value):
        self.__price = value


    @property
    def type(self):
        return self.__type


    @property
    def effects(self):
        return self.__effects


    @effects.setter
    def effects(self, value):
        self.__effects = value


    def __eq__(self, other):
        if super().__eq__(
                other) and self.weight == other.weight and self.price == other.price:
            return True

        return False
