from data.xml.templates.XMLTemplate import XMLTemplate, XElement, XAttribElement
from structure.enums.Items import Items


class XMLMoney(XMLTemplate):
    ROOT_NAME = 'money'
    OBJECT_TYPE = Items.MONEY


    def __init__(self):
        self.id = XElement('id')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')
        self.copper = XElement('copper')
        self.silver = XElement('silver')
        self.gold = XElement('gold')
