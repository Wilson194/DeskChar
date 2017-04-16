from data.xml.templates.XMLAbility import XMLAbility
from data.xml.templates.XMLArmor import XMLArmor
from data.xml.templates.XMLCharacter import XMLCharacter
from data.xml.templates.XMLContainer import XMLContainer
from data.xml.templates.XMLEffectl import XMLEffect
from data.xml.templates.XMLItem import XMLItem
from data.xml.templates.XMLMeleeWeapon import XMLMeleeWeapon
from data.xml.templates.XMLMoney import XMLMoney
from data.xml.templates.XMLRangeWeapon import XMLRangeWeapon
from data.xml.templates.XMLSpell import XMLSpell
from data.xml.templates.XMLTemplate import XMLTemplate
from data.xml.templates.XMLThrowableWeapon import XMLThrowableWeapon
from structure.enums.Alignment import Alignment
from structure.enums.Classes import Classes
from structure.enums.ObjectType import ObjectType
from data.xml.templates.XMLTemplate import XInstance, XElement, XAttribElement
from structure.enums.Races import Races


class XMLPartyCharacter(XMLTemplate):
    ROOT_NAME = 'partyCharacter'
    OBJECT_TYPE = ObjectType.PARTY_CHARACTER


    def __init__(self):
        self.id = XElement('id')
        self.deviceName = XElement('deviceName')
        self.MACAddress = XElement('MACAddress')

        self.character = XInstance('character', XMLCharacter, True)
