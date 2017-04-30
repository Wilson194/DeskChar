from data.DAO.interface.IMessageDAO import IMessageDAO
from data.database.Database import Database
from structure.character.Message import Message
from structure.enums.ObjectType import ObjectType
from data.DAO.DAO import DAO
from datetime import datetime, date


class MessageDAO(DAO, IMessageDAO):
    DATABASE_TABLE = 'Message'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.MESSAGE


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, message: Message) -> int:
        """
        Create new message in database
        :param message: Message object
        :return: id of autoincrement
        """
        curDate = datetime.strptime(message.date, '%d/%m/%Y %H:%M:%S') if message.date else None

        if type(message.isMine) is str:
            isMine = True if message.isMine == 'true' else False
        else:
            isMine = message.isMine

        intValues = {
            'text'            : message.text,
            'date'            : curDate.toordinal() if curDate else None,
            'isMine'          : int(isMine),
            'characterId'     : message.characterId,
            'partyCharacterId': message.partyCharacterId
        }

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        message.id = id

        return id


    def update(self, message: Message):
        """
        Update message in database
        :param message: Message object with new data
        """
        if type(message.isMine) is str:
            isMine = True if message.isMine == 'true' else False
        else:
            isMine = message.isMine

        intValues = {
            'text'  : message.text,
            'date'  : message.date.toordinal(),
            'isMine': int(isMine)
        }

        self.database.update(self.DATABASE_TABLE, message.id, intValues)


    def delete(self, message_id: int):
        """
        Delete Message from database and all his translates
        :param message_id: id of Message
        """
        self.database.delete(self.DATABASE_TABLE, message_id)


    def get(self, message_id: int, lang: str = None) -> Message:
        """
        Get Message from database
        :param message_id: id of Message
        :param lang: lang of spell
        :return: Message object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'

        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': message_id})[0])

        curDate = datetime.fromordinal(data.get('date')) if data.get('date') else None

        message = Message(message_id, data['text'], curDate, bool(data['isMine']), data.get('partyCharacterId'),
                          data.get('characterId'))

        return message


    def get_by_party_character(self, partyCharacterId: int) -> list:
        """
        Get all messages for one party character
        :param partyCharacterId: id of party character
        :return: list of Messages
        """
        select = self.database.select(self.DATABASE_TABLE, {'partyCharacterId': partyCharacterId})

        messages = []
        for one in select:
            data = dict(one)
            curDate = date.fromordinal(data.get('date')) if data.get('date') else None
            message = Message(data.get('id'), data.get('text', ''), curDate, bool(data['isMine']), data.get('partyCharacterId'),
                              None)

            messages.append(message)

        return messages


    def get_all(self, lang=None) -> list:
        """
        Get list of all messages from database, only one lang
        :param lang: lang code
        :return: list of messages
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)
        characters = []
        for line in lines:
            character = self.get(line['ID'], lang)
            characters.append(character)
        return characters
