from data.xml.templates.XMLTemplate import XMLTemplate, XElement, XAttribElement
from structure.enums.Items import Items


class XMLRangeWeapon(XMLTemplate):
    ROOT_NAME = 'rangedWeapon'
    OBJECT_TYPE = Items.RANGED_WEAPON


    def __init__(self):
        self.id = XElement('id')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')
        self.price = XElement('price')
        self.weight = XElement('weight')
        self.initiative = XElement('initiative')
        self.strength = XElement('strength')
        self.rampancy = XElement('rampancy')
        self.rangeLow = XElement('rangeLow')
        self.rangeMedium = XElement('rangeMedium')
        self.rangeHigh = XElement('rangeHigh')
