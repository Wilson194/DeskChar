from business.managers.interface.IModifierManager import IModifierManager
from data.DAO.ModifierDAO import ModifierDAO
from structure.effects.Modifier import Modifier
from structure.enums.ObjectType import ObjectType


class ModifierManager(IModifierManager):
    def __init__(self):
        self.DAO = ModifierDAO()


    def create(self, modifier: Modifier, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        return self.DAO.create(modifier, nodeParentId, contextType)


    def update(self, modifier: Modifier):
        return self.DAO.update(modifier)


    def delete(self, modifierId: int) -> None:
        return self.DAO.delete(modifierId)


    def get(self, modifierId: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Modifier:
        return self.DAO.get(modifierId, lang, nodeId, contextType)


    def get_all(self, lang: str = None) -> list:
        return self.DAO.get_all(lang)


    def create_empty(self, lang):
        item = Modifier(None, lang)
        id = self.DAO.create(item)
        item.id = id

        return item
