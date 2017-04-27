from PyQt5.QtCore import QPointF

from data.DAO.DAO import DAO
from data.DAO.MapItemDAO import MapItemDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.database.Database import Database
from structure.enums.ObjectType import ObjectType
from structure.map.Map import Map
from structure.map.MapItem import MapItem
from structure.tree.NodeObject import NodeObject


class MapDAO(DAO):
    DATABASE_TABLE = 'Map'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.MAP


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, map: Map, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        values = {
            'name'       : map.name,
            'description': map.description,
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
        Delete spell from database and all his translates
        :param spell_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, map_id)


    def get(self, map_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Map:
        """
        Get spell from database
        :param monster_id: id of spell
        :param lang: lang of spell
        :return: Monster object
        """

        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': map_id})[0])

        map = Map(map_id, None, data.get('name', ''), data.get('description', ''),
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
        pass


    def create_map_image(self, map: Map):
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