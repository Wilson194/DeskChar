from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object


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
        if isinstance(other, PartyCharacter):
            if super().__eq__(other) and self.MACAddress == other.MACAddress and self.deviceName == other.deviceName:
                return True
        return False


    def printer(self, depth: int, full: bool = False):
        print('{}PartyCharacter - {}'.format(depth * '  ', self.deviceName))
        print('{}   Character:'.format(depth * '  ', self.deviceName))

        if full:
            print('{}   deviceName: {}'.format(depth * '  ', self.deviceName))
            print('{}   MACAddress: {}'.format(depth * '  ', self.MACAddress))

        if self.character:
            self.character.printer(depth, full)
        else:
            print('{}      None'.format(depth * '  '))

    def __hash__(self):
        return hash((self.object_type, self.id))