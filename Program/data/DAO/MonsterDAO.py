from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.enums.MonsterRace import MonsterRace
from structure.enums.ObjectType import ObjectType
from structure.monster.Monster import Monster

from data.DAO.DAO import DAO


class MonsterDAO(DAO):
    DATABASE_TABLE = 'Monster'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.MONSTER


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, monster: Monster) -> int:
        """
        Create new spell in database
        :param spell: Spell object
        :return: id of autoincrement
        """
        return ObjectDatabase(self.DATABASE_DRIVER).insert_object(monster)


    def update(self, monster: Monster):
        """
        Update spell in database
        :param spell: Spell object with new data
        """
        ObjectDatabase(self.DATABASE_DRIVER).update_object(monster)


    def delete(self, monster_id: int):
        """
        Delete spell from database and all his translates
        :param spell_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, monster_id)
        self.database.delete_where('translates',
                                   {'target_id': monster_id, 'type': ObjectType.SPELL})


    def get(self, monster_id: int, lang: str = None) -> Monster:
        """
        Get spell from database
        :param spell_id: id of spell
        :param lang: lang of spell
        :return: Spell object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': monster_id})[0])
        tr_data = self.database.select_translate(monster_id, ObjectType.MONSTER.value,
                                                 lang)

        monsterRace = MonsterRace(data['monsterRace']) if data['monsterRace'] else None
        monsterSize = MonsterRace(data['monsterSize']) if data['monsterSize'] else None
        monster = Monster(data['id'], lang, tr_data.get('name', ''), tr_data.get('description', ''),
                          data.get('viability', 0), data.get('offense', 0), data.get('defense', 0),
                          data.get('endurance', 0), data.get('rampnacy', 0),
                          data.get('mobility', 0), data.get('perserverance', 0),
                          data.get('intelligence', 0), data.get('charisma', 0),
                          data.get('conviction', 0), data.get('experience', 0), data.get('hp', 0),
                          monsterRace, monsterSize)

        return monster


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
