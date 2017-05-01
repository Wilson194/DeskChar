from abc import ABC, abstractmethod

from structure.abilities.Ability import Ability
from structure.effects.AbilityContext import AbilityContext
from structure.effects.Effect import Effect
from structure.effects.Modifier import Modifier
from structure.enums.ObjectType import ObjectType
from structure.general.Lang import Lang
from structure.map.Map import Map
from structure.monster.Monster import Monster
from structure.scenario.Scenario import Scenario
from structure.spells.Spell import Spell


class ITabWidgetManager(ABC):
    @abstractmethod
    def get_data(self, target_id: int, target_type: ObjectType) -> list:
        """
        Return list of objects, objects are for one ID but all langs
        :param target_id: id of object
        :param target_type: Type of object
        :return: List of object
        """
        pass


    @abstractmethod
    def get_layout(self, target_type: ObjectType, parent):
        """
        Get layout for targget type
        :param target_type: Type of object
        :param parent: parent object for creating layout
        :return: Layout for target object
        """
        pass


    @abstractmethod
    def get_empty_object(self, target_type: ObjectType, id: int, lang: str) -> object:
        """
        Create empty object for id and lang
        :param target_type: Type ob object
        :param id: id of object
        :param lang: lang code of object
        :return: New empty object
        """
        pass
