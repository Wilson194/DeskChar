from structure.items.Item import *


class Money(Item):
    TABLE_SCHEMA = ['id', 'name', 'description', 'copper', 'silver', 'gold', 'type', 'amount']


    def __init__(self, id: int = None, lang=None, name: str = None,
                 description: str = None, parent_id: int = None, copper: int = None,
                 silver: int = None, gold: int = None, amount: int = 1):
        super().__init__(id, lang, name, description, parent_id, None, None, amount)

        self.__copper = copper
        self.__silver = silver
        self.__gold = gold
        self.__type = Items.MONEY


    def __name__(self):
        names = super().__name__()
        names.append('Money')
        return names


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLMoney import XMLMoney
        return XMLMoney


    @staticmethod
    def layout():
        from presentation.layouts.MoneyLayout import MoneyLayout
        return MoneyLayout


    @property
    def icon(self):
        return 'resources/icons/coin.png'


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


    @property
    def type(self):
        return self.__type

    def __hash__(self):
        return hash((self.object_type, self.id))