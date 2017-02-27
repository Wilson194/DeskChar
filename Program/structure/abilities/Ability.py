from structure.enums.Races import Races
from structure.general.Object import Object


class Ability(Object):
    def __init__(self, id: int = None, lang: str = None, name: str = None,
                 description: str = None, chance: str = None, drd_race: Races = None):
        super().__init__(id, lang, name, description)
        self.__chance = chance
        self.__drd_race = drd_race


    def __name__(self):
        names = super().__name__()
        names.append('Ability')
        return names


    @property
    def chance(self):
        return self.__chance


    @chance.setter
    def chance(self, value):
        self.__chance = value


    @property
    def drd_races(self):
        return self.__drd_races


    @drd_races.setter
    def drd_races(self, value):
        self.__drd_races = value


    def __eq__(self, other):
        if not isinstance(other, Ability):
            return False

        if super().__eq__(other) and self.__chance == other.chance:
            return True

        return False
