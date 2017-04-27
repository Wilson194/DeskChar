from datetime import date as d

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


class Scenario(Object):
    TABLE_SCHEMA = [
        'id', 'name', 'description', 'date'
    ]


    def __init__(self, id: int = None, lang: str = None, name: str = None, description: str = None,
                 date: d = None):
        super().__init__(id, lang, name, description)

        self.__date = date

        self.__party = []

        self.__locations = []

        self.__abilities = []
        self.__spells = []
        self.__effects = []

        self.__items = []
        self.__armors = []
        self.__containers = []
        self.__meleeWeapons = []
        self.__moneyList = []
        self.__rangedWeapons = []
        self.__throwableWeapons = []


    def __name__(self):
        names = super().__name__()
        names.append('Scenario')
        return names


    @staticmethod
    def DAO():
        from data.DAO.ScenarioDAO import ScenarioDAO
        return ScenarioDAO


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLScenario import XMLScenario
        return XMLScenario


    @staticmethod
    def layout():
        from presentation.layouts.ScenarioLayout import ScenarioLayout
        return ScenarioLayout


    @property
    def children(self):
        return []


    @property
    def treeChildren(self):
        return [ObjectType.SPELL, ObjectType.ITEM, ObjectType.ABILITY,
                ObjectType.EFFECT, NodeType.FOLDER, ObjectType.LOCATION,
                ObjectType.CHARACTER] + super().treeChildren


    @property
    def icon(self):
        return 'resources/icons/drd.png'


    @property
    def object_type(self):
        return ObjectType.SCENARIO


    # ------------------------------------- getters and setters -------------------------------
    @property
    def date(self):
        return self.__date


    @date.setter
    def date(self, value):
        self.__date = value


    # ------------------------------------- list getters and setters -------------------------------

    @property
    def locations(self):
        return self.__locations


    @locations.setter
    def locations(self, value):
        self.__locations = value


    @property
    def party(self):
        return self.__party


    @party.setter
    def party(self, value):
        self.__party = value


    @property
    def effects(self):
        return self.__effects


    @effects.setter
    def effects(self, value):
        self.__effects = value


    @property
    def abilities(self):
        return self.__abilities


    @abilities.setter
    def abilities(self, value):
        self.__abilities = value


    @property
    def spells(self):
        return self.__spells


    @spells.setter
    def spells(self, value):
        self.__spells = value


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


    def printer(self, depth: int = 0):
        print('Scenario: {}'.format(self.name))
        print('  Spells: ')
        for spell in self.spells:
            spell.printer(depth + 2)
        print('  Effects:')
        for effect in self.effects:
            effect.printer(depth + 2)
        print('  Abilities: ')
        for ability in self.abilities:
            ability.printer(depth + 2)
        print('  Locations: ')
        for location in self.locations:
            location.printer(depth + 2)
