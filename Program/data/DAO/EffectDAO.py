from data.DAO.DAO import DAO
from data.DAO.ModifierDAO import ModifierDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.SettingsDAO import SettingsDAO
from data.DAO.interface.IEffectDAO import IEffectDAO

from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.effects.Effect import Effect
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ObjectType import ObjectType
from structure.tree.NodeObject import NodeObject


class EffectDAO(DAO, IEffectDAO):
    DATABASE_TABLE = 'Effect'
    TYPE = ObjectType.EFFECT


    def __init__(self):
        self.database = ObjectDatabase(self.DATABASE_DRIVER)
        # self.obj_database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, effect: Effect, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new effect
        :param effect: Effect object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created effect
        """
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

        self.database.insert_translate(strValues, effect.lang, id, self.TYPE)

        # Create node for tree structure
        node = NodeObject(None, effect.name, nodeParentId, effect)
        nodeId = self.treeDAO.insert_node(node, contextType)

        for modifier in effect.modifiers:
            ModifierDAO().create(modifier, nodeId, contextType)
        return id


    def update(self, effect: Effect) -> None:
        """
        Update effect in database
        :param effect: Effect object with new data
        """
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
        self.database.update_translate(strValues, effect.lang, effect.id, self.TYPE)


    def delete(self, effect_id: int) -> None:
        """
        Delete Effect from database and from translate
        :param effect_id: id of effect
        """
        self.database.delete(self.DATABASE_TABLE, effect_id)
        self.database.delete_where('translates',
                                   {'target_id': effect_id, 'type': ObjectType.EFFECT})


    def get(self, effect_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Effect:
        """
        Get Effect , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param effect_id: id of Effect
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Effect object
        """
        if lang is None:
            lang = SettingsDAO().get_value('language', str)

        data = self.database.select(self.DATABASE_TABLE, {'ID': effect_id})
        if not data:
            return None
        else:
            data = dict(data[0])
        tr_data = self.database.select_translate(effect_id, self.TYPE.value, lang)

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


    def get_all(self, lang=None) -> list:
        """
        Get list of effects for selected lang
        :param lang: lang of effects
        :return: list of effects
        """
        if lang is None:
            lang = SettingsDAO().get_value('language', str)
        lines = self.database.select_all(self.DATABASE_TABLE)
        effects = []
        for line in lines:
            character = self.get(line['ID'], lang)
            effects.append(character)
        return effects
