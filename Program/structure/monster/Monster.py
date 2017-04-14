from structure.enums.MonsterRace import MonsterRace
from structure.enums.MonsterSize import MonsterSize
from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object


class Monster(Object):
    def __init__(self, id: int = None, lang: str = None, name: str = None, description: str = None,
                 viability: int = None, offens: int = None, defense: int = None,
                 endurance: int = None, rampancy: int = None, mobility: int = None,
                 perseverance: int = None, intelligence: int = None, charisma: int = None,
                 conviction: int = None, experience: int = None, hp: int = None,
                 monsterRace: MonsterRace = None, size: MonsterSize = None):
        super().__init__(id, lang, name, description)

        self.__viability = viability
        self.__offens = offens
        self.__defense = defense
        self.__endurance = endurance
        self.__rampancy = rampancy
        self.__mobility = mobility
        self.__perseverance = perseverance
        self.__intelligence = intelligence
        self.__charisma = charisma
        self.__conviction = conviction
        self.__experience = experience
        self.__hp = hp

        self.__monsterRace = monsterRace
        self.__size = size

        self.__items = []
        self.__abilities = []
        self.__spells = []

    def __name__(self):
        names = super().__name__()
        names.append('Monster')
        return names


    @staticmethod
    def DAO():
        return None


    @staticmethod
    def XmlClass():
        return None


    @staticmethod
    def layout():
        return None


    @property
    def children(self):
        return []


    @property
    def treeChildren(self):
        return [] + super().treeChildren


    @property
    def icon(self):
        return 'resources/icons/imp.png'


    @property
    def object_type(self):
        return ObjectType.CHARACTER


    @property
    def viability(self):
        return self.__viability


    @viability.setter
    def viability(self, value):
        self.__viability = value


    @property
    def offens(self):
        return self.__offens


    @offens.setter
    def offens(self, value):
        self.__offens = value


    @property
    def defense(self):
        return self.__defense


    @defense.setter
    def defense(self, value):
        self.__defense = value


    @property
    def endurance(self):
        return self.__endurance


    @endurance.setter
    def endurance(self, value):
        self.__endurance = value


    @property
    def rampancy(self):
        return self.__rampancy


    @rampancy.setter
    def rampancy(self, value):
        self.__rampancy = value


    @property
    def mobility(self):
        return self.__mobility


    @mobility.setter
    def mobility(self, value):
        self.__mobility = value


    @property
    def perseverance(self):
        return self.__perseverance


    @perseverance.setter
    def perseverance(self, value):
        self.__perseverance = value


    @property
    def intelligence(self):
        return self.__intelligence


    @intelligence.setter
    def intelligence(self, value):
        self.__intelligence = value


    @property
    def charisma(self):
        return self.__charisma


    @charisma.setter
    def charisma(self, value):
        self.__charisma = value


    @property
    def conviction(self):
        return self.__conviction


    @conviction.setter
    def conviction(self, value):
        self.__conviction = value


    @property
    def experience(self):
        return self.__experience


    @experience.setter
    def experience(self, value):
        self.__experience = value


    @property
    def hp(self):
        return self.__hp


    @hp.setter
    def hp(self, value):
        self.__hp = value


    @property
    def drdRace(self):
        return self.__drdRace


    @drdRace.setter
    def drdRace(self, value):
        self.__drdRace = value


    @property
    def size(self):
        return self.__size


    @size.setter
    def size(self, value):
        self.__size = value


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

