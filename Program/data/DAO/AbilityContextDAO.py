from data.DAO.DAO import DAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.effects.AbilityContext import AbilityContext
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.ObjectType import ObjectType
from structure.tree.NodeObject import NodeObject


class AbilityContextDAO(DAO):
    DATABASE_TABLE = 'AbilityContext'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.ABILITY_CONTEXT


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)
        self.obj_database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, context: AbilityContext, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        intValues = {
            'value'          : context.value,
            'valueType'      : context.valueType.value if context.valueType else None,
            'targetAttribute': context.targetAttribute.value if context.targetAttribute else None
        }

        strValues = {
            'name'       : context.name,
            'description': context.description
        }

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        context.id = id

        self.obj_database.insert_translate(strValues, context.lang, id, self.TYPE)

        # Create node for tree structure
        node = NodeObject(None, context.name, nodeParentId, context)
        self.treeDAO.insert_node(node, contextType)

        return id


    def update(self, context: AbilityContext) -> None:
        intValues = {
            'value'          : context.value,
            'valueType'      : context.valueType.value if context.valueType else None,
            'targetAttribute': context.targetAttribute.value if context.targetAttribute else None
        }

        strValues = {
            'name'       : context.name,
            'description': context.description
        }

        self.database.update(self.DATABASE_TABLE, context.id, intValues)
        self.obj_database.update_translate(strValues, context.lang, context.id, self.TYPE)


    def delete(self, context_id: int) -> None:
        self.obj_database.delete(self.DATABASE_TABLE, context_id)
        self.database.delete_where('translates',
                                   {'target_id': context_id, 'type': ObjectType.ABILITY_CONTEXT})


    def get(self, context_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> AbilityContext:
        if lang is None:
            lang = 'cs'  # TODO: default lang

        data = dict(self.obj_database.select(self.DATABASE_TABLE, {'ID': context_id})[0])
        tr_data = dict(self.database.select_translate(context_id, self.TYPE.value, lang))

        valueType = ModifierValueTypes(data['valueType']) if data['valueType'] else None
        targetAttribute = CharacterAttributes(data['targetAttribute']) if data['targetAttribute'] else None

        context = AbilityContext(data['ID'], lang, tr_data.get('name', ''),
                                 tr_data.get('description', ''), valueType, data.get('value', 0),
                                 targetAttribute)
        return context


    def get_all(self) -> list:
        return []


        # def get_link(self, abilityId):
        #     data = self.database.select('Ability_context', {'ability_id': abilityId})
        #
        #     contexts = []
        #     for i in data:
        #         contexts.append(self.get(i['context_id']))
        #
        #     return contexts
        #
        #
        #
