from business.managers.interface.IAbilityManager import IAbilityManager
from data.DAO.AbilityDAO import AbilityDAO
from structure.abilities.Ability import Ability
from structure.enums.ObjectType import ObjectType


class AbilityManager(IAbilityManager):
    def __init__(self):
        self.DAO = AbilityDAO()


    def create(self, ability: Ability, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        return self.DAO.create(ability, nodeParentId, contextType)


    def update_ability(self, ability: Ability):
        self.DAO.update(ability)


    def delete(self, abilityId: int):
        return self.DAO.delete(abilityId)


    def get(self, abilityId: int, lang=None, nodeId: int = None, contextType: ObjectType = None) -> Ability:
        return self.DAO.get(abilityId, lang, nodeId, contextType)


    def get_all(self, lang: str) -> list:
        return self.DAO.get_all(lang)


    def create_empty(self, lang) -> Ability:
        ability = Ability(None, lang)
        id = self.DAO.create(ability)
        ability.id = id

        return ability
