from structure.enums.Classes import Classes
from structure.enums.ObjectType import ObjectType
from structure.enums.Races import Races
from structure.general.Object import Object


class Ability(Object):
    def __init__(self, id: int = None, lang: str = None, name: str = None,
                 description: str = None, chance: str = None, drd_race: Races = None,
                 drd_class: Classes = None):
        super().__init__(id, lang, name, description)
        self.__chance = chance
        self.__drd_race = drd_race
        self.__drd_class = drd_class


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


    def __eq__(self, other):
        if not isinstance(other, Ability):
            return False

        if super().__eq__(other) and self.__chance == other.chance:
            return True

        return False
