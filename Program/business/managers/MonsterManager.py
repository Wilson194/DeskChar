from data.DAO.AbilityDAO import AbilityDAO
from structure.abilities.Ability import Ability


class MonsterManager:
    def __init__(self):
        self.DAO = AbilityDAO()


    def update_ability(self, ability: Ability):
        self.DAO.update(ability)


    def create_empty(self, lang):
        ability = Ability(None, lang)
        id = self.DAO.create(ability)
        ability.id = id

        return ability
