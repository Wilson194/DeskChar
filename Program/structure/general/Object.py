from abc import ABC, abstractmethod


class Object(ABC):
    @abstractmethod
    def __init__(self, id: int, lang: str, name: str, description: str):
        self.__id = id
        self.__lang = lang
        self.__name = name
        self.__description = description


    @property
    def id(self):
        return self.__id


    @id.setter
    def id(self, value):
        self.__id = value


    @property
    def lang(self):
        return self.__lang


    @lang.setter
    def lang(self, value):
        self.__lang = value


    @property
    def name(self):
        return self.__name


    @name.setter
    def name(self, value):
        self.__name = value


    @property
    def description(self):
        return self.__description


    @description.setter
    def description(self, value):
        self.__description = value


    def __eq__(self, other):
        return self.__name == other.name and self.__description == other.description

    @abstractmethod
    def __name__(self):
        return ['Object']
