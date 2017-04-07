from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.interface.ISpellDAO import ISpellDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.character.Character import Character
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


class CharacterDAO(DAO, ISpellDAO):
    DATABASE_TABLE = 'Character'
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
        self.database.delete_where('translates',
                                   {'target_id': character_id, 'type': ObjectType.CHARACTER})


    def get(self, character_id: int, lang: str = None) -> Character:
        """
        Get spell from database
        :param character_id: id of spell
        :param lang: lang of spell
        :return: Spell object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'

        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': character_id})[0])
        tr_data = self.database.select_translate(character_id, ObjectType.CHARACTER.value,
                                                 lang)

        drdClass = Classes(data.get('drdClass')) if data.get('drdClass') is not None else None
        drdRace = Races(data.get('drdRace')) if data.get('drdRace') is not None else None
        character = Character(data.get('ID'), lang, tr_data.get('name', ''),
                              tr_data.get('description', ''), data.get('agility', 0),
                              data.get('charisma', 0), data.get('intelligence', 0),
                              data.get('mobility', 0), data.get('strength', 0),
                              data.get('toughness', 0), data.get('age', 0), data.get('height', 0),
                              data.get('weight', 0), data.get('level', 0), data.get('xp', 0),
                              data.get('maxHealth', 0), data.get('maxMana', 0), drdClass, drdRace)

        spells = PlayerTreeDAO().get_children_objects(ObjectType.SPELL, character)
        character.spells = spells

        abilities = PlayerTreeDAO().get_children_objects(ObjectType.ABILITY, character)
        character.abilities = abilities

        effects = PlayerTreeDAO().get_children_objects(ObjectType.EFFECT, character)
        character.effects = effects

        items = PlayerTreeDAO().get_children_objects(ObjectType.ITEM, character)

        for item in items:
            if isinstance(item, Armor):
                character.addArmor(item)
            elif isinstance(item, Money):
                character.addMoney(item)
            elif isinstance(item, Container):
                character.addContainer(item)
            elif isinstance(item, MeleeWeapon):
                character.addMeleeWeapon(item)
            elif isinstance(item, RangeWeapon):
                character.addRangedWeapon(item)
            elif isinstance(item, ThrowableWeapon):
                character.addThrowableWeapon(item)
            else:
                character.addItem(item)

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
