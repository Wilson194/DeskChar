from data.DAO.DAO import DAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
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
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.MODIFIER


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)
        self.obj_database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, modifier: Modifier, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        print(modifier.itemTargetAttribute)
        intValues = {
            'value'                   : modifier.value,
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
        intValues = {
            'value'                   : modifier.value,
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
        self.obj_database.delete(self.DATABASE_TABLE, modifier_id)
        self.database.delete_where('translates',
                                   {'target_id': modifier_id, 'type': ObjectType.MODIFIER})


    def get(self, modifier_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Modifier:
        if lang is None:
            lang = 'cs'  # TODO: default lang

        data = dict(self.obj_database.select(self.DATABASE_TABLE, {'ID': modifier_id})[0])
        tr_data = dict(self.database.select_translate(modifier_id, ObjectType.MODIFIER.value, lang))

        targetTypeIndex = data.get('targetType', None)
        targetType = ModifierTargetTypes(int(targetTypeIndex)) if targetTypeIndex is not None else None

        characterAttributeIndex = data.get('characterTargetAttribute', None)
        itemAttributeIndex = data.get('itemTargetAttribute', None)

        characterTargetAttribute = CharacterAttributes(characterAttributeIndex) if characterAttributeIndex is not None else None

        itemTargetAttribute = ItemsAttributes(itemAttributeIndex) if itemAttributeIndex is not None else None

        valueTypeIndex = data.get('valueType', None)
        value = data.get('value', 0)
        if itemTargetAttribute is ItemsAttributes.WEAPON_MELEE_HANDLING:
            valueType = Handling(valueTypeIndex)
            value = value
        elif itemTargetAttribute is ItemsAttributes.WEAPON_WEIGHT:
            valueType = WeaponWeight(valueTypeIndex)
            value = value

        elif itemTargetAttribute is ItemsAttributes.ARMOR_SIZE:
            valueType = ArmorSize(valueTypeIndex)
            value = value
        else:
            valueType = ModifierValueTypes(valueTypeIndex) if valueTypeIndex else None
            value = data.get('value', 0)

        modifier = Modifier(modifier_id, lang, tr_data.get('name', ''),
                            tr_data.get('description', ''), valueType, value,
                            characterTargetAttribute, itemTargetAttribute,
                            targetType)

        return modifier


    def get_all(self) -> list:
        return []


        # def get_link(self, effectId):
        #     data = self.database.select('Effect_modifier', {'effect_id': effectId})
        #
        #     modifiers = []
        #     for i in data:
        #         modifiers.append(self.get(i['modifier_id']))
        #
        #     return modifiers
