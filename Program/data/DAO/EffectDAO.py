from data.DAO.DAO import DAO
from data.DAO.ModifierDAO import ModifierDAO
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
        self.database.delete_where('translates',
                                   {'target_id': effect_id, 'type': ObjectType.EFFECT})


    def get(self, effect_id: int, lang: str = None) -> Effect:

        if lang is None:  # TODO : default lang
            lang = 'cs'
        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': effect_id})[0])
        tr_data = self.database.select_translate(effect_id, ObjectType.EFFECT.value, lang)

        index = data.get('targetType', 1) if data.get('targetType', 1) is not None else 1
        targetType = ModifierTargetTypes(index)
        effect = Effect(effect_id, lang, tr_data.get('name', ''), tr_data.get('description', ''),
                        targetType)

        effect.modifiers = self.get_modifiers(effect_id)

        return effect


    def get_all(self) -> list:
        return []


    def delete_link(self, object, target):
        objects = self.database.select('Effect_modifiers',
                                       {'effect_id': object.id, 'modifier_id': target.id})
        if objects:
            self.database.delete('Effect_modifiers', objects[0]['ID'])


    def create_link(self, object, target):
        self.database.insert('Effect_modifier',
                             {'effect_id': object.id, 'modifier_id': target.id})


    def get_link(self, item_id, item_type):
        data = self.database.select('Item_effect',
                                    {'item_id': item_id, 'item_type': item_type.value})

        effects = []
        for i in data:
            effects.append(self.get(i['effect_id']))

        return effects


    def get_modifiers(self, object_id):
        datas = self.database.select('Effect_modifier', {'effect_id': object_id})
        modifiers = []
        for one in datas:
            modifiers.append(ModifierDAO().get(one['modifier_id']))

        return modifiers
