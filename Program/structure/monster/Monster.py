from structure.enums.Alignment import Alignment
from structure.enums.MonsterRace import MonsterRace
from structure.enums.MonsterSize import MonsterSize
from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.Item import Item
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon


class Monster(Object):
    TABLE_SCHEMA = [
        'id', 'name', 'description', 'viability', 'offense', 'defense', 'endurance', 'rampancy',
        'mobility', 'perseverance', 'intelligence', 'charisma', 'alignment', 'experience', 'hp',
        'monsterRace', 'size'
    ]


    def __init__(self, id: int = None, lang: str = None, name: str = None, description: str = None,
                 viability: str = None, offense: str = None, defense: int = None,
                 endurance: int = None, rampancy: int = None, mobility: int = None,
                 perseverance: int = None, intelligence: int = None, charisma: int = None,
                 alignment: Alignment = None, experience: int = None, hp: int = None,
                 monsterRace: MonsterRace = None, size: MonsterSize = None):
        super().__init__(id, lang, name, description)

        self.__viability = viability
        self.__offense = offense
        self.__defense = defense
        self.__endurance = endurance
        self.__rampancy = rampancy
        self.__mobility = mobility
        self.__perseverance = perseverance
        self.__intelligence = intelligence
        self.__charisma = charisma
        self.__alignment = alignment
        self.__experience = experience
        self.__hp = hp

        self.__monsterRace = monsterRace
        self.__size = size

        self.__abilities = []
        self.__spells = []

        self.__items = []
        self.__armors = []
        self.__containers = []
        self.__meleeWeapons = []
        self.__moneyList = []
        self.__rangedWeapons = []
        self.__throwableWeapons = []


    def __name__(self):
        names = super().__name__()
        names.append('Monster')
        return names


    @staticmethod
    def DAO():
        from data.DAO.MonsterDAO import MonsterDAO
        return MonsterDAO


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLMonster import XMLMonster
        return XMLMonster


    @staticmethod
    def layout():
        from presentation.layouts.MonsterLayout import MonsterLayout
        return MonsterLayout


    @property
    def children(self):
        return []


    @property
    def treeChildren(self):
        return [ObjectType.SPELL, ObjectType.ITEM, ObjectType.ABILITY] + super().treeChildren


    @property
    def icon(self):
        return 'resources/icons/imp.png'


    @property
    def object_type(self):
        return ObjectType.MONSTER


    @property
    def viability(self):
        return self.__viability


    @viability.setter
    def viability(self, value):
        self.__viability = value


    @property
    def offense(self):
        return self.__offense


    @offense.setter
    def offense(self, value):
        self.__offense = value


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
    def alignment(self):
        return self.__alignment


    @alignment.setter
    def alignment(self, value):
        self.__alignment = value


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
    def monsterRace(self):
        return self.__monsterRace


    @monsterRace.setter
    def monsterRace(self, value):
        self.__monsterRace = value


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
        if isinstance(other, Monster):
            if super().__eq__(other) and self.viability == other.viability and self.offense == other.offense \
                    and self.defense == other.defense and self.endurance == other.endurance and self.rampancy == other.rampancy \
                    and self.mobility == other.mobility and self.perseverance == other.perseverance \
                    and self.intelligence == other.intelligence and self.charisma == other.charisma \
                    and self.alignment is other.alignment and self.experience == other.experience and self.hp == other.hp \
                    and self.monsterRace is other.monsterRace and self.size is other.size:
                return True

        return False

    def __hash__(self):
        return hash((self.object_type, self.id))