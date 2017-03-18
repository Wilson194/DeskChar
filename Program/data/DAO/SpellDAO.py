from data.DAO.interface.ISpellDAO import ISpellDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.enums.Classes import Classes
from structure.enums.ObjectType import ObjectType
from structure.spells.Spell import Spell
from data.DAO.DAO import DAO


class SpellDAO(DAO, ISpellDAO):
    DATABASE_TABLE = 'Spell'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.SPELL


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, spell: Spell) -> int:
        """
        Create new spell in database
        :param spell: Spell object
        :return: id of autoincrement
        """
        return ObjectDatabase(self.DATABASE_DRIVER).insert_object(spell)


    def update(self, spell: Spell):
        """
        Update spell in database
        :param spell: Spell object with new data
        """
        ObjectDatabase(self.DATABASE_DRIVER).update_object(spell)


    def delete(self, spell_id: int):
        """
        Delete spell from database and all his translates
        :param spell_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, spell_id)
        self.database.delete_where('translates',
                                   {'target_id': spell_id, 'type': 'Item'})


    def get(self, spell_id: int, lang: str = None) -> Spell:
        """
        Get spell from database
        :param spell_id: id of spell
        :param lang: lang of spell
        :return: Spell object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': spell_id})[0])
        tr_data = self.database.select_translate(spell_id, ObjectType.SPELL.value,
                                                 lang)
        drdClassIndex = data.get('drd_class', None)
        drdClass = Classes(drdClassIndex) if drdClassIndex is not None else None
        spell = Spell(spell_id, lang, tr_data.get('name', ''),
                      tr_data.get('description', ''), tr_data.get('mana_cost_initial', ''),
                      tr_data.get('mana_cost_continual', ''), tr_data.get('range', ''),
                      tr_data.get('scope', ''), data.get('cast_time', 0),
                      tr_data.get('duration', ''), drdClass)

        return spell


    def get_all(self, lang=None) -> list:
        """
        Get list of all spells from database, only one lang
        :param lang: lang code
        :return: list of Spells
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)
        items = []
        for line in lines:
            item = self.get(line['ID'], lang)
            items.append(item)
        return items


    def get_languages(self, id: int) -> list:
        """
        Get list of all languages codes for this spell
        :param id: id of spell
        :return: list of langs codes
        """
        data = self.database.select('translates', {'target_id': id, 'type': ObjectType.SPELL.value})
        languages = []
        for line in data:
            if line['lang'] not in languages:
                languages.append(line['lang'])
        return languages


    def get_all_data(self, spell_id: int) -> dict:
        """
        Get all data dictionary of one spell, all langs
        :param spell_id: id of spell
        :return: dictionary of all data
        """
        data = {}
        int_data = dict(self.database.select(self.DATABASE_TABLE, {'ID': spell_id})[0])
        tr_data = self.database.select('translates',
                                       {'target_id': spell_id, 'type': ObjectType.SPELL.value})
        for key, value in int_data.items():
            data[key] = value

        for line in tr_data:
            name = line['name']
            lang = line['lang']
            value = line['value']

            if name in data:
                data[name][lang] = value
            else:
                data[name] = {}
                data[name][lang] = value

        return data
