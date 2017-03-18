from data.DAO.DAO import DAO
from data.DAO.interface.IModifierDAO import IModifierDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.effects.Modifier import Modifier
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.Handling import Handling
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.ObjectType import ObjectType
from structure.enums.WeaponWeight import WeaponWeight


class ModifierDAO(DAO, IModifierDAO):
    DATABASE_TABLE = 'Modifier'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.MODIFIER


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)
        self.obj_database = ObjectDatabase(self.DATABASE_DRIVER)


    def create(self, modifier: Modifier) -> int:
        return self.obj_database.insert_object(modifier)


    def update(self, modifier: Modifier) -> None:
        self.obj_database.update_object(modifier)


    def delete(self, modifier_id: int) -> None:
        self.obj_database.delete(self.DATABASE_TABLE, modifier_id)


    def get(self, modifier_id: int, lang: str = None) -> Modifier:
        if lang is None:
            lang = 'cs'  # TODO: default lang

        data = dict(self.obj_database.select(self.DATABASE_TABLE, {'ID': modifier_id})[0])
        tr_data = dict(self.database.select_translate(modifier_id, ObjectType.MODIFIER.value, lang))

        targetTypeIndex = data.get('targetType', None)
        targetType = ModifierTargetTypes(
            int(targetTypeIndex)) if targetTypeIndex is not None else None

        targetAttributeIndex = data.get('valueTargetAttribute', None)
        if targetType is ModifierTargetTypes.CHARACTER:
            targetAttribute = CharacterAttributes(targetAttributeIndex)
        elif targetType is ModifierTargetTypes.ITEM:
            targetAttribute = ItemsAttributes(targetAttributeIndex)
        else:
            return Modifier(modifier_id, lang)

        valueTypeIndex = data.get('valueType', None)
        value = data.get('value',0)
        if targetAttribute is ItemsAttributes.WEAPON_MELEE_HANDLING:
            valueType = Handling(value)
            value = value
        elif targetAttribute is ItemsAttributes.WEAPON_WEIGHT:
            valueType = WeaponWeight(value)
            value = value
        else:
            valueType = ModifierValueTypes(int(valueTypeIndex))
            value = data.get('value', 0)

        modifier = Modifier(modifier_id, lang, tr_data.get('name', ''),
                            tr_data.get('description', ''), valueType, value, targetAttribute,
                            targetType)

        return modifier


    def get_all(self) -> list:
        return []
