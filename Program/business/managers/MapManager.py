from data.DAO.MapDAO import MapDAO
from data.DAO.ModifierDAO import ModifierDAO
from structure.effects.Modifier import Modifier
from structure.map.Map import Map


class MapManager:
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
