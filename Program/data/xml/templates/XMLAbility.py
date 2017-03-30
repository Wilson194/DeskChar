from data.xml.templates.XMLTemplate import XMLTemplate, XElement, XAttribElement, XInstance
from structure.enums.Classes import Classes
from structure.enums.ObjectType import ObjectType

from structure.enums.Races import Races


class XMLAbility(XMLTemplate):
    ROOT_NAME = 'ability'
    OBJECT_TYPE = ObjectType.ABILITY


    def __init__(self):
        self.id = XElement('id')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')
        self.chance = XAttribElement('chance', 'lang')
        self.drd_race = XElement('race', Races)
        self.drd_class = XElement('class', Classes)
