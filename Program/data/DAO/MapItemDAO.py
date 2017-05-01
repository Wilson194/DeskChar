from PyQt5.QtCore import QPointF

from data.DAO.SettingsDAO import SettingsDAO
from data.DAO.interface.IMapItemDAO import IMapItemDAO
from data.database.Database import Database
from structure.enums.MapItem import MapItemType
from structure.enums.ObjectType import ObjectType
from structure.map.MapItem import MapItem


class MapItemDAO(IMapItemDAO):
    DATABASE_TABLE = 'Map_item'
    DATABASE_DRIVER = "file::memory:?cache=shared"
    TYPE = ObjectType.MAP_ITEM


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, mapItem: MapItem) -> int:
        """
        Create new map item        
        :param mapItem: Map object        
        :return: id of created mapItem
        """
        X = mapItem.coord.x()
        Y = mapItem.coord.y()

        values = {
            'name'       : mapItem.name,
            'description': mapItem.description,
            'number'     : mapItem.number,
            'scale'      : mapItem.scale,
            'positionX'  : X,
            'positionY'  : Y,
            'map_id'     : mapItem.mapId,
            'itemType'   : mapItem.itemType.value
        }
        id = self.database.insert(self.DATABASE_TABLE, values)

        return id


    def update(self, mapItem: MapItem):
        """
        Update map item in database
        :param mapItem: mapItem object with new data
        """
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
        Delete Map item from database and all his translates
        :param mapitem_id: id of Map item
        """
        self.database.delete(self.DATABASE_TABLE, mapitem_id)


    def get(self, mapitem_id: int) -> MapItem:
        """
        Get map item from database
        :param mapitem_id: id of map item        
        :return: Map item object
        """

        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': mapitem_id})[0])

        coord = QPointF(data.get('positionX', 0), data.get('positionY', 0))

        itemType = MapItemType(data.get('itemType'))

        mapitem = MapItem(mapitem_id, data.get('name', ''), data.get('description', ''), coord,
                          data.get('scale', 0), data.get('number', 0), None, data.get('map_id'), itemType)

        return mapitem


    def get_all(self, lang=None) -> list:
        """
        Get list of map items for selected lang
        :param lang: lang of map items
        :return: list of map items
        """
        if lang is None:
            lang = SettingsDAO().get_value('language', str)
        lines = self.database.select_all(self.DATABASE_TABLE)
        mapItems = []
        for line in lines:
            item = self.get(line['ID'], lang)
            mapItems.append(item)
        return mapItems
