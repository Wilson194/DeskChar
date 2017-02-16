from data.DAO.interface.ISpellDAO import *
from database.ObjectDatabase import *


class SpellDAO(ISpellDAO):
    DATABASE_TABLE = 'Spell'
    DATABASE_DRIVER = 'test.db'


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
        data = self.database.select(self.DATABASE_TABLE, {'ID': spell_id})[0]
        tr_data = self.database.select_translate(spell_id, self.DATABASE_TABLE,
                                                 lang)
        ability = Spell(spell_id, lang, tr_data['name'],
                        tr_data['description'], tr_data['mana_cost_initial'],
                        tr_data['mana_cost_continual'], tr_data['range'],
                        tr_data['scope'], data['cast_time'],
                        tr_data['duration'])

        return ability


    def get_all_spells(self, lang=None) -> list:
        if lang is None:
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)
        items = []
        for line in lines:
            item = self.get_spell(line['ID'], lang)
            items.append(item)
        return items
