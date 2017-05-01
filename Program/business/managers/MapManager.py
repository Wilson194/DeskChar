from business.managers.interface.IMapManager import IMapManager
from data.DAO.MapDAO import MapDAO
from data.DAO.ModifierDAO import ModifierDAO
from structure.effects.Modifier import Modifier
from structure.enums.ObjectType import ObjectType
from structure.map.Map import Map

import os
import shutil


class MapManager(IMapManager):
    MAP_FOLDER = 'resources/maps/'


    def __init__(self):
        self.DAO = MapDAO()


    def create(self, map: Map, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        return self.DAO.create(map, nodeParentId, contextType)


    def update(self, map: Map):
        mapItems = []
        for mapItemDraw in map.mapItemDraws:
            mapItem = mapItemDraw.get_object()
            mapItems.append(mapItem)

        map.mapItems = mapItems

        self.DAO.update(map)


    def delete(self, mapId: int):
        return self.DAO.delete(mapId)


    def create_empty(self, lang):
        pass


    def get(self, mapId: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Map:
        return self.DAO.get(mapId, lang, nodeId, contextType)


    def get_all(self, lang=None) -> list:
        return self.DAO.get_all(lang)


    def copy_map(self, filePath: str, map: Map):
        extension = os.path.splitext(filePath)[1]
        name = 'map-{}{}'.format(str(map.id), extension)

        if not os.path.exists(self.MAP_FOLDER):
            os.mkdir(self.MAP_FOLDER)

        if os.path.exists(self.MAP_FOLDER + name):
            os.remove(self.MAP_FOLDER + name)

        shutil.copy2(filePath, self.MAP_FOLDER + name)

        return self.MAP_FOLDER + name
