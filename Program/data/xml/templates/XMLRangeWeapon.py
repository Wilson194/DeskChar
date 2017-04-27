from data.xml.templates.XMLEffectl import XMLEffect
from data.xml.templates.XMLTemplate import XMLTemplate, XElement, XAttribElement, XInstance
from structure.enums.Items import Items
from structure.enums.Races import Races
from structure.enums.WeaponWeight import WeaponWeight


class XMLRangeWeapon(XMLTemplate):
    ROOT_NAME = 'rangedWeapon'
    OBJECT_TYPE = Items.RANGED_WEAPON


    def __init__(self):
        self.id = XElement('id')
        self.parent_id = XElement('parentId')
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
        self.amount = XElement('amount')

        self.weaponWeight = XElement('weaponWeight', WeaponWeight)
        self.racial = XElement('racial', Races)

        self.effects = XInstance('effects', XMLEffect)
