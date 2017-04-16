from structure.enums.Classes import Classes
from structure.enums.ObjectType import ObjectType
from structure.enums.Races import Races
from structure.general.Object import Object


class Ability(Object):
    TABLE_SCHEMA = ['id', 'name', 'description', 'chance', 'drd_race', 'drd_class']


    def __init__(self, id: int = None, lang: str = None, name: str = None,
                 description: str = None, chance: str = None, drd_race: Races = None,
                 drd_class: Classes = None):
        super().__init__(id, lang, name, description)

        self.__chance = chance
        self.__drd_race = drd_race
        self.__drd_class = drd_class

        self.__contexts = []


    def __name__(self):
        names = super().__name__()
        names.append('Ability')
        return names


    @staticmethod
    def DAO():
        from data.DAO.AbilityDAO import AbilityDAO
        return AbilityDAO


    @staticmethod
    def layout():
        from presentation.layouts.AbilityLayout import AbilityLayout
        return AbilityLayout


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLAbility import XMLAbility
        return XMLAbility


    @property
    def object_type(self):
        return ObjectType.ABILITY


    @property
    def children(self):
        return []


    @property
    def icon(self):
        return 'resources/icons/map.png'


    @property
    def treeChildren(self):
        return [ObjectType.ABILITY_CONTEXT] + super().treeChildren


    @property
    def chance(self):
        return self.__chance


    @chance.setter
    def chance(self, value):
        self.__chance = value


    @property
    def drd_race(self):
        return self.__drd_race


    @drd_race.setter
    def drd_race(self, value):
        self.__drd_race = value


    @property
    def drd_class(self):
        return self.__drd_class


    @drd_class.setter
    def drd_class(self, value):
        self.__drd_class = value


    @property
    def contexts(self):
        return self.__contexts


    @contexts.setter
    def contexts(self, value):
        self.__contexts = value


    def __eq__(self, other):
        if not isinstance(other, Ability):
            return False

        if super().__eq__(other) and self.__chance == other.chance:
            return True

        return False
