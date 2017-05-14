from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object
from structure.map.MapItem import MapItem


class Map(Object):
    TABLE_SCHEMA = [
        'id', 'name', 'description'
    ]


    def __init__(self, id: int = None, lang: str = None, name: str = None, description: str = None,
                 mapFile: str = None):
        super().__init__(id, lang, name, description)

        self.__mapFile = mapFile
        self.__mapPixMap = None
        self.__XMLMap = None
        self.__finalMapPath = None

        self.__mapItems = []
        self.__mapItemDraws = []


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
        from data.xml.templates.XMLMap import XMLMap
        return XMLMap


    @staticmethod
    def layout():
        return None


    @property
    def children(self):
        return []


    @property
    def treeChildren(self):
        return []


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
    def mapFile(self):
        return self.__mapFile


    @mapFile.setter
    def mapFile(self, value):
        self.__mapFile = value


    @property
    def mapPixMap(self):
        return self.__mapPixMap


    @mapPixMap.setter
    def mapPixMap(self, value):
        self.__mapPixMap = value


    @property
    def mapItemDraws(self):
        return self.__mapItemDraws


    @mapItemDraws.setter
    def mapItemDraws(self, value):
        self.__mapItemDraws = value


    def addMapItemDraws(self, value):
        self.__mapItemDraws.append(value)


    @property
    def XMLMap(self):
        return self.__XMLMap


    @XMLMap.setter
    def XMLMap(self, value):
        self.__XMLMap = value


    @property
    def finalMapPath(self):
        return self.__finalMapPath


    @finalMapPath.setter
    def finalMapPath(self, value):
        self.__finalMapPath = value

    def __hash__(self):
        return hash((self.object_type, self.id))