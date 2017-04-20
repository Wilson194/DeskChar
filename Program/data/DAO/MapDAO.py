from PyQt5.QtCore import QPointF

from data.DAO.MapItemDAO import MapItemDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.database.Database import Database
from structure.enums.ObjectType import ObjectType
from structure.map.Map import Map
from structure.map.MapItem import MapItem
from structure.tree.NodeObject import NodeObject


class MapDAO:
    DATABASE_TABLE = 'Map'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.MAP


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, map: Map) -> int:
        values = {
            'name'       : map.id,
            'description': map.description,
            'map_file'   : map.map,
        }

        id = self.database.insert(self.DATABASE_TABLE, values)

        map.id = id
        node = NodeObject(None, map.name, None, map)
        PlayerTreeDAO().insert_node(node, self.TYPE)

        return id


    def update(self, map: Map):
        values = {
            'name'       : map.id,
            'description': map.description,
            'map_file'   : map.map,
        }

        self.database.update(self.DATABASE_TABLE, map.id, values)


    def delete(self, map_id: int):
        """
        Delete spell from database and all his translates
        :param spell_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, map_id)


    def get(self, map_id: int) -> Map:
        """
        Get spell from database
        :param monster_id: id of spell
        :param lang: lang of spell
        :return: Monster object
        """

        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': map_id})[0])

        map = Map(map_id, None, data.get('name', ''), data.get('description', ''),
                  data.get('map_file', None))

        sql = self.database.select('Map_item', {'map_id': id})

        mapItems = []
        for line in sql:
            mapItem = MapItemDAO().get(line['ID'])
            mapItems.append(mapItem)
        map.mapItems = mapItems

        return map


    def get_all(self, lang=None) -> list:
        pass
