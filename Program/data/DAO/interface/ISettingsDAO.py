from abc import ABC, abstractmethod

from structure.character.PartyCharacter import PartyCharacter
from structure.effects.Modifier import Modifier
from structure.enums.ObjectType import ObjectType
from structure.monster.Monster import Monster
from structure.scenario.Scenario import Scenario
from structure.spells.Spell import Spell


class ISettingsDAO(ABC):
    @abstractmethod
    def get_value(self, name: str, type=None):
        """
        Get value of setting from database, str and int values could be returned
            Type could be str or int
        If not specified, int is first
        :param name: name of setting attribute
        :param type: type of value that will be returned
        :return: value of setting
        """
        pass


    @abstractmethod
    def set_value(self, name: str, value):
        """
        Set value for setting, save to database
        :param name: name of setting value
        :param value: value of setting 
        """
        pass
