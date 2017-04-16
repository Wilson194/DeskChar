from structure.enums.Alignment import Alignment
from structure.enums.Classes import Classes
from structure.enums.NodeType import NodeType
from structure.enums.ObjectType import ObjectType
from structure.enums.Races import Races
from structure.general.Object import Object
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.Item import Item
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon


class Character(Object):
    TABLE_SCHEMA = [
        'id', 'name', 'description', 'agility', 'charisma', 'intelligence', 'mobility',
        'strength', 'toughness', 'age', 'height', 'weight', 'level', 'xp', 'maxHealth', 'maxMana',
        'drdClass', 'drdRace', 'alignment', 'currentMana', 'currentHealth'
    ]


    def __init__(self, id: int = None, lang: str = None, name: str = None, description: str = None,
                 agility: int = None, charisma: int = None, intelligence: int = None,
                 mobility: int = None, strength: int = None, toughness: int = None, age: int = None,
                 height: int = None, weight: int = None, level: int = None, xp: int = None,
                 maxHealth: int = None, maxMana: int = None, drdClass: Classes = None,
                 drdRace: Races = None, alignment: Alignment = None, currentHealth: int = None,
                 currentMana: int = None):
        super().__init__(id, lang, name, description)

        self.__agility = agility
        self.__charisma = charisma
        self.__intelligence = intelligence
        self.__mobility = mobility
        self.__strength = strength
        self.__toughness = toughness
        self.__age = age
        self.__height = height
        self.__weight = weight
        self.__level = level
        self.__xp = xp
        self.__maxHealth = maxHealth
        self.__maxMana = maxMana
        self.__currentHealth = currentHealth
        self.__currentMana = currentMana
        self.__drdClass = drdClass
        self.__drdRace = drdRace
        self.__alignment = alignment

        self.__items = []
        self.__armors = []
        self.__containers = []
        self.__meleeWeapons = []
        self.__moneyList = []
        self.__rangedWeapons = []
        self.__throwableWeapons = []

        self.__spells = []
        self.__abilities = []
        self.__effects = []


    def __name__(self):
        names = super().__name__()
        names.append('Character')
        return names


    @staticmethod
    def DAO():
        from data.DAO.CharacterDAO import CharacterDAO
        return CharacterDAO


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLCharacter import XMLCharacter
        return XMLCharacter


    @staticmethod
    def layout():
        from presentation.layouts.CharacterLayout import CharacterLayout
        return CharacterLayout


    @property
    def children(self):
        return []


    @property
    def treeChildren(self):
        return [ObjectType.ABILITY, ObjectType.SPELL, ObjectType.EFFECT,
                ObjectType.ITEM, NodeType.FOLDER] + super().treeChildren


    @property
    def icon(self):
        return 'resources/icons/helmet.png'


    @property
    def object_type(self):
        return ObjectType.CHARACTER


    @property
    def agility(self):
        return self.__agility


    @agility.setter
    def agility(self, value):
        self.__agility = value


    @property
    def charisma(self):
        return self.__charisma


    @charisma.setter
    def charisma(self, value):
        self.__charisma = value


    @property
    def intelligence(self):
        return self.__intelligence


    @intelligence.setter
    def intelligence(self, value):
        self.__intelligence = value


    @property
    def mobility(self):
        return self.__mobility


    @mobility.setter
    def mobility(self, value):
        self.__mobility = value


    @property
    def strength(self):
        return self.__strength


    @strength.setter
    def strength(self, value):
        self.__strength = value


    @property
    def toughness(self):
        return self.__toughness


    @toughness.setter
    def toughness(self, value):
        self.__toughness = value


    @property
    def age(self):
        return self.__age


    @age.setter
    def age(self, value):
        self.__age = value


    @property
    def height(self):
        return self.__height


    @height.setter
    def height(self, value):
        self.__height = value


    @property
    def weight(self):
        return self.__weight


    @weight.setter
    def weight(self, value):
        self.__weight = value


    @property
    def level(self):
        return self.__level


    @level.setter
    def level(self, value):
        self.__level = value


    @property
    def xp(self):
        return self.__xp


    @xp.setter
    def xp(self, value):
        self.__xp = value


    @property
    def maxHealth(self):
        return self.__maxHealth


    @maxHealth.setter
    def maxHealth(self, value):
        self.__maxHealth = value


    @property
    def maxMana(self):
        return self.__maxMana


    @maxMana.setter
    def maxMana(self, value):
        self.__maxMana = value


    @property
    def drdRace(self):
        return self.__drdRace


    @drdRace.setter
    def drdRace(self, value):
        self.__drdRace = value


    @property
    def drdClass(self):
        return self.__drdClass


    @drdClass.setter
    def drdClass(self, value):
        self.__drdClass = value


    @property
    def alignment(self):
        return self.__alignment


    @alignment.setter
    def alignment(self, value):
        self.__alignment = value


    @property
    def currentHealth(self):
        return self.__currentHealth


    @currentHealth.setter
    def currentHealth(self, value):
        self.__currentHealth = value


    @property
    def currentMana(self):
        return self.__currentMana


    @currentMana.setter
    def currentMana(self, value):
        self.__currentMana = value


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
    def effects(self):
        return self.__effects


    @effects.setter
    def effects(self, value):
        self.__effects = value


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


    def __eq__(self, other):
        return False
