from abc import ABC, abstractmethod

from structure.abilities.Ability import Ability
from structure.effects.AbilityContext import AbilityContext
from structure.effects.Effect import Effect
from structure.enums.ObjectType import ObjectType
from structure.general.Lang import Lang


class ILangManager(ABC):
    @abstractmethod
    def get_all_langs(self) -> list:
        """
        Return all langs in database
        :return: list of object Langs
        """
        pass


    @abstractmethod
    def lang_exists(self, code: str) -> bool:
        """
        Check if lang code exist in database
        :param code: lang code ( 2 char)
        :return: True if exist, False otherwise
        """
        pass


    @abstractmethod
    def get_lang(self, id: int) -> Lang:
        """
        Get lang by id
        :param id: id of lang
        :return: object Lang if exist, None otherwise
        """
        pass


    @abstractmethod
    def get_lang_by_code(self, code):
        """
        Get lang by code
        :param code: lang code (2 char)
        :return: object Lang if exist, None otherwise
        """
        pass


    @abstractmethod
    def create_lang(self, name, code):
        """
        Create new lang
        :param name: Name of lang
        :param code: Code of lang
        :return: object Lang if created, None otherwise
        """
        pass
