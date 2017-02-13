from Item import *


class Money(Item):
    def __init__(self, id: int = None, lang=None, name: str = None,
                 description: str = None, parent_id: int = None):
        super().__init__(id, lang, name, description, parent_id)

        self.__copper = 0
        self.__silver = 0
        self.__gold = 0


    @property
    def copper(self):
        return self.__copper


    @copper.setter
    def copper(self, value):
        self.__copper = value


    @property
    def silver(self):
        return self.__silver


    @silver.setter
    def silver(self, value):
        self.__silver = value


    @property
    def gold(self):
        return self.__gold


    @gold.setter
    def gold(self, value):
        self.__gold = value
