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

        self.__inventory = None
        self.__ground = None

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
                NodeType.FOLDER] + super().treeChildren


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
    def inventory(self):
        return self.__inventory


    @inventory.setter
    def inventory(self, value):
        self.__inventory = value


    @property
    def ground(self):
        return self.__ground


    @ground.setter
    def ground(self, value):
        self.__ground = value


    def __eq__(self, other):
        if isinstance(other, Character):
            if super().__eq__(other) and self.__agility == other.agility and self.__charisma == other.charisma \
                    and self.__intelligence == other.intelligence and self.__mobility == other.mobility \
                    and self.__strength == other.strength and self.__toughness == other.toughness and self.__age == other.age \
                    and self.__height == other.height and self.__weight == other.weight and self.__level == other.level \
                    and self.xp == other.xp and self.__maxHealth == other.maxHealth and self.__maxMana == other.maxMana \
                    and self.__currentHealth == other.currentHealth and self.__currentMana == other.currentMana \
                    and self.__drdClass is other.drdClass and self.__drdRace is other.drdRace \
                    and self.__alignment == other.alignment:
                return True
        return False


    def printer(self, depth: int, full: bool = False):
        print('{}Character - {}'.format("  " * depth, self.name))
        if full:
            print('{}   agility: {}'.format("  " * depth, self.agility))
            print('{}   charisma: {}'.format("  " * depth, self.charisma))
            print('{}   intelligence: {}'.format("  " * depth, self.intelligence))
            print('{}   mobility: {}'.format("  " * depth, self.mobility))
            print('{}   strength: {}'.format("  " * depth, self.strength))
            print('{}   toughness: {}'.format("  " * depth, self.toughness))
            print('{}   age: {}'.format("  " * depth, self.age))
            print('{}   height: {}'.format("  " * depth, self.height))
            print('{}   weight: {}'.format("  " * depth, self.weight))
            print('{}   level: {}'.format("  " * depth, self.level))
            print('{}   xp: {}'.format("  " * depth, self.xp))
            print('{}   maxHealth: {}'.format("  " * depth, self.maxHealth))
            print('{}   maxMana: {}'.format("  " * depth, self.maxMana))
            print('{}   currentHealth: {}'.format("  " * depth, self.currentHealth))
            print('{}   currentMana: {}'.format("  " * depth, self.currentMana))
            print('{}   drdClass: {}'.format("  " * depth, self.drdClass))
            print('{}   drdRace: {}'.format("  " * depth, self.drdRace))
            print('{}   alignment: {}'.format("  " * depth, self.alignment))
