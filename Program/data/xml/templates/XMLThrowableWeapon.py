from data.xml.templates.XMLTemplate import XMLTemplate, XElement, XAttribElement
from structure.enums.Items import Items
from structure.enums.WeaponWeight import WeaponWeight


class XMLThrowableWeapon(XMLTemplate):
    ROOT_NAME = 'throwableWeapon'
    OBJECT_TYPE = Items.THROWABLE_WEAPON


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
        self.defence = XElement('defence')
        self.weaponWeight = XElement('weaponWeight', WeaponWeight)
