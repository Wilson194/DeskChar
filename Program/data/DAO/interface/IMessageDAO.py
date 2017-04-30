from abc import ABC, abstractmethod

from structure.character.Message import Message
from structure.items.Item import *
from structure.map.Map import Map
from structure.map.MapItem import MapItem


class IMessageDAO(ABC):
    @abstractmethod
    def create(self, message: Message) -> int:
        """
        Create new message in database
        :param message: Message object
        :return: id of autoincrement
        """
        pass


    @abstractmethod
    def update(self, message: Message):
        """
        Update message in database
        :param message: Message object with new data
        """
        pass


    @abstractmethod
    def delete(self, message_id: int):
        """
        Delete Message from database and all his translates
        :param message_id: id of Message
        """
        pass


    @abstractmethod
    def get(self, message_id: int, lang: str = None) -> Message:
        """
        Get Message from database
        :param message_id: id of Message
        :param lang: lang of spell
        :return: Message object
        """
        pass


    @abstractmethod
    def get_by_party_character(self, partyCharacterId: int) -> list:
        """
        Get all messages for one party character
        :param partyCharacterId: id of party character
        :return: list of Messages
        """
        pass


    @abstractmethod
    def get_all(self, lang: str = None):
        """
        Get list of all messages from database, only one lang
        :param lang: lang code
        :return: list of messages
        """
        pass
