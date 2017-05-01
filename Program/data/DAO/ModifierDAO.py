from data.DAO.DAO import DAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.SettingsDAO import SettingsDAO
from data.DAO.interface.IModifierDAO import IModifierDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.effects.Modifier import Modifier
from structure.enums.ArmorSize import ArmorSize
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.Handling import Handling
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.ObjectType import ObjectType
from structure.enums.WeaponWeight import WeaponWeight
from structure.tree.NodeObject import NodeObject


class ModifierDAO(DAO, IModifierDAO):
    DATABASE_TABLE = 'Modifier'
    TYPE = ObjectType.MODIFIER


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)
        self.obj_database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, modifier: Modifier, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new Modifier
        :param modifier: Modifier object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created Modifier
        """
        if not contextType:
            contextType = self.TYPE

        if modifier.valueType is ModifierValueTypes.TYPE_ARMOR_SIZE:
            value = ArmorSize.by_name(ArmorSize, modifier.value).value
        elif modifier.valueType is ModifierValueTypes.TYPE_WEAPON_HANDLING:
            value = Handling.by_name(Handling, modifier.value).value
        elif modifier.valueType is ModifierValueTypes.TYPE_WEAPON_WEIGHT:
            value = WeaponWeight.by_name(WeaponWeight, modifier.value).value
        else:
            value = modifier.value

        intValues = {
            'value'                   : value,
            'valueType'               : modifier.valueType.value if modifier.valueType else None,
            'targetType'              : modifier.targetType.value if modifier.targetType else None,
            'characterTargetAttribute': modifier.characterTargetAttribute.value if modifier.characterTargetAttribute else None,
            'itemTargetAttribute'     : modifier.itemTargetAttribute.value if modifier.itemTargetAttribute else None
        }

        strValues = {
            'name'        : modifier.name,
            'desccription': modifier.description
        }

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        modifier.id = id

        self.obj_database.insert_translate(strValues, modifier.lang, id, self.TYPE)

        # Create node for tree structure
        node = NodeObject(None, modifier.name, nodeParentId, modifier)
        self.treeDAO.insert_node(node, contextType)

        return id


    def update(self, modifier: Modifier) -> None:
        """
        Update modifier in database
        :param modifier: Modifier object with new data
        """

        intValues = {
            'value'                   : modifier.value if type(modifier.value) is int else modifier.value.value,
            'valueType'               : modifier.valueType.value if modifier.valueType else None,
            'targetType'              : modifier.targetType.value if modifier.targetType.value else None,
            'characterTargetAttribute': modifier.characterTargetAttribute.value if modifier.characterTargetAttribute else None,
            'itemTargetAttribute'     : modifier.itemTargetAttribute.value if modifier.itemTargetAttribute else None
        }

        strValues = {
            'name'        : modifier.name,
            'desccription': modifier.description
        }

        self.database.update(self.DATABASE_TABLE, modifier.id, intValues)
        self.obj_database.update_translate(strValues, modifier.lang, modifier.id, self.TYPE)


    def delete(self, modifier_id: int) -> None:
        """
        Delete Modifier from database and all his translates
        :param modifier_id: id of Modifier
        """
        self.obj_database.delete(self.DATABASE_TABLE, modifier_id)
        self.database.delete_where('translates',
                                   {'target_id': modifier_id, 'type': ObjectType.MODIFIER})


    def get(self, modifier_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Modifier:
        """
        Get Modifier , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param modifier_id: id of Modifier
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Modifier object
        """
        if lang is None:
            lang = SettingsDAO().get_value('language', str)

        data = self.obj_database.select(self.DATABASE_TABLE, {'ID': modifier_id})
        if not data:
            return None
        else:
            data = dict(data[0])

        tr_data = dict(self.database.select_translate(modifier_id, ObjectType.MODIFIER.value, lang))

        targetTypeIndex = data.get('targetType', None)
        targetType = ModifierTargetTypes(int(targetTypeIndex)) if targetTypeIndex is not None else None

        characterAttributeIndex = data.get('characterTargetAttribute', None)
        itemAttributeIndex = data.get('itemTargetAttribute', None)

        characterTargetAttribute = CharacterAttributes(characterAttributeIndex) if characterAttributeIndex is not None else None
        itemTargetAttribute = ItemsAttributes(itemAttributeIndex) if itemAttributeIndex is not None else None

        valueTypeIndex = data.get('valueType', None)
        valueType = ModifierValueTypes(valueTypeIndex) if valueTypeIndex else None

        value = data.get('value', 0)
        if valueType is ItemsAttributes.WEAPON_MELEE_HANDLING:
            value = Handling(value)
        elif valueType is ItemsAttributes.WEAPON_WEIGHT:
            value = WeaponWeight(value)
        elif valueType is ItemsAttributes.ARMOR_SIZE:
            valueType = ArmorSize(value)
        else:
            value = value

        modifier = Modifier(modifier_id, lang, tr_data.get('name', ''),
                            tr_data.get('description', ''), valueType, value,
                            characterTargetAttribute, itemTargetAttribute,
                            targetType)

        return modifier


    def get_all(self, lang: str = None) -> list:
        """
        Get list of modifiers for selected lang
        :param lang: lang of modifiers
        :return: list of modifiers
        """
        if lang is None:
            lang = SettingsDAO().get_value('language', str)
        lines = self.database.select_all('Item')

        modifiers = []
        for line in lines:
            item = self.get(line['ID'], lang)
            modifiers.append(item)
        return modifiers
