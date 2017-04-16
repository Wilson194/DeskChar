from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.enums.Alignment import Alignment
from structure.enums.MonsterRace import MonsterRace
from structure.enums.ObjectType import ObjectType
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon
from structure.monster.Monster import Monster

from data.DAO.DAO import DAO
from structure.scenario.Location import Location
from structure.scenario.Scenario import Scenario


class LocationDAO(DAO):
    DATABASE_TABLE = 'Location'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.LOCATION


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, location: Location) -> int:
        """
        Create new spell in database
        :param location: Spell object
        :return: id of autoincrement
        """
        return ObjectDatabase(self.DATABASE_DRIVER).insert_object(location)


    def update(self, location: Location):
        """
        Update spell in database
        :param location: Spell object with new data
        """
        ObjectDatabase(self.DATABASE_DRIVER).update_object(location)


    def delete(self, location_id: int):
        """
        Delete spell from database and all his translates
        :param location_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, location_id)
        self.database.delete_where('translates',
                                   {'target_id': location_id, 'type': self.TYPE})


    def get(self, location_id: int, lang: str = None) -> Location:
        """
        Get spell from database
        :param location_id: id of spell
        :param lang: lang of spell
        :return: Monster object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': location_id})[0])
        tr_data = dict(self.database.select_translate(location_id, self.TYPE.value,
                                                      lang))

        location = Location(data.get('ID'), lang, tr_data.get('name', ''),
                            tr_data.get('description', ''))

        locations = PlayerTreeDAO().get_children_objects(ObjectType.LOCATION, location)
        location.locations = locations

        monsters = PlayerTreeDAO().get_children_objects(ObjectType.MONSTER, location)
        location.monsters = monsters

        items = PlayerTreeDAO().get_children_objects(ObjectType.ITEM, location)

        for item in items:
            if isinstance(item, Armor):
                location.addArmor(item)
            elif isinstance(item, Money):
                location.addMoney(item)
            elif isinstance(item, Container):
                location.addContainer(item)
            elif isinstance(item, MeleeWeapon):
                location.addMeleeWeapon(item)
            elif isinstance(item, RangeWeapon):
                location.addRangedWeapon(item)
            elif isinstance(item, ThrowableWeapon):
                location.addThrowableWeapon(item)
            else:
                location.addItem(item)

        return location


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
