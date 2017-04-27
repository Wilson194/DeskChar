from PyQt5.QtCore import QPointF

from structure.enums.MapItem import MapItemType
from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object


class MapItem(Object):
    def __init__(self, id: int = None, name: str = None, description: str = None,
                 coord: QPointF = None, scale: int = None, number: int = None,
                 object: object = None, mapId: int = None, itemType: MapItemType = None):
        super().__init__(id, None, name, description)

        self.__itemType = itemType
        self.__coord = coord
        self.__scale = scale
        self.__object = object
        self.__name = name
        self.__description = description
        self.__number = number
        self.__mapId = mapId


    @staticmethod
    def DAO():
        from data.DAO.MapItemDAO import MapItemDAO
        return MapItemDAO


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLMapItem import XMLMapItem
        return XMLMapItem


    @property
    def object_type(self):
        return ObjectType.MAP_ITEM

    def __name__(self):
        names = super().__name__()
        names.append('MapItem')
        return names

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


    @property
    def icon(self):
        return self.__icon


    @icon.setter
    def icon(self, value):
        self.__icon = value


    @property
    def mapId(self):
        return self.__mapId


    @mapId.setter
    def mapId(self, value):
        self.__mapId = value


    @property
    def itemType(self):
        return self.__itemType


    @itemType.setter
    def itemType(self, value):
        self.__itemType = value
