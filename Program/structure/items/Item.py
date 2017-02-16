from general.Object import *


class Item(Object):
    def __init__(self, id=None, lang=None, name=None, description=None,
                 type=None, parent_id=None, weight=None, price=None):
        super().__init__(id, lang, name, description)
        self.__parent_id = parent_id
        self.__weight = weight
        self.__price = price
        self.__amount = 1
        self.__type = type


    def __name__(self):
        names = super().__name__()
        names.append('Item')
        return names


    @property
    def parent_id(self):
        return self.__parent_id


    @parent_id.setter
    def parent_id(self, value):
        self.__parent_id = value


    @property
    def weight(self):
        return self.__weight


    @weight.setter
    def weight(self, value):
        self.__weight = value


    @property
    def price(self):
        return self.__price


    @price.setter
    def price(self, value):
        self.__price = value


    @property
    def amount(self):
        return self.__amount


    @amount.setter
    def amount(self, value):
        self.__amount = value


    @property
    def type(self):
        return self.__type


    @type.setter
    def type(self, value):
        self.__type = value


    def __eq__(self, other):
        if super().__eq__(
                other) and self.weight == other.weight and self.price == other.price:
            return True

        return False
