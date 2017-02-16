from data.DAO.interface.IAbilityDAO import *
from data.database.ObjectDatabase import *


class AbilityDAO(IAbilityDAO):
    DATABASE_TABLE = 'Ability'


    def __init__(self):
        self.database = Database(':memory:')


    def create_ability(self, ability: Ability) -> int:
        return ObjectDatabase(':memory:').insert_object(ability)


    def update_ability(self, ability: Ability) -> None:
        ObjectDatabase(':memory:').update_object(ability)


    def delete_ability(self, ability_id: int) -> None:
        self.database.delete(self.DATABASE_TABLE, ability_id)
        self.database.delete_where('translates',
                                   {'target_id': ability_id, 'type': 'Item'})


    def get_ability(self, ability_id: int, lang=None) -> Ability:
        if lang is None:
            lang = 'cs'
        data = self.database.select(self.DATABASE_TABLE, {'ID': ability_id})[0]
        tr_data = self.database.select_translate(ability_id, 'Item', lang)
        ability = Ability(ability_id, lang, tr_data['name'],
                          tr_data['description'], data['chance'])

        return ability


    def get_all_abilities(self, lang=None) -> list:
        if lang is None:
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)

        items = []
        for line in lines:
            item = self.get_ability(line['ID'], lang)
            items.append(item)
        return items
