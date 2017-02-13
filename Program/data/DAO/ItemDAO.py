from data.DAO.interface.IItemDAO import *
from data.database.Database import *


class ItemDAO(IItemDAO):
    DATABASE_TABLE = 'Item'


    def __init__(self):
        self.database = Database(':memory:')


    def create_item(self, item: Item):
        int_values = {
            'parent_id': item.parent_id,
            'weight': item.weight,
            'price': item.price,
            'amount': item.amount,
            'type': 'Money'
        }
        id = self.database.insert(self.DATABASE_TABLE, int_values)

        str_values = {
            'name': item.name,
            'description': item.description,
        }

        for name, value in str_values.items():
            trans_values = {
                'language_code': item.lang,
                'target_id': id,
                'name': name,
                'value': value,
                'type': 'Item',
            }
            self.database.insert('translates', trans_values)


    def update_item(self, item: Item):
        if item.id is None:
            raise ValueError('Cant update none existing item')

        result = self.database.select(self.DATABASE_TABLE, {'ID': item.id})
        if not result:
            raise ValueError('Cant update none existing item')

        int_values = {
            'parent_id': item.parent_id,
            'price': item.price,
            'weight': item.weight,
        }

        self.database.update(self.DATABASE_TABLE, item.id, int_values)

        str_values = {
            'name': item.description,
            'description': item.description
        }


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
        tr_data = self.database.select_translate(item_id, 'Item', lang)
        item = Item(item_id, lang, tr_data['name'], tr_data['description'],
                    data['parent_id'], data['weight'], data['price'])

        return item
