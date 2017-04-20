from PyQt5.QtCore import QPointF

from structure.general.Object import Object


class MapItem(Object):
    def __init__(self, id: int = None, name: str = None, description: str = None,
                 coord: QPointF = None, scale: int = None, number: int = None,
                 object: object = None):
        super().__init__(id, None, name, description)

        self.__coord = None
        self.__scale = None
        self.__object = None
        self.__name = None
        self.__description = None
        self.__number = None


    @property
    def coord(self):
        return self.__coord


    @coord.setter
    def coord(self, value):
        self.__coord = value


    @property
    def scale(self):
        return self.__scale


    @scale.setter
    def scale(self, value):
        self.__scale = value


    @property
    def object(self):
        return self.__object


    @object.setter
    def object(self, value):
        self.__object = value


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


    @property
    def number(self):
        return self.__number


    @number.setter
    def number(self, value):
        self.__number = value
