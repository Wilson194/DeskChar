from structure.enums.NodeType import NodeType
from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.Item import Item
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon


class Location(Object):
    TABLE_SCHEMA = [
        'id', 'name', 'description'
    ]


    def __init__(self, id: int = None, lang: str = None, name: str = None, description: str = None):
        super().__init__(id, lang, name, description)

        self.__locations = []
        self.__monsters = []
        self.__maps = []
        self.__characters = []

        self.__items = []
        self.__armors = []
        self.__containers = []
        self.__meleeWeapons = []
        self.__moneyList = []
        self.__rangedWeapons = []
        self.__throwableWeapons = []


    def __name__(self):
        names = super().__name__()
        names.append('Location')
        return names


    @staticmethod
    def DAO():
        from data.DAO.LocationDAO import LocationDAO
        return LocationDAO


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLLocation import XMLLocation
        return XMLLocation


    @staticmethod
    def layout():
        from presentation.layouts.LocationLayout import LocationLayout
        return LocationLayout


    @property
    def children(self):
        return []


    @property
    def treeChildren(self):
        return [ObjectType.LOCATION, ObjectType.ITEM, ObjectType.MONSTER,
                ObjectType.CHARACTER] + super().treeChildren


    @property
    def icon(self):
        return 'resources/icons/scroll.png'


    @property
    def object_type(self):
        return ObjectType.LOCATION


    # ------------------------------------- getters and setters -------------------------------


    # ------------------------------------- list getters and setters -------------------------------

    @property
    def locations(self):
        return self.__locations


    @locations.setter
    def locations(self, value):
        self.__locations = value


    @property
    def maps(self):
        return self.__maps


    @maps.setter
    def maps(self, value):
        self.__maps = value


    @property
    def characters(self):
        return self.__characters


    @characters.setter
    def characters(self, value):
        self.__characters = value


    @property
    def monsters(self):
        return self.__monsters


    @monsters.setter
    def monsters(self, value):
        self.__monsters = value


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


    def addContainer(self, container: Container):
        self.__containers.append(container)


    def addMoney(self, money: Money):
        self.__moneyList.append(money)


    def addMeleeWeapon(self, meleeWeapon: MeleeWeapon):
        self.__meleeWeapons.append(meleeWeapon)


    def addRangedWeapon(self, rangedWeapon: RangeWeapon):
        self.__rangedWeapons.append(rangedWeapon)


    def addThrowableWeapon(self, throwableWeapon: ThrowableWeapon):
        self.__throwableWeapons.append(throwableWeapon)
