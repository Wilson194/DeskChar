from data.DAO.CharacterDAO import CharacterDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.database.Database import Database
from structure.character.PartyCharacter import PartyCharacter
from structure.enums.ObjectType import ObjectType
from data.DAO.DAO import DAO


class PartyCharacterDAO(DAO):
    DATABASE_TABLE = 'PartyCharacter'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.CHARACTER


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, character: PartyCharacter, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new spell in database
        :param character: Character object
        :return: id of autoincrement
        """
        if character.character:
            character_id = CharacterDAO().create(character.character.popitem()[1], nodeParentId,
                                                 contextType)  # TODO: default lang
        else:
            character_id = None

        if nodeParentId:
            scenario = PlayerTreeDAO().get_node(nodeParentId).object

        intValues = {
            'deviceName'  : character.deviceName,
            'MACAddress'  : character.MACAddress,
            'character_id': character_id,
            'scenario_id' : scenario.id,
            'name'        : character.name
        }

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        character.id = id

        return id


    def update(self, character: PartyCharacter):
        """
        Update spell in database
        :param character: Character object with new data
        """
        intValues = {
            'deviceName': character.deviceName,
            'MACAddress': character.MACAddress,
            'name'      : character.name
        }

        self.database.update(self.DATABASE_TABLE, character.id, intValues)


    def delete(self, character_id: int):
        """
        Delete spell from database and all his translates
        :param character_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, character_id)


    def get(self, character_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> PartyCharacter:
        """
        Get spell from database
        :param character_id: id of spell
        :param lang: lang of spell
        :return: Spell object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'

        select = self.database.select(self.DATABASE_TABLE, {'character_id': character_id})

        if not select:
            return None

        data = dict(select[0])

        character = PartyCharacter(data.get('ID'), lang, data['name'], None, data.get('deviceName', ''),
                                   data.get('MACAddress'))

        # character.character = CharacterDAO().get(data.get('character_id'))

        return character


    def get_by_id(self, partyCharacterId: int, lang: str = None):

        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': partyCharacterId})[0])

        character = PartyCharacter(data.get('ID'), lang, data['name'], None, data.get('deviceName', ''),
                                   data.get('MACAddress'))

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
