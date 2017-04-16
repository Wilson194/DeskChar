from data.DAO.LocationDAO import LocationDAO
from structure.scenario.Location import Location


class LocationManager:
    def __init__(self):
        self.DAO = LocationDAO()


    def update_location(self, location: Location):
        self.DAO.update(location)
