from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType
from structure.items.Item import Item


class Armor(Item):
    TABLE_SCHEMA = ['id', 'name', 'description', 'price', 'quality', 'weightA', 'weightB',
                    'weightC', 'size', 'type']


    def __init__(self, id: int = None, lang=None, name: str = None,
                 description: str = None, parent_id: int = None,
                 price: int = None, quality: int = None,
                 weightA: int = None, weightB: int = None, weightC: int = None, size: int = None):
        super().__init__(id, lang, name, description, parent_id, None, price)

        self.__quality = quality
        self.__weightA = weightA
        self.__weightB = weightB
        self.__weightC = weightC
        self.__size = size
        self.__type = Items.ARMOR


    def __name__(self):
        names = super().__name__()
        names.append('Armor')
        return names


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLArmor import XMLArmor
        return XMLArmor


    @staticmethod
    def layout():
        from presentation.layouts.ArmorLayout import ArmorLayout
        return ArmorLayout


    @property
    def icon(self):
        return 'resources/icons/armor.png'


    @property
    def type(self):
        return self.__type


    @property
    def quality(self):
        return self.__quality


    @quality.setter
    def quality(self, value):
        self.__quality = value


    @property
    def weightA(self):
        return self.__weightA


    @weightA.setter
    def weightA(self, value):
        self.__weightA = value


    @property
    def weightB(self):
        return self.__weightB


    @weightB.setter
    def weightB(self, value):
        self.__weightB = value


    @property
    def weightC(self):
        return self.__weightC


    @weightC.setter
    def weightC(self, value):
        self.__weightC = value


    @property
    def size(self):
        return self.__size


    @size.setter
    def size(self, value):
        self.__size = value
