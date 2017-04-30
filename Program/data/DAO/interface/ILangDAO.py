from abc import ABC, abstractmethod

from structure.general.Lang import Lang
from structure.items.Item import *


class ILangDAO(ABC):
    @abstractmethod
    def get_all_langs(self) -> list:
        """
        Return list of all langs
        :return: List of lang objects
        """
        pass


    def get_lang_by_code(self, code: str) -> Lang:
        """
        Get lang from database by code
        :param code: Code of lang (2 char)
        :return: Lang object if exist, None otherwise
        """
        pass


    def get_lang(self, id: int) -> Lang:
        """
        Get lang by id
        :param id: id of lang
        :return: Lang object if exist, None otherwise
        """
        pass


    def create_lang(self, lang: Lang) -> int:
        """
        Create new lang, must be unique
        :param lang: lang object
        :return: id of created lang
        """
        pass
