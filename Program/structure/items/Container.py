from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType
from structure.items.Item import Item


class Container(Item):
    TABLE_SCHEMA = ['id', 'name', 'description', 'weight', 'price', 'capacity', 'type', 'amount']


    def __init__(self, id: int = None, lang=None, name: str = None,
                 description: str = None, parent_id: int = None, weight: int = None,
                 price: int = None, capacity: int = None, amount: int = 1):
        super().__init__(id, lang, name, description, parent_id, weight, price, amount)

        self.__capacity = capacity
        self.__type = Items.CONTAINER

        self.__items = []


    def __name__(self):
        names = super().__name__()
        names.append('Container')
        return names


    @property
    def treeChildren(self):
        return [ObjectType.ITEM] + super().treeChildren


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLContainer import XMLContainer
        return XMLContainer


    @staticmethod
    def layout():
        from presentation.layouts.ContainerLayout import ContainerLayout
        return ContainerLayout


    @property
    def icon(self):
        return 'resources/icons/bag.png'


    @property
    def capacity(self):
        return self.__capacity


    @capacity.setter
    def capacity(self, value):
        self.__capacity = value


    @property
    def type(self):
        return self.__type
