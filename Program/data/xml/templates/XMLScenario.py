from data.xml.templates.XMLAbility import XMLAbility
from data.xml.templates.XMLArmor import XMLArmor
from data.xml.templates.XMLCharacter import XMLCharacter
from data.xml.templates.XMLContainer import XMLContainer
from data.xml.templates.XMLEffectl import XMLEffect
from data.xml.templates.XMLItem import XMLItem
from data.xml.templates.XMLLocation import XMLLocation
from data.xml.templates.XMLMeleeWeapon import XMLMeleeWeapon
from data.xml.templates.XMLMoney import XMLMoney
from data.xml.templates.XMLPartyCharacter import XMLPartyCharacter
from data.xml.templates.XMLRangeWeapon import XMLRangeWeapon
from data.xml.templates.XMLSpell import XMLSpell
from data.xml.templates.XMLTemplate import XMLTemplate
from data.xml.templates.XMLThrowableWeapon import XMLThrowableWeapon
from structure.enums.Alignment import Alignment

from structure.enums.MonsterRace import MonsterRace
from structure.enums.MonsterSize import MonsterSize
from structure.enums.ObjectType import ObjectType
from data.xml.templates.XMLTemplate import XInstance, XElement, XAttribElement


class XMLScenario(XMLTemplate):
    ROOT_NAME = 'scenario'
    OBJECT_TYPE = ObjectType.SCENARIO


    def __init__(self):
        self.id = XElement('id')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')
        self.date = XElement('date')

        self.party = XInstance('party', XMLPartyCharacter)
        self.npc = XInstance('scenarioCharacters', XMLCharacter)

        self.locations = XInstance('locations', XMLLocation)

        self.effects = XInstance('effects', XMLEffect)
        self.spells = XInstance('spells', XMLSpell)
        self.abilities = XInstance('abilities', XMLAbility)

        self.items = XInstance('items', XMLItem)
        self.armors = XInstance('items', XMLArmor)
        self.containers = XInstance('items', XMLContainer)
        self.meleeWeapons = XInstance('items', XMLMeleeWeapon)
        self.rangedWeapons = XInstance('items', XMLRangeWeapon)
        self.moneyList = XInstance('items', XMLMoney)
        self.throwableWeapons = XInstance('items', XMLThrowableWeapon)
