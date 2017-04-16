from data.xml.templates.XMLEffectl import XMLEffect
from data.xml.templates.XMLTemplate import XMLTemplate, XElement, XAttribElement, XInstance
from structure.enums.Items import Items


class XMLArmor(XMLTemplate):
    ROOT_NAME = 'armor'
    OBJECT_TYPE = Items.ARMOR


    def __init__(self):
        self.id = XElement('id')
        self.parent_id = XElement('parentId')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')
        self.price = XElement('price')
        self.quality = XElement('quality')
        self.weightA = XElement('weightA')
        self.weightB = XElement('weightB')
        self.weightC = XElement('weightC')
        self.size = XElement('size')
        self.amount = XElement('amount')

        self.effects = XInstance('effects', XMLEffect)
