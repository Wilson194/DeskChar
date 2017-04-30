from data.DAO.DAO import DAO
from data.DAO.MapItemDAO import MapItemDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.interface.IMapDAO import IMapDAO
from data.database.Database import Database
from structure.enums.ObjectType import ObjectType
from structure.map.Map import Map
from structure.tree.NodeObject import NodeObject
import os


class MapDAO(DAO, IMapDAO):
    DATABASE_TABLE = 'Map'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.MAP


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, map: Map, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new map and create empty map image, because of exporting        
        :param map: Map object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created map
        """
        if contextType is None:
            contextType = self.TYPE

        values = {
            'name'       : map.name if map.name else '',
            'description': map.description if map.description else '',
            'map_file'   : map.mapFile,
        }

        id = self.database.insert(self.DATABASE_TABLE, values)
        map.id = id

        node = NodeObject(None, map.name, nodeParentId, map)
        nodeId = self.treeDAO.insert_node(node, contextType)

        for mapItem in map.mapItems:
            mapItem.mapId = id
            MapItemDAO().create(mapItem)

        self.create_map_image(map)
        return id


    def update(self, map: Map):
        """
        Update map in database
        :param map: Location object with new data
        """
        values = {
            'name'       : map.name,
            'description': map.description,
            'map_file'   : map.mapFile,
        }

        self.database.set_many(True)
        for mapItem in map.mapItems:
            MapItemDAO().update(mapItem)

        self.database.insert_many_execute()
        self.database.set_many(False)

        self.database.update(self.DATABASE_TABLE, map.id, values)


    def delete(self, map_id: int):
        """
        Delete Map from database and from translate and delete all maps linked with map
        :param map_id: id of Map
        """
        map = self.get(map_id)
        self.database.delete(self.DATABASE_TABLE, map_id)
        os.remove(map.mapFile)
        os.remove('resources/maps/exportedMap-1.png')


    def get(self, map_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Map:
        """
        Get Map , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param map_id: id of Map
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Map object
        """

        data = self.database.select(self.DATABASE_TABLE, {'ID': map_id})

        if not data:
            return None
        else:
            data = dict(data[0])

        map = Map(map_id, None, data.get('name', ' '), data.get('description', ' '),
                  data.get('map_file', None))

        sql = self.database.select('Map_item', {'map_id': map.id})

        map.XMLMap = 'map-{}.png'.format(map_id)
        mapItems = []
        for line in sql:
            mapItem = MapItemDAO().get(line['ID'])
            mapItems.append(mapItem)
        map.mapItems = mapItems

        return map


    def get_all(self, lang=None) -> list:
        """
        Get list of maps for selected lang
        :param lang: lang of maps
        :return: list of maps
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)
        maps = []
        for line in lines:
            item = self.get(line['ID'], lang)
            maps.append(item)
        return maps


    def create_map_image(self, map: Map) -> None:
        """
        Create empty image for map, important because of exporting
        :param map: map object         
        """
        from PyQt5.QtWidgets import QGraphicsView
        from PyQt5.QtWidgets import QGraphicsScene
        from PyQt5.QtGui import QPainter, QPixmap
        from PyQt5.QtGui import QImage
        from presentation.widgets.MapWidget import MapItemDraw

        grview = QGraphicsView()
        grview.setRenderHints(grview.renderHints() | QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        scene = QGraphicsScene()
        grview.setScene(scene)
        if not map.mapFile:
            mapFile = 'resources/icons/no_map.png'
        else:
            mapFile = map.mapFile
        pixMap = QPixmap(mapFile)
        sceneMap = scene.addPixmap(pixMap)

        for num, mapItem in enumerate(map.mapItems):
            mapItem.number = num + 1
            item = MapItemDraw(mapItem, None)
            scene.addItem(item)
            # self.map.addMapItemDraws(item)

        scene.setSceneRect(scene.itemsBoundingRect())
        img = QImage(scene.sceneRect().size().toSize(), QImage.Format_ARGB32)

        painter = QPainter(img)
        scene.render(painter)

        name = 'resources/maps/exportedMap-{}.png'.format(map.id)
        img.save(name)

        del painter
