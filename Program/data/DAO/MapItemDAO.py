from PyQt5.QtCore import QPointF
from data.database.Database import Database
from structure.enums.ObjectType import ObjectType
from structure.map.MapItem import MapItem


class MapItemDAO():
    DATABASE_TABLE = 'Map_item'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.MAP_ITEM


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, mapItem: MapItem) -> int:
        X = mapItem.coord.x()
        Y = mapItem.coord.y()

        values = {
            'name'       : mapItem.name,
            'description': mapItem.description,
            'number'     : mapItem.number,
            'scale'      : mapItem.scale,
            'positionX'  : X,
            'positionY'  : Y,
        }
        id = self.database.insert(self.DATABASE_TABLE, values)

        return id


    def update(self, mapItem: MapItem):
        X = mapItem.coord.x()
        Y = mapItem.coord.y()

        values = {
            'name'       : mapItem.name,
            'description': mapItem.description,
            'number'     : mapItem.number,
            'scale'      : mapItem.scale,
            'positionX'  : X,
            'positionY'  : Y,
        }

        self.database.update(self.DATABASE_TABLE, mapItem.id, values)


    def delete(self, mapitem_id: int):
        """
        Delete spell from database and all his translates
        :param spell_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, mapitem_id)


    def get(self, mapitem_id: int) -> MapItem:
        """
        Get spell from database
        :param monster_id: id of spell
        :param lang: lang of spell
        :return: Monster object
        """

        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': mapitem_id})[0])

        coord = QPointF(data.get('positionX', 0), data.get('positionY', 0))

        mapitem = MapItem(mapitem_id, data.get('name', ''), data.get('description', ''), coord,
                          data.get('scale', 0), data.get('number', 0))

        return mapitem


    def get_all(self, lang=None) -> list:
        pass
