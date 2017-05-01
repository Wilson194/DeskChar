from business.managers.interface.ILocationManager import ILocationManager
from data.DAO.LocationDAO import LocationDAO
from structure.enums.ObjectType import ObjectType
from structure.scenario.Location import Location


class LocationManager(ILocationManager):
    def __init__(self):
        self.DAO = LocationDAO()


    def create(self, location: Location, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        return self.DAO.create(location, nodeParentId, contextType)


    def update_location(self, location: Location):
        return self.DAO.update(location)


    def delete(self, locationId: int):
        return self.DAO.delete(locationId)


    def get(self, locationId: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Location:
        return self.DAO.get(locationId, lang, nodeId, contextType)


    def get_all(self, lang=None) -> list:
        return self.DAO.get_all(lang)


    def create_empty(self, lang: str) -> Location:
        item = Location(None, lang)
        id = self.DAO.create(item)
        item.id = id

        return item
