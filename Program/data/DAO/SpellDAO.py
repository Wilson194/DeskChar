from data.DAO.interface.ISpellDAO import *
from database.ObjectDatabase import *
from structure.enums.ObjectType import ObjectType


class SpellDAO(ISpellDAO):
    DATABASE_TABLE = 'Spell'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.SPELL


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create_spell(self, spell: Spell) -> int:
        return ObjectDatabase(self.DATABASE_DRIVER).insert_object(spell)


    def update_spell(self, spell: Spell) -> None:
        ObjectDatabase(self.DATABASE_DRIVER).update_object(spell)


    def delete_spell(self, spell_id: int) -> None:
        self.database.delete(self.DATABASE_TABLE, spell_id)
        self.database.delete_where('translates',
                                   {'target_id': spell_id, 'type': 'Item'})


    def get_spell(self, spell_id: int, lang: str = None) -> Spell:
        if lang is None:
            lang = 'cs'
        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': spell_id})[0])
        tr_data = self.database.select_translate(spell_id, self.DATABASE_TABLE,
                                                 lang)

        spell = Spell(spell_id, lang, tr_data.get('name', ''),
                      tr_data.get('description', ''), tr_data.get('mana_cost_initial', ''),
                      tr_data.get('mana_cost_continual', ''), tr_data.get('range', ''),
                      tr_data.get('scope', ''), data.get('cast_time', ''),
                      tr_data.get('duration', ''))

        return spell


    def get_all_spells(self, lang=None) -> list:
        if lang is None:
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)
        items = []
        for line in lines:
            item = self.get_spell(line['ID'], lang)
            items.append(item)
        return items


    def get_languages(self, id):
        data = self.database.select('translates', {'target_id': id, 'type': 'Spell'})
        languages = []
        for line in data:
            if line['lang'] not in languages:
                languages.append(line['lang'])
        return languages