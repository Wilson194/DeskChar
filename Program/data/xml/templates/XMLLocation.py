from data.xml.templates.XMLAbility import XMLAbility
from data.xml.templates.XMLArmor import XMLArmor
from data.xml.templates.XMLCharacter import XMLCharacter
from data.xml.templates.XMLContainer import XMLContainer
from data.xml.templates.XMLEffectl import XMLEffect
from data.xml.templates.XMLItem import XMLItem
from data.xml.templates.XMLMap import XMLMap
from data.xml.templates.XMLMeleeWeapon import XMLMeleeWeapon
from data.xml.templates.XMLMoney import XMLMoney
from data.xml.templates.XMLMonster import XMLMonster
from data.xml.templates.XMLRangeWeapon import XMLRangeWeapon
from data.xml.templates.XMLSpell import XMLSpell
from data.xml.templates.XMLTemplate import XMLTemplate
from data.xml.templates.XMLThrowableWeapon import XMLThrowableWeapon
from structure.enums.Alignment import Alignment

from structure.enums.MonsterRace import MonsterRace
from structure.enums.MonsterSize import MonsterSize
from structure.enums.ObjectType import ObjectType
from data.xml.templates.XMLTemplate import XInstance, XElement, XAttribElement


class XMLLocation(XMLTemplate):
    ROOT_NAME = 'location'
    OBJECT_TYPE = ObjectType.LOCATION


    def __init__(self):
        self.id = XElement('id')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')

        self.monsters = XInstance('monsters', XMLMonster)
        self.locations = XInstance('locations', XMLLocation)
        self.maps = XInstance('maps', XMLMap)

        self.characters = XInstance('scenarioCharacters', XMLCharacter)

        self.items = XInstance('items', XMLItem)
        self.armors = XInstance('items', XMLArmor)
        self.containers = XInstance('items', XMLContainer)
        self.meleeWeapons = XInstance('items', XMLMeleeWeapon)
        self.rangedWeapons = XInstance('items', XMLRangeWeapon)
        self.moneyList = XInstance('items', XMLMoney)
        self.throwableWeapons = XInstance('items', XMLThrowableWeapon)
