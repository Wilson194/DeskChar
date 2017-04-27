from data.DAO.DAO import DAO
from data.DAO.ModifierDAO import ModifierDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.interface.IEffectDAO import IEffectDAO

from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.effects.Effect import Effect
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ObjectType import ObjectType
from structure.tree.NodeObject import NodeObject


class EffectDAO(DAO, IEffectDAO):
    DATABASE_TABLE = 'Effect'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.EFFECT


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)
        self.obj_database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, effect: Effect, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        if not contextType:
            contextType = self.TYPE

        if type(effect.active) is str:
            active = True if effect.active == 'true' else False
        else:
            active = effect.active

        intValues = {
            'targetType': effect.targetType.value if effect.targetType else None,
            'active'    : int(active) if active else 0
        }

        strValues = {
            'name'       : effect.name,
            'description': effect.description
        }

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        effect.id = id

        self.obj_database.insert_translate(strValues, effect.lang, id, self.TYPE)

        # Create node for tree structure
        node = NodeObject(None, effect.name, nodeParentId, effect)
        nodeId = self.treeDAO.insert_node(node, contextType)

        for modifier in effect.modifiers:
            ModifierDAO().create(modifier, nodeId, contextType)
        return id


    def update(self, effect: Effect) -> None:
        if type(effect.active) is str:
            active = True if effect.active == 'true' else False
        else:
            active = effect.active

        intValues = {
            'targetType': effect.targetType.value if effect.targetType else None,
            'active'    : int(active)
        }

        strValues = {
            'name'       : effect.name,
            'description': effect.description
        }

        self.database.update(self.DATABASE_TABLE, effect.id, intValues)
        self.obj_database.update_translate(strValues, effect.lang, effect.id, self.TYPE)


    def delete(self, effect_id: int) -> None:
        self.obj_database.delete(self.DATABASE_TABLE, effect_id)
        self.database.delete_where('translates',
                                   {'target_id': effect_id, 'type': ObjectType.EFFECT})


    def get(self, effect_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Effect:
        if lang is None:  # TODO : default lang
            lang = 'cs'

        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': effect_id})[0])
        tr_data = self.database.select_translate(effect_id, ObjectType.EFFECT.value, lang)

        index = data.get('targetType', 1) if data.get('targetType', 1) is not None else 1
        targetType = ModifierTargetTypes(index)
        effect = Effect(effect_id, lang, tr_data.get('name', ''), tr_data.get('description', ''),
                        targetType, bool(data.get('active', 0)))

        if nodeId and contextType:
            children = self.treeDAO.get_children_objects(nodeId, contextType)

            modifiers = []
            for child in children:
                if child.object.object_type is ObjectType.MODIFIER:
                    modifiers.append(ModifierDAO().get(child.object.id, None, child.id, contextType))
            effect.modifiers = modifiers
        return effect


    def get_all(self) -> list:
        return []
