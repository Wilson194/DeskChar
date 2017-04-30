from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType
from structure.items.Armor import Armor
from structure.items.Item import Item
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon


class Container(Item):
    TABLE_SCHEMA = ['id', 'name', 'description', 'weight', 'price', 'capacity', 'type', 'amount']


    def __init__(self, id: int = None, lang=None, name: str = None,
                 description: str = None, parent_id: int = None, weight: int = None,
                 price: int = None, capacity: int = None, amount: int = 1):
        super().__init__(id, lang, name, description, parent_id, weight, price, amount)

        self.__capacity = capacity
        self.__type = Items.CONTAINER

        self.__items = []
        self.__armors = []
        self.__containers = []
        self.__meleeWeapons = []
        self.__moneyList = []
        self.__rangedWeapons = []
        self.__throwableWeapons = []


    def __name__(self):
        names = super().__name__()
        names.append('Container')
        return names


    @property
    def treeChildren(self):
        return [ObjectType.ITEM] + super().treeChildren


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLContainer import XMLContainer
        return XMLContainer


    @staticmethod
    def layout():
        from presentation.layouts.ContainerLayout import ContainerLayout
        return ContainerLayout


    @property
    def icon(self):
        return 'resources/icons/bag.png'


    @property
    def capacity(self):
        return self.__capacity


    @capacity.setter
    def capacity(self, value):
        self.__capacity = value


    @property
    def type(self):
        return self.__type


    @property
    def items(self):
        return self.__items


    @items.setter
    def items(self, value):
        self.__items = value


    @property
    def containers(self):
        return self.__containers


    @containers.setter
    def containers(self, value):
        self.__containers = value


    @property
    def armors(self):
        return self.__armors


    @armors.setter
    def armors(self, value):
        self.__armors = value


    @property
    def meleeWeapons(self):
        return self.__meleeWeapons


    @meleeWeapons.setter
    def meleeWeapons(self, value):
        self.__meleeWeapons = value


    @property
    def rangedWeapons(self):
        return self.__rangedWeapons


    @rangedWeapons.setter
    def rangedWeapons(self, value):
        self.__rangedWeapons = value


    @property
    def moneyList(self):
        return self.__moneyList


    @moneyList.setter
    def moneyList(self, value):
        self.__moneyList = value


    @property
    def throwableWeapons(self):
        return self.__throwableWeapons


    @throwableWeapons.setter
    def throwableWeapons(self, value):
        self.__throwableWeapons = value


    def addItem(self, item: Item):
        self.__items.append(item)


    def addArmor(self, armor: Armor):
        self.__armors.append(armor)


    def addContainer(self, container):
        self.__containers.append(container)


    def addMoney(self, money: Money):
        self.__moneyList.append(money)


    def addMeleeWeapon(self, meleeWeapon: MeleeWeapon):
        self.__meleeWeapons.append(meleeWeapon)


    def addRangedWeapon(self, rangedWeapon: RangeWeapon):
        self.__rangedWeapons.append(rangedWeapon)


    def addThrowableWeapon(self, throwableWeapon: ThrowableWeapon):
        self.__throwableWeapons.append(throwableWeapon)


    def __eq__(self, other):
        if isinstance(other, Container):
            if super().__eq__(other) and self.capacity == other.capacity:
                return True

        return False
