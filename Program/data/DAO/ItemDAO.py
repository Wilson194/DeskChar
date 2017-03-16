from data.DAO.DAO import DAO
from data.DAO.interface.IItemDAO import IItemDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.enums.Handling import Handling
from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType
from structure.enums.WeaponWeight import WeaponWeight
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.Item import Item
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon


class ItemDAO(DAO, IItemDAO):
    DATABASE_TABLE = 'Item'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.ITEM


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, item: Item):

        return ObjectDatabase(self.DATABASE_DRIVER).insert_object(item, self.DATABASE_TABLE)


    def update(self, item: Item):
        ObjectDatabase(self.DATABASE_DRIVER).update_object(item, self.DATABASE_TABLE)


    def delete(self, item_id: int):
        self.database.delete(self.DATABASE_TABLE, item_id)
        self.database.delete_where('translates',
                                   {'target_id': item_id, 'type': 'Item'})


    def get_all(self, lang=None) -> list:
        if lang is None:  # TODO : default lang
            lang = 'cs'
        lines = self.database.select_all('Item')

        items = []
        for line in lines:
            item = self.get(line['ID'], lang)
            items.append(item)
        return items


    def get(self, item_id: int, lang=None) -> Item:
        if lang is None:
            lang = 'cs'
        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': item_id})[0])
        tr_data = dict(self.database.select_translate(item_id, ObjectType.ITEM.value,
                                                      lang))
        if data['type'] == Items.GENERIC.value:
            return Item(item_id, lang, tr_data.get('name', ''), tr_data.get('description', ''),
                        data.get('parent_id', 0), data.get('weight', 0), data.get('price', 0))

        if data['type'] == Items.CONTAINER.value:
            return Container(item_id, lang, tr_data.get('name', ''), tr_data.get('description', ''),
                             data.get('parent_id', 0), data.get('weight', 0), data.get('price', 0),
                             data.get('capacity', 0))

        if data['type'] == Items.MELEE_WEAPON.value:
            weaponWeightIndex = data.get('weaponWeight', None)
            weaponWeight = WeaponWeight(weaponWeightIndex) if weaponWeightIndex else None

            handlingIndex = data.get('handling', None)
            handling = Handling(handlingIndex) if handlingIndex else None

            return MeleeWeapon(item_id, lang, tr_data.get('name', ''),
                               tr_data.get('description', ''), data.get('parent_id', 0),
                               data.get('weight', 0), data.get('price', 0), data.get('strength', 0),
                               data.get('rampancy', 0), data.get('defence', 0),
                               data.get('length', 0), weaponWeight, handling)

        if data['type'] == Items.THROWABLE_WEAPON.value:
            weaponWeightIndex = data.get('weaponWeight', None)
            weaponWeight = WeaponWeight(weaponWeightIndex) if weaponWeightIndex else None

            return ThrowableWeapon(item_id, lang, tr_data.get('name', ''),
                                   tr_data.get('description', ''),
                                   data.get('parent_id', 0), data.get('weight', 0),
                                   data.get('price', 0), data.get('initiative', 0),
                                   data.get('strength', 0), data.get('rampancy', 0),
                                   data.get('rangeLow', 0), data.get('rangeMedium', 0),
                                   data.get('rangeHigh', 0), data.get('defence', 0),
                                   weaponWeight)

        if data['type'] == Items.RANGED_WEAPON.value:
            return RangeWeapon(item_id, lang, tr_data.get('name', ''),
                               tr_data.get('description', ''),
                               data.get('parent_id', 0), data.get('weight', 0),
                               data.get('price', 0), data.get('initiative', 0),
                               data.get('strength', 0), data.get('rampancy', 0),
                               data.get('rangeLow', 0), data.get('rangeMedium', 0),
                               data.get('rangeHigh', 0))

        if data['type'] == Items.ARMOR.value:
            return Armor(item_id, lang, tr_data.get('name', ''), tr_data.get('description', ''),
                         data.get('parent_id', 0), data.get('price', 0), data.get('quality', 0),
                         data.get('weightA', 0), data.get('weightB', 0), data.get('weightC', 0),
                         data.get('size', 0))

        if data['type'] == Items.MONEY.value:
            return Money(item_id, lang, tr_data.get('name', ''), tr_data.get('description', ''),
                         data.get('parent_id', 0), data.get('copper'), data.get('silver'),
                         data.get('gold'))


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
