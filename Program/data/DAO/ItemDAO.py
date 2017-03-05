from data.DAO.interface.IItemDAO import IItemDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.enums.ObjectType import ObjectType
from structure.items.Item import Item


class ItemDAO(IItemDAO):
    DATABASE_TABLE = 'Item'
    DATABASE_DRIVER = 'test.db'


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create_item(self, item: Item):
        return ObjectDatabase(self.DATABASE_DRIVER).insert_object(item)


    def update_item(self, item: Item):
        ObjectDatabase(self.DATABASE_DRIVER).update_object(item)


    def delete_item(self, item_id: int):
        self.database.delete(self.DATABASE_TABLE, item_id)
        self.database.delete_where('translates',
                                   {'target_id': item_id, 'type': 'Item'})


    def get_all_items(self, lang=None) -> list:
        if lang is None:
            lang = 'cs'
        lines = self.database.select_all('Item')

        items = []
        for line in lines:
            item = self.get_item(line['ID'], lang)
            items.append(item)
        return items


    def get_item(self, item_id: int, lang=None) -> Item:
        if lang is None:
            lang = 'cs'
        data = self.database.select(self.DATABASE_TABLE, {'ID': item_id})[0]
        tr_data = self.database.select_translate(item_id, self.DATABASE_TABLE,
                                                 lang)
        item = Item(item_id, lang, tr_data['name'], tr_data['description'],
                    data['parent_id'], data['weight'], data['price'])

        return item

    def get_languages(self, id: int) -> list:
        """
        Get list of all languages of one item
        :param id: id of item
        :return: list of language codes
        """
        data = self.database.select('translates',
                                    {'target_id': id, 'type': ObjectType.ITEM.value})
        languages = []
        for line in data:
            if line['lang'] not in languages:
                languages.append(line['lang'])
        return languages
