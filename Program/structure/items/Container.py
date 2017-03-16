from structure.enums.Items import Items
from structure.items.Item import Item


class Container(Item):
    def __init__(self, id: int = None, lang=None, name: str = None,
                 description: str = None, parent_id: int = None, weight: int = None,
                 price: int = None, capacity: int = None):
        super().__init__(id, lang, name, description, parent_id, weight, price)

        self.__capacity = capacity
        self.__type = Items.CONTAINER


    def __name__(self):
        names = super().__name__()
        names.append('Container')
        return names


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
    def object_type(self):
        return Items.CONTAINER


    @property
    def capacity(self):
        return self.__capacity


    @capacity.setter
    def capacity(self, value):
        self.__capacity = value
