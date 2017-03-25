from data.DAO.DAO import DAO
from data.DAO.interface.IEffectDAO import IEffectDAO

from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.effects.Effect import Effect
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ObjectType import ObjectType


class EffectDAO(DAO, IEffectDAO):
    DATABASE_TABLE = 'Effect'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.EFFECT


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)
        self.obj_database = ObjectDatabase(self.DATABASE_DRIVER)


    def create(self, effect: Effect) -> int:
        return self.obj_database.insert_object(effect)


    def update(self, effect: Effect) -> None:
        self.obj_database.update_object(effect)


    def delete(self, effect_id: int) -> None:
        self.obj_database.delete(self.DATABASE_TABLE, effect_id)


    def get(self, effect_id: int, lang: str = None) -> Effect:
        if lang is None:  # TODO : default lang
            lang = 'cs'
        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': effect_id})[0])
        tr_data = self.database.select_translate(effect_id, ObjectType.EFFECT.value, lang)

        index = data.get('targetType', 1) if data.get('targetType', 1) is not None else 1
        targetType = ModifierTargetTypes(index)
        effect = Effect(effect_id, lang, tr_data.get('name', ''), tr_data.get('description', ''),
                        None, targetType)

        return effect


    def get_all(self) -> list:
        return []