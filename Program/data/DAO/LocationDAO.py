from data.DAO.CharacterDAO import CharacterDAO
from data.DAO.ItemDAO import ItemDAO
from data.DAO.MapDAO import MapDAO
from data.DAO.MonsterDAO import MonsterDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.SettingsDAO import SettingsDAO
from data.DAO.interface.ILocationDAO import ILocationDAO
from data.database.ObjectDatabase import ObjectDatabase
from structure.enums.ObjectType import ObjectType
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon

from data.DAO.DAO import DAO
from structure.scenario.Location import Location
from structure.tree.NodeObject import NodeObject


class LocationDAO(DAO, ILocationDAO):
    DATABASE_TABLE = 'Location'
    TYPE = ObjectType.LOCATION


    def __init__(self):
        self.database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, location: Location, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new location        
        :param location: Location object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created location
        """

        if not contextType:
            contextType = self.TYPE

        strValues = {
            'name'       : location.name,
            'description': location.description
        }

        id = self.database.insert_null(self.DATABASE_TABLE)
        location.id = id

        self.database.insert_translate(strValues, location.lang, id, self.TYPE)

        # Create node for tree structure
        node = NodeObject(None, location.name, nodeParentId, location)
        nodeId = self.treeDAO.insert_node(node, contextType)

        for one in location.containers + location.armors + location.moneyList + location.meleeWeapons + location.rangedWeapons + location.throwableWeapons + location.items:
            ItemDAO().create(one, nodeId, contextType)

        for monster in location.monsters:
            MonsterDAO().create(monster, nodeId, contextType)

        for one in location.locations:
            self.create(one, nodeId, contextType)

        for character in location.characters:
            CharacterDAO().create(character, nodeId, contextType)

        return id


    def update(self, location: Location):
        """
        Update location in database
        :param location: Location object with new data
        """
        strValues = {
            'name'       : location.name,
            'description': location.description
        }

        self.database.update_translate(strValues, location.lang, location.id, self.TYPE)


    def delete(self, location_id: int):
        """
        Delete Location from database and from translate
        :param location_id: id of Location
        """
        self.database.delete(self.DATABASE_TABLE, location_id)
        self.database.delete_where('translates',
                                   {'target_id': location_id, 'type': self.TYPE})


    def get(self, location_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Location:
        """
        Get Location , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param location_id: id of Location
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Location object
        """
        if lang is None:
            lang = SettingsDAO().get_value('language', str)
        data = self.database.select(self.DATABASE_TABLE, {'ID': location_id})
        if not data:
            return None
        else:
            data = dict(data[0])

        tr_data = dict(self.database.select_translate(location_id, self.TYPE.value,
                                                      lang))

        location = Location(data.get('ID'), lang, tr_data.get('name', ''),
                            tr_data.get('description', ''))

        if nodeId and contextType:
            children = self.treeDAO.get_children_objects(nodeId, contextType)
            locations = []
            monsters = []
            characters = []
            items = []
            armors = []
            moneys = []
            containers = []
            meleeWeapons = []
            rangedWeapons = []
            throwableWeapons = []
            maps = []

            for child in children:
                if child.object.object_type is ObjectType.LOCATION:
                    childLocation = self.get(child.object.id, None, child.id, contextType)
                    locations.append(childLocation)
                elif child.object.object_type is ObjectType.MONSTER:
                    monster = MonsterDAO().get(child.object.id, None, child.id, contextType)
                    monsters.append(monster)
                elif child.object.object_type is ObjectType.CHARACTER:
                    character = CharacterDAO().get(child.object.id, None, child.id, contextType)
                    characters.append(character)
                elif child.object.object_type is ObjectType.MAP:
                    map = MapDAO().get(child.object.id)
                    maps.append(map)
                elif child.object.object_type is ObjectType.ITEM:
                    childItem = ItemDAO().get(child.object.id, None, child.id, contextType)
                    if isinstance(childItem, Armor):
                        armors.append(childItem)
                    elif isinstance(childItem, Container):
                        containers.append(childItem)
                    elif isinstance(childItem, Money):
                        moneys.append(childItem)
                    elif isinstance(childItem, MeleeWeapon):
                        meleeWeapons.append(childItem)
                    elif isinstance(childItem, RangeWeapon):
                        rangedWeapons.append(childItem)
                    elif isinstance(childItem, ThrowableWeapon):
                        throwableWeapons.append(childItem)
                    else:
                        items.append(childItem)

            location.items = items
            location.armors = armors
            location.moneyList = moneys
            location.containers = containers
            location.meleeWeapons = meleeWeapons
            location.rangedWeapons = rangedWeapons
            location.throwableWeapons = throwableWeapons
            location.locations = locations
            location.monsters = monsters
            location.characters = characters
            location.maps = maps

        return location


    def get_all(self, lang=None) -> list:
        """
        Get list of locations for selected lang
        :param lang: lang of locations
        :return: list of locations
        """
        if lang is None:
            lang = SettingsDAO().get_value('language', str)
        lines = self.database.select_all(self.DATABASE_TABLE)
        items = []
        for line in lines:
            item = self.get(line['ID'], lang)
            items.append(item)
        return items
