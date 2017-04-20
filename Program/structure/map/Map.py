from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object
from structure.map.MapItem import MapItem


class Map(Object):
    TABLE_SCHEMA = [
        'id', 'name', 'description'
    ]


    def __init__(self, id: int = None, lang: str = None, name: str = None, description: str = None,
                 map: str = None):
        super().__init__(id, lang, name, description)

        self.__map = map

        self.__mapItems = []


    def __name__(self):
        names = super().__name__()
        names.append('Map')
        return names


    @staticmethod
    def DAO():
        from data.DAO.MapDAO import MapDAO
        return MapDAO


    @staticmethod
    def XmlClass():
        return None


    @staticmethod
    def layout():
        return None


    @property
    def children(self):
        return []


    @property
    def treeChildren(self):
        return None


    @property
    def icon(self):
        return 'resources/icons/map.png'


    @property
    def object_type(self):
        return ObjectType.MAP


    @property
    def mapItems(self):
        return self.__mapItems


    @mapItems.setter
    def mapItems(self, value):
        self.__mapItems = value


    def addMapItem(self, mapItem: MapItem):
        self.__mapItems.append(mapItem)


    @property
    def map(self):
        return self.__map


    @map.setter
    def map(self, value):
        self.__map = value
