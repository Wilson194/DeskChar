from data.DAO.interface.IAbilityDAO import *
from data.database.ObjectDatabase import *
from structure.enums.ObjectType import ObjectType


class AbilityDAO(IAbilityDAO):
    DATABASE_TABLE = 'Ability'
    DATABASE_DRIVER = 'test.db'


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create_ability(self, ability: Ability) -> int:
        """
        Create new ability in database
        :param ability: Ability object
        :return: id of autoincrement
        """
        return ObjectDatabase(self.DATABASE_DRIVER).insert_object(ability)


    def update_ability(self, ability: Ability):
        """
        Update ability in database
        :param ability: Ability object with new data
        """
        ObjectDatabase(self.DATABASE_DRIVER).update_object(ability)


    def delete_ability(self, ability_id: int):
        """
        Delete ability from database and all from translate
        :param ability_id: id of ability
        """
        self.database.delete(self.DATABASE_TABLE, ability_id)
        self.database.delete_where('translates',
                                   {'target_id': ability_id, 'type': 'Item'})


    def get_ability(self, ability_id: int, lang=None) -> Ability:
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
        ability = Ability(ability_id, lang, tr_data.get('name', ''),
                          tr_data.get('description', ''), tr_data.get('chance', ''),
                          data.get('drd_race', None), data.get('drd_class', None))

        return ability


    def get_all_abilities(self, lang=None) -> list:
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
            item = self.get_ability(line['ID'], lang)
            items.append(item)
        return items


    def get_languages(self, id: int) -> list:
        """
        Get list of all languages of one ability
        :param id: id of ability
        :return: list of language codes
        """
        data = self.database.select('translates',
                                    {'target_id': id, 'type': ObjectType.ABILITY.value})
        languages = []
        for line in data:
            if line['lang'] not in languages:
                languages.append(line['lang'])
        return languages
