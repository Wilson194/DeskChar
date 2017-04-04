from data.DAO.DAO import DAO
from data.DAO.interface.IAbilityDAO import IAbilityDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.abilities.Ability import Ability
from structure.enums.ObjectType import ObjectType
from structure.enums.Races import Races


class AbilityDAO(DAO, IAbilityDAO):
    DATABASE_TABLE = 'Ability'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.ABILITY


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, ability: Ability) -> int:
        """
        Create new ability in database
        :param ability: Ability object
        :return: id of autoincrement
        """
        return ObjectDatabase(self.DATABASE_DRIVER).insert_object(ability)


    def update(self, ability: Ability):
        """
        Update ability in database
        :param ability: Ability object with new data
        """
        ObjectDatabase(self.DATABASE_DRIVER).update_object(ability)


    def delete(self, ability_id: int):
        """
        Delete ability from database and all from translate
        :param ability_id: id of ability
        """
        self.database.delete(self.DATABASE_TABLE, ability_id)
        self.database.delete_where('translates',
                                   {'target_id': ability_id, 'type': 'Item'})


    def get(self, ability_id: int, lang=None) -> Ability:
        """
        Get ability from database
        :param ability_id: id of ability
        :param lang: lang of ability
        :return: Ability object
        """
        if lang is None:  # TODO: default lang
            lang = 'cs'
        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': ability_id})[0])
        tr_data = self.database.select_translate(ability_id, ObjectType.ABILITY.value, lang)

        drd_class = Races(data.get('drd_class')) if data.get('drd_class') is not None else None
        drd_race = Races(data.get('drd_race')) if data.get('drd_race') is not None else None
        ability = Ability(ability_id, lang, tr_data.get('name', ''),
                          tr_data.get('description', ''), tr_data.get('chance', ''),
                          drd_race, drd_class)

        return ability


    def get_all(self, lang=None) -> list:
        """
        Get list of abilities for selected lang
        :param lang: lang of abilities
        :return: list of abilities
        """
        if lang is None:  # TODO: default lang
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)

        items = []
        for line in lines:
            item = self.get(line['ID'], lang)
            items.append(item)
        return items
