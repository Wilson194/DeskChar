from data.DAO.AbilityDAO import AbilityDAO
from structure.abilities.Ability import Ability


class AbilityManager:
    def __init__(self):
        self.DAO = AbilityDAO()


    def update_ability(self, ability: Ability):
        self.DAO.update_ability(ability)


    def create_empty(self, lang):
        ability = Ability(None, lang)
        id = self.DAO.create_ability(ability)
        ability.id = id

        return ability
