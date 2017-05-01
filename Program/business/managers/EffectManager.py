from business.managers.interface.IEffectManager import IEffectManager
from data.DAO.EffectDAO import EffectDAO
from structure.effects.Effect import Effect
from structure.enums.ObjectType import ObjectType


class EffectManager(IEffectManager):
    def __init__(self):
        self.DAO = EffectDAO()


    def create(self, effect: Effect, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        return self.DAO.create(effect, nodeParentId, contextType)


    def update(self, effect: Effect) -> None:
        return self.DAO.update(effect)


    def delete(self, effectId: int) -> None:
        return self.DAO.delete(effectId)


    def get(self, effectId: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Effect:
        return self.DAO.get(effectId, lang, nodeId, contextType)


    def get_all(self, lang: str) -> list:
        return self.DAO.get_all(lang)


    def update_effect(self, effect: Effect):
        return self.DAO.update(effect)


    def create_empty(self, lang: str) -> Effect:
        character = Effect(None, lang)
        id = self.DAO.create(character)
        character.id = id

        return character
