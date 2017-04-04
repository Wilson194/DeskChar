from data.xml.templates.XMLTemplate import XMLTemplate, XElement, XInstance, XAttribElement
from structure.enums.Items import Items


class XMLItem(XMLTemplate):
    ROOT_NAME = 'item'
    OBJECT_TYPE = Items.GENERIC


    def __init__(self):
        self.id = XElement('id')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')
        self.price = XElement('price')
        self.weight = XElement('weight')
