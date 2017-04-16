from data.DAO.DAO import DAO
from data.DAO.interface.IModifierDAO import IModifierDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.effects.AbilityContext import AbilityContext
from structure.effects.Modifier import Modifier
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.Handling import Handling
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.ObjectType import ObjectType
from structure.enums.WeaponWeight import WeaponWeight


class AbilityContextDAO(DAO):
    DATABASE_TABLE = 'AbilityContext'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.ABILITY_CONTEXT


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)
        self.obj_database = ObjectDatabase(self.DATABASE_DRIVER)


    def create(self, context: AbilityContext) -> int:
        return self.obj_database.insert_object(context)


    def update(self, context: AbilityContext) -> None:
        self.obj_database.update_object(context)


    def delete(self, context_id: int) -> None:
        self.obj_database.delete(self.DATABASE_TABLE, context_id)
        self.database.delete_where('translates',
                                   {'target_id': context_id, 'type': self.TYPE})


    def get(self, context_id: int, lang: str = None) -> AbilityContext:
        if lang is None:
            lang = 'cs'  # TODO: default lang

        data = dict(self.obj_database.select(self.DATABASE_TABLE, {'ID': context_id})[0])
        tr_data = dict(self.database.select_translate(context_id, self.TYPE.value, lang))

        valueType = ModifierValueTypes(data['valueType']) if data['valueType'] else None
        targetAttribute = CharacterAttributes(data['targetAttribute']) if data[
            'targetAttribute'] else None

        context = AbilityContext(data['ID'], lang, tr_data.get('name', ''),
                                 tr_data.get('description', ''), valueType, data.get('value', 0),
                                 targetAttribute)
        return context


    def get_link(self, abilityId):
        data = self.database.select('Ability_context', {'ability_id': abilityId})

        contexts = []
        for i in data:
            contexts.append(self.get(i['context_id']))

        return contexts


    def get_all(self) -> list:
        return []
