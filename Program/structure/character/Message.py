from datetime import datetime


class Message:
    def __init__(self, id: int = None, text: str = None, date: datetime = None, isMine: bool = None, partyCharacterId: int = None,
                 characterId: int = None):
        self.__id = id
        self.__text = text
        self.__date = date
        self.__isMine = isMine
        self.__partyCharacterId = partyCharacterId
        self.__characterId = characterId

    def __name__(self):
        names = ['Message']
        return names


    @staticmethod
    def DAO():
        from data.DAO.MessageDAO import MessageDAO
        return MessageDAO


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLMessage import XMLMessage
        return XMLMessage


    @property
    def id(self):
        return self.__id


    @id.setter
    def id(self, value):
        self.__id = value


    @property
    def text(self):
        return self.__text


    @text.setter
    def text(self, value):
        self.__text = value


    @property
    def date(self):
        return self.__date


    @date.setter
    def date(self, value):
        self.__date = value


    @property
    def isMine(self):
        return self.__isMine


    @isMine.setter
    def isMine(self, value):
        self.__isMine = value


    @property
    def partyCharacterId(self):
        return self.__partyCharacterId


    @partyCharacterId.setter
    def partyCharacterId(self, value):
        self.__partyCharacterId = value


    @property
    def characterId(self):
        return self.__characterId


    @characterId.setter
    def characterId(self, value):
        self.__characterId = value
