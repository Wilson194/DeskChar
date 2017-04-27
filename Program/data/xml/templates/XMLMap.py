from data.xml.templates.XMLAbilityContext import XMLAbilityContext
from data.xml.templates.XMLMapItem import XMLMapItem
from data.xml.templates.XMLTemplate import XMLTemplate, XElement, XAttribElement, XInstance
from structure.enums.Classes import Classes
from structure.enums.ObjectType import ObjectType

from structure.enums.Races import Races


class XMLMap(XMLTemplate):
    ROOT_NAME = 'map'
    OBJECT_TYPE = ObjectType.MAP


    def __init__(self):
        # self.id = XElement('id')
        self.name = XElement('name')
        self.description = XElement('description')
        self.XMLMap = XElement('filePath')

        self.mapItems = XInstance('mapItems', XMLMapItem)
