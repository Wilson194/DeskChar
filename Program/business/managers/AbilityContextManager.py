from business.managers.interface.IAbilityContextManager import IAbilityContextManager
from data.DAO.AbilityContextDAO import AbilityContextDAO
from structure.effects.AbilityContext import AbilityContext
from structure.enums.ObjectType import ObjectType


class AbilityContextManager(IAbilityContextManager):
    def __init__(self):
        self.DAO = AbilityContextDAO()


    def create(self, context: AbilityContext, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        return self.DAO.create(context, nodeParentId, contextType)


    def update(self, context: AbilityContext) -> None:
        return self.DAO.update(context)


    def delete(self, contextId: int) -> None:
        return self.DAO.delete(contextId)


    def get(self, contextId: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> AbilityContext:
        return self.DAO.get(contextId, lang, nodeId, contextType)


    def get_all(self, lang: str = None) -> list:
        return self.DAO.get_all(lang)


    def create_empty(self, lang: str) -> AbilityContext:
        ability = AbilityContext(None, lang)
        id = self.DAO.create(ability)
        ability.id = id

        return ability
