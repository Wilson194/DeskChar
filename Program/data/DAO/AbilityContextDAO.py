from data.DAO.DAO import DAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.interface.IAbilityContextDAO import IAbilityContextDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.effects.AbilityContext import AbilityContext
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.ObjectType import ObjectType
from structure.tree.NodeObject import NodeObject


class AbilityContextDAO(DAO, IAbilityContextDAO):
    DATABASE_TABLE = 'AbilityContext'
    TYPE = ObjectType.ABILITY_CONTEXT


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)
        self.obj_database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, context: AbilityContext, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new ability context
        :param context: Ability context object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created ability context
        """
        if contextType is None:
            contextType = self.TYPE

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
        """
        Update Ability context with new values
        :param context: Ability context object with new values    
        """
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
        """
        Delete ability context from database
        :param context_id: id of context 
        :return: 
        """
        self.obj_database.delete(self.DATABASE_TABLE, context_id)
        self.database.delete_where('translates',
                                   {'target_id': context_id, 'type': ObjectType.ABILITY_CONTEXT})


    def get(self, context_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> AbilityContext:
        """
        Get ability context, object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all subobjects)
        If not specified, only basic attributes are set.        
        :param context_id: id of ability context
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Ability context object
        """
        if lang is None:
            lang = 'cs'  # TODO: default lang

        data = self.obj_database.select(self.DATABASE_TABLE, {'ID': context_id})
        if not data:
            return None
        else:
            data = dict(data[0])

        tr_data = dict(self.database.select_translate(context_id, self.TYPE.value, lang))

        valueType = ModifierValueTypes(data['valueType']) if data['valueType'] else None
        targetAttribute = CharacterAttributes(data['targetAttribute']) if data['targetAttribute'] else None

        context = AbilityContext(data['ID'], lang, tr_data.get('name', ''),
                                 tr_data.get('description', ''), valueType, data.get('value', 0),
                                 targetAttribute)
        return context


    def get_all(self, lang: str = None) -> list:
        """
        Gel list of all Ability context
        :param lang: lang of objects
        :return: list of Ability context
        """
        if lang is None:  # TODO: default lang
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)

        items = []
        for line in lines:
            item = self.get(line['ID'], lang)
            items.append(item)
        return items
