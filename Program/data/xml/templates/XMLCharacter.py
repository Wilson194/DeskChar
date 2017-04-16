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
from structure.enums.Classes import Classes
from structure.enums.ObjectType import ObjectType
from data.xml.templates.XMLTemplate import XInstance, XElement, XAttribElement
from structure.enums.Races import Races


class XMLCharacter(XMLTemplate):
    ROOT_NAME = 'character'
    OBJECT_TYPE = ObjectType.CHARACTER


    def __init__(self):
        self.id = XElement('id')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')

        self.agility = XElement('agility')
        self.charisma = XElement('charisma')
        self.intelligence = XElement('intelligence')
        self.mobility = XElement('mobility')
        self.strength = XElement('strength')
        self.toughness = XElement('toughness')

        self.age = XElement('age')
        self.height = XElement('height')
        self.weight = XElement('weight')
        self.level = XElement('level')
        self.xp = XElement('xp')
        self.maxHealth = XElement('maxHealth')
        self.maxMana = XElement('maxMana')
        self.currentHealth = XElement('currentHealth')
        self.currentMana = XElement('currentMana')

        # self.drdClass = XElement('class', Classes)
        # self.drdRace = XElement('race', Races)
        self.alignment = XElement('alignment', Alignment)

        self.spells = XInstance('spells', XMLSpell)
        self.abilities = XInstance('abilities', XMLAbility)
        self.effects = XInstance('effects', XMLEffect)

        self.items = XInstance('items', XMLItem)
        self.armors = XInstance('armors', XMLArmor)
        self.containers = XInstance('containers', XMLContainer)
        self.meleeWeapons = XInstance('meleeWeapons', XMLMeleeWeapon)
        self.rangedWeapons = XInstance('rangedWeapons', XMLRangeWeapon)
        self.moneyList = XInstance('moneyList', XMLMoney)
        self.throwableWeapons = XInstance('throwableWeapons', XMLThrowableWeapon)
