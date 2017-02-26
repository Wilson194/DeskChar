from structure.general.Object import *


class Ability(Object):
    def __init__(self, id: int = None, lang: str = None, name: str = None,
                 description: str = None, chance: str = None):
        super().__init__(id, lang, name, description)
        self.__chance = chance


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


    def __eq__(self, other):
        if not isinstance(other, Ability):
            return False

        if super().__eq__(other) and self.__chance == other.chance:
            return True

        return False
