from data.database.Database import Database
from structure.character.Message import Message
from structure.character.PartyCharacter import PartyCharacter
from structure.enums.ObjectType import ObjectType
from data.DAO.DAO import DAO
from datetime import datetime, date


class MessageDAO(DAO):
    DATABASE_TABLE = 'Message'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.MESSAGE


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, message: Message) -> int:
        """
        Create new spell in database
        :param character: Character object
        :return: id of autoincrement
        """
        curDate = datetime.strptime(message.date, '%d/%m/%Y') if message.date else None

        if type(message.isMine) is str:
            isMine = True if message.isMine == 'true' else False
        else:
            isMine = message.isMine

        intValues = {
            'text'  : message.text,
            'date'  : curDate.toordinal() if curDate else None,
            'isMine': int(isMine)
        }

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        message.id = id

        return id


    def update(self, message: Message):
        """
        Update spell in database
        :param character: Character object with new data
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


    def delete(self, character_id: int):
        """
        Delete spell from database and all his translates
        :param character_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, character_id)


    def get(self, message_id: int, lang: str = None) -> Message:
        """
        Get spell from database
        :param character_id: id of spell
        :param lang: lang of spell
        :return: Spell object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'

        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': message_id})[0])

        curDate = date.fromordinal(data.get('date')) if data.get('date') else None

        message = Message(message_id, data['text'], curDate, bool(data['isMine']))

        return message


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
