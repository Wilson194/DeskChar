from data.xml.templates.XMLCharacter import XMLCharacter
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.enums.ObjectType import ObjectType
from data.xml.templates.XMLTemplate import XInstance, XElement, XAttribElement


class XMLPartyCharacter(XMLTemplate):
    ROOT_NAME = 'partyCharacter'
    OBJECT_TYPE = ObjectType.PARTY_CHARACTER


    def __init__(self):
        self.id = XElement('id')
        self.deviceName = XElement('deviceName')
        self.MACAddress = XElement('MACAddress')
        self.name = XElement('name')

        self.character = XInstance('character', XMLCharacter, True)
