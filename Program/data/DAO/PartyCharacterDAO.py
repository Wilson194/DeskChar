from data.DAO.CharacterDAO import CharacterDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.interface.ISpellDAO import ISpellDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.character.Character import Character
from structure.character.PartyCharacter import PartyCharacter
from structure.enums.Alignment import Alignment
from structure.enums.Classes import Classes
from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType
from structure.enums.Races import Races
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.Item import Item
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon
from structure.spells.Spell import Spell
from data.DAO.DAO import DAO


class PartyCharacterDAO(DAO):
    DATABASE_TABLE = 'PartyCharacter'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.CHARACTER


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, character: Character) -> int:
        """
        Create new spell in database
        :param character: Character object
        :return: id of autoincrement
        """
        return ObjectDatabase(self.DATABASE_DRIVER).insert_object(character)


    def update(self, character: Character):
        """
        Update spell in database
        :param character: Character object with new data
        """
        ObjectDatabase(self.DATABASE_DRIVER).update_object(character)


    def delete(self, character_id: int):
        """
        Delete spell from database and all his translates
        :param character_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, character_id)


    def get(self, character_id: int, lang: str = None) -> PartyCharacter:
        """
        Get spell from database
        :param character_id: id of spell
        :param lang: lang of spell
        :return: Spell object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'

        select = self.database.select(self.DATABASE_TABLE, {'ID': character_id})

        if not select:
            return None

        data = dict(select[0])
        tr_data = self.database.select_translate(character_id, ObjectType.PARTY_CHARACTER.value,
                                                 lang)

        character = PartyCharacter(data.get('ID'), lang, None, None, tr_data.get('deviceName', ''),
                                   tr_data.get('MACAddress'))

        character.character = CharacterDAO().get(data.get('character_id'))

        return character


    def get_all(self, lang=None) -> list:
        """
        Get list of all spells from database, only one lang
        :param lang: lang code
        :return: list of Spells
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)
        characters = []
        for line in lines:
            character = self.get(line['ID'], lang)
            characters.append(character)
        return characters
