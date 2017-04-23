from data.xml.templates.XMLAbility import XMLAbility
from data.xml.templates.XMLArmor import XMLArmor
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

from structure.enums.MonsterRace import MonsterRace
from structure.enums.MonsterSize import MonsterSize
from structure.enums.ObjectType import ObjectType
from data.xml.templates.XMLTemplate import XInstance, XElement, XAttribElement


class XMLMonster(XMLTemplate):
    ROOT_NAME = 'monster'
    OBJECT_TYPE = ObjectType.MONSTER


    def __init__(self):
        self.id = XElement('id')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')

        self.viability = XElement('viability')
        self.offense = XAttribElement('offense', 'lang')
        self.defense = XElement('defense')
        self.endurance = XElement('endurance')
        self.rampancy = XElement('pugnacity')
        self.mobility = XElement('mobility')
        self.perseverance = XElement('perseverance')
        self.intelligence = XElement('intelligence')
        self.charisma = XElement('charisma')
        self.alignment = XElement('alignment', Alignment)
        self.experience = XElement('experience')
        self.hp = XElement('HP')

        self.monsterRace = XElement('race', MonsterRace)
        self.size = XElement('size', MonsterSize)

        self.spells = XInstance('spells', XMLSpell)
        self.abilities = XInstance('abilities', XMLAbility)

        self.items = XInstance('items', XMLItem)
        self.armors = XInstance('items', XMLArmor)
        self.containers = XInstance('items', XMLContainer)
        self.meleeWeapons = XInstance('items', XMLMeleeWeapon)
        self.rangedWeapons = XInstance('items', XMLRangeWeapon)
        self.moneyList = XInstance('items', XMLMoney)
        self.throwableWeapons = XInstance('items', XMLThrowableWeapon)
