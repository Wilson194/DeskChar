from data.xml.templates.XMLArmor import XMLArmor
from data.xml.templates.XMLEffectl import XMLEffect
from data.xml.templates.XMLItem import XMLItem
from data.xml.templates.XMLMeleeWeapon import XMLMeleeWeapon
from data.xml.templates.XMLMoney import XMLMoney
from data.xml.templates.XMLRangeWeapon import XMLRangeWeapon
from data.xml.templates.XMLTemplate import XMLTemplate, XAttribElement, XElement, XInstance
from data.xml.templates.XMLThrowableWeapon import XMLThrowableWeapon
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
        self.amount = XElement('amount')

        self.effects = XInstance('effects', XMLEffect)

        self.items = XInstance('items', XMLItem)
        self.armors = XInstance('items', XMLArmor)
        self.containers = XInstance('items', XMLContainer)
        self.meleeWeapons = XInstance('items', XMLMeleeWeapon)
        self.rangedWeapons = XInstance('items', XMLRangeWeapon)
        self.moneyList = XInstance('items', XMLMoney)
        self.throwableWeapons = XInstance('items', XMLThrowableWeapon)
