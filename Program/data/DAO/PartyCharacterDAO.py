from data.DAO.CharacterDAO import CharacterDAO
from data.DAO.MessageDAO import MessageDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.interface.IPartyCharacterDAO import IPartyCharacterDAO
from data.database.Database import Database
from structure.character.PartyCharacter import PartyCharacter
from structure.enums.ObjectType import ObjectType
from data.DAO.DAO import DAO


class PartyCharacterDAO(DAO, IPartyCharacterDAO):
    DATABASE_TABLE = 'PartyCharacter'
    TYPE = ObjectType.CHARACTER


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, character: PartyCharacter, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new PartyCharacter, if character given, linked with character and create character
                                   if character is not given, only party character created and liked with scenario
        :param character: PartyCharacter object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created character
        """
        if not contextType:
            contextType = self.TYPE

        if character.character:
            if type(character.character) is dict:
                character_id = CharacterDAO().create(character.character.popitem()[1], nodeParentId,
                                                     contextType)  # TODO: default lang
            else:
                character_id = CharacterDAO().create(character.character, nodeParentId,
                                                     contextType)  # TODO: default lang
        else:
            character_id = None

        if nodeParentId:
            scenario = PlayerTreeDAO().get_node(nodeParentId).object
        else:
            scenario = None

        intValues = {
            'deviceName'  : character.deviceName,
            'MACAddress'  : character.MACAddress,
            'character_id': character_id,
            'scenario_id' : scenario.id if scenario else None,
            'name'        : character.name,
        }

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        character.id = id

        for message in character.messages:
            message.partyCharacterId = id
            MessageDAO().create(message)

        return id


    def update(self, character: PartyCharacter):
        """
        Update party PartyCharacter in database, update only party character, not Character
        :param character: PartyCharacter object with new data
        """
        intValues = {
            'deviceName': character.deviceName,
            'MACAddress': character.MACAddress,
            'name'      : character.name
        }

        self.database.update(self.DATABASE_TABLE, character.id, intValues)


    def delete(self, character_id: int):
        """
        Delete party character from database and all his translates
        :param character_id: id of party character
        """
        self.database.delete(self.DATABASE_TABLE, character_id)


    def get(self, character_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> PartyCharacter:
        """
        Get Party Character by character id, object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param character_id: id of Party Character
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Party Character object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'

        select = self.database.select(self.DATABASE_TABLE, {'character_id': character_id})

        if not select:
            return None

        data = dict(select[0])

        character = PartyCharacter(data.get('ID'), lang, data['name'], None, data.get('deviceName', ''),
                                   data.get('MACAddress'))

        messages = MessageDAO().get_by_party_character(character.id)

        character.messages = messages

        # character.character = CharacterDAO().get(data.get('character_id'))

        return character


    def get_by_id(self, partyCharacterId: int, lang: str = None) -> PartyCharacter:
        """
        Get party character by id, without character
        :param partyCharacterId: party character ID
        :param lang: lang of object
        :return: Party character object
        """
        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': partyCharacterId})[0])

        character = PartyCharacter(data.get('ID'), lang, data['name'], None, data.get('deviceName', ''),
                                   data.get('MACAddress'))

        return character


    def get_all(self, lang=None) -> list:
        """
        Get list of all Party Characters from database, only one lang
        :param lang: lang code
        :return: list of Party Characters
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)
        characters = []
        for line in lines:
            character = self.get(line['ID'], lang)
            characters.append(character)
        return characters
