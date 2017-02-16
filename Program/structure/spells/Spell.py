from general.Object import *


class Spell(Object):
    def __init__(self, id: int = None, lang: str = None, name: str = None,
                 description: str = None, mana_cost_initial: str = None,
                 mana_cost_continual: str = None, range: str = None,
                 scope: str = None, cast_time: int = None,
                 duration: str = None):
        super().__init__(id, lang, name, description)
        self.__mana_cost_initial = mana_cost_initial
        self.__mana_cost_continual = mana_cost_continual
        self.__range = range
        self.__scope = scope
        self.__cast_time = cast_time
        self.__duration = duration


    def __name__(self):
        names = super().__name__()
        names.append('Spell')
        return names


    @property
    def mana_cost_initial(self):
        return self.__mana_cost_initial


    @mana_cost_initial.setter
    def mana_cost_initial(self, value):
        self.__mana_cost_initial = value


    @property
    def mana_cost_continual(self):
        return self.__mana_cost_continual


    @mana_cost_continual.setter
    def mana_cost_continual(self, value):
        self.__mana_cost_continual = value


    @property
    def range(self):
        return self.__range


    @range.setter
    def range(self, value):
        self.__range = value


    @property
    def scope(self):
        return self.__scope


    @scope.setter
    def scope(self, value):
        self.__scope = value


    @property
    def cast_time(self):
        return self.__cast_time


    @cast_time.setter
    def cast_time(self, value):
        self.__cast_time = value


    @property
    def duration(self):
        return self.__duration


    @duration.setter
    def duration(self, value):
        self.__duration = value


    def __eq__(self, other):
        if not isinstance(other, Spell):
            return False

        if super().__eq__(
                other) and self.__mana_cost_initial == other.mana_cost_initial \
                and self.__mana_cost_continual == other.mana_cost_continual \
                and self.__range == other.range \
                and self.__scope == other.scope \
                and self.__cast_time == other.cast_time \
                and self.__duration == other.duration:
            return True

        return False
