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


class IScenarioManager(ABC):
    @abstractmethod
    def create(self, scenario: Scenario, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new scenario
        :param scenario: Scenario object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created Scenario
        """
        pass


    @abstractmethod
    def update_scenario(self, scenario: Scenario):
        """
        Update scenario in database
        :param scenario: Scenario object with new data
        """
        pass


    @abstractmethod
    def delete(self, scenario_id: int):
        """
        Delete Scenario from database and all his translates
        :param scenario_id: id of Scenario
        """
        pass


    @abstractmethod
    def get(self, scenario_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Scenario:
        """
        Get Scenario , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param scenario_id: id of Scenario
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Scenario object
        """
        pass


    @abstractmethod
    def get_all(self, lang: str = None) -> list:
        """
        Get list of Scenario for selected lang
        :param lang: lang of Scenario
        :return: list of Scenario
        """
        pass


    @abstractmethod
    def create_empty(self, lang: str) -> Monster:
        pass
