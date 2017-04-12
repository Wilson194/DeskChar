from data.xml.templates.XMLEffectl import XMLEffect
from data.xml.templates.XMLTemplate import XMLTemplate, XAttribElement, XElement, XInstance
from structure.enums.Items import Items


class XMLContainer(XMLTemplate):
    ROOT_NAME = 'container'
    OBJECT_TYPE = Items.CONTAINER


    def __init__(self):
        self.id = XElement('id')
        self.parent_id = XElement('parentId')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')
        self.price = XElement('price')
        self.quality = XElement('quality')
        self.weight = XElement('weight')
        self.capacity = XElement('capacity')

        self.effects = XInstance('effects', XMLEffect)

