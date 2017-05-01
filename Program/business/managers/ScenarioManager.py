from business.managers.interface.IScenarioManager import IScenarioManager
from data.DAO.ScenarioDAO import ScenarioDAO
from structure.enums.ObjectType import ObjectType
from structure.scenario.Scenario import Scenario


class ScenarioManager(IScenarioManager):
    def __init__(self):
        self.DAO = ScenarioDAO()


    def create(self, scenario: Scenario, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        return self.DAO.create(scenario, nodeParentId, contextType)


    def update_scenario(self, scenario: Scenario):
        return self.DAO.update(scenario)


    def delete(self, scenarioId: int):
        return self.DAO.delete(scenarioId)


    def get(self, scenarioId: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Scenario:
        return self.DAO.get(scenarioId, lang, nodeId, contextType)


    def get_all(self, lang=None) -> list:
        return self.DAO.get_all(lang)


    def create_empty(self, lang):
        item = Scenario(None, lang)
        id = self.DAO.create(item)
        item.id = id

        return item
