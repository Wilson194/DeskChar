from data.DAO.ScenarioDAO import ScenarioDAO
from structure.scenario.Scenario import Scenario


class ScenarioManager:
    def __init__(self):
        self.DAO = ScenarioDAO()


    def update_scenario(self, scenario: Scenario):
        self.DAO.update(scenario)
