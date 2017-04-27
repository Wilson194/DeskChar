from data.xml.templates.XMLEffectl import XMLEffect
from data.xml.templates.XMLTemplate import XMLTemplate, XAttribElement, XElement, XInstance
from structure.enums.Handling import Handling
from structure.enums.Items import Items
from structure.enums.Races import Races
from structure.enums.WeaponWeight import WeaponWeight


class XMLMeleeWeapon(XMLTemplate):
    ROOT_NAME = 'meleeWeapon'
    OBJECT_TYPE = Items.MELEE_WEAPON


    def __init__(self):
        self.id = XElement('id')
        self.parent_id = XElement('parentId')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')
        self.price = XElement('price')
        self.weight = XElement('weight')
        self.strength = XElement('strength')
        self.rampancy = XElement('rampancy')
        self.defence = XElement('defence')
        self.length = XElement('length')
        self.amount = XElement('amount')
        self.initiative = XElement('initiative')

        self.weaponWeight = XElement('weaponWeight', WeaponWeight)
        self.handling = XElement('handling', Handling)
        self.racial = XElement('racial', Races)

        self.effects = XInstance('effects', XMLEffect)