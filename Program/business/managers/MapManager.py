from data.DAO.MapDAO import MapDAO
from data.DAO.ModifierDAO import ModifierDAO
from structure.effects.Modifier import Modifier
from structure.map.Map import Map

import os
import shutil


class MapManager:
    MAP_FOLDER = 'resources/maps/'


    def __init__(self):
        self.DAO = MapDAO()


    def update(self, map: Map):
        mapItems = []
        for mapItemDraw in map.mapItemDraws:
            mapItem = mapItemDraw.get_object()
            mapItems.append(mapItem)

        map.mapItems = mapItems

        self.DAO.update(map)


    def create_empty(self, lang):
        pass


    def copy_map(self, filePath: str, map: Map):
        extension = os.path.splitext(filePath)[1]
        name = 'map-{}{}'.format(str(map.id), extension)

        if os.path.exists(self.MAP_FOLDER + name):
            os.remove(self.MAP_FOLDER + name)

        shutil.copy2(filePath,self.MAP_FOLDER + name)

        return self.MAP_FOLDER + name

