from structure.enums.Alignment import Alignment
from structure.enums.Classes import Classes
from structure.enums.NodeType import NodeType
from structure.enums.ObjectType import ObjectType
from structure.enums.Races import Races
from structure.general.Object import Object
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.Item import Item
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon


class PartyCharacter(Object):
    TABLE_SCHEMA = [
        'id', 'name', 'description', 'deviceName', 'MACAddress'
    ]


    def __init__(self, id: int = None, lang: str = None, name: str = None, description: str = None,
                 deviceName: str = None, MACAddress: str = None):
        super().__init__(id, lang, name, description)

        self.__character = None
        self.__messages = []
        self.__deviceName = deviceName
        self.__MACAddress = MACAddress


    def __name__(self):
        names = super().__name__()
        names.append('PartyCharacter')
        return names


    @staticmethod
    def DAO():
        from data.DAO.PartyCharacterDAO import PartyCharacterDAO
        return PartyCharacterDAO


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLPartyCharacter import XMLPartyCharacter
        return XMLPartyCharacter


    @staticmethod
    def layout():
        return None


    @property
    def children(self):
        return []


    @property
    def treeChildren(self):
        return [] + super().treeChildren


    @property
    def icon(self):
        return 'resources/icons/helmet.png'


    @property
    def object_type(self):
        return ObjectType.PARTY_CHARACTER


    @property
    def character(self):
        return self.__character


    @character.setter
    def character(self, value):
        self.__character = value


    @property
    def messages(self):
        return self.__messages


    @messages.setter
    def messages(self, value):
        self.__messages = value


    @property
    def deviceName(self):
        return self.__deviceName


    @deviceName.setter
    def deviceName(self, value):
        self.__deviceName = value


    @property
    def MACAddress(self):
        return self.__MACAddress


    @MACAddress.setter
    def MACAddress(self, value):
        self.__MACAddress = value


    def __eq__(self, other):
        return False
