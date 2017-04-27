from data.xml.templates.XMLTemplate import XMLTemplate
from structure.enums.Classes import Classes
from structure.enums.ObjectType import ObjectType
from data.xml.templates.XMLTemplate import XInstance, XElement, XAttribElement


class XMLMessage(XMLTemplate):
    ROOT_NAME = 'message'
    OBJECT_TYPE = ObjectType.MESSAGE


    def __init__(self):
        self.id = XElement('id')
        self.date = XElement('date', valueType='DATETIME')

        self.text = XElement('text')
        self.isMine = XElement('isMine')
