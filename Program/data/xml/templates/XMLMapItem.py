from data.xml.templates.XMLAbilityContext import XMLAbilityContext
from data.xml.templates.XMLTemplate import XMLTemplate, XElement, XAttribElement, XInstance
from structure.enums.Classes import Classes
from structure.enums.MapItem import MapItemType
from structure.enums.ObjectType import ObjectType

from structure.enums.Races import Races


class XMLMapItem(XMLTemplate):
    ROOT_NAME = 'mapItem'
    OBJECT_TYPE = ObjectType.MAP_ITEM


    def __init__(self):
        # self.id = XElement('id')
        self.name = XElement('name')
        self.description = XElement('text')
        self.number = XElement('number')
        self.itemType = XElement('mapItemType', MapItemType)
