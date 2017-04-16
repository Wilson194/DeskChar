from structure.enums.Handling import Handling
from structure.enums.WeaponWeight import WeaponWeight
from structure.items.Item import *


class MeleeWeapon(Item):
    TABLE_SCHEMA = ['id', 'name', 'description', 'weight', 'price', 'strength', 'rampancy',
                    'defence', 'length', 'weaponWeight', 'handling', 'type', 'amount']


    def __init__(self, id: int = None, lang=None, name: str = None,
                 description: str = None, parent_id: int = None, weight: int = None,
                 price: int = None, strength: int = None,
                 rampancy: int = None, defence: int = None, length: int = None,
                 weaponWeight: WeaponWeight = None, handling: Handling = None, amount: int = 1):
        super().__init__(id, lang, name, description, parent_id, weight, price, amount)

        self.__strength = strength
        self.__rampancy = rampancy
        self.__defence = defence
        self.__length = length
        self.__weaponWeight = weaponWeight
        self.__handling = handling
        self.__type = Items.MELEE_WEAPON


    def __name__(self):
        names = super().__name__()
        names.append('MeleeWeapon')
        return names


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLMeleeWeapon import XMLMeleeWeapon
        return XMLMeleeWeapon


    @staticmethod
    def layout():
        from presentation.layouts.MeleeWeaponLayout import MeleeWeaponLayout
        return MeleeWeaponLayout


    @property
    def icon(self):
        return 'resources/icons/axe.png'


    @property
    def strength(self):
        return self.__strength


    @strength.setter
    def strength(self, value):
        self.__strength = value


    @property
    def rampancy(self):
        return self.__rampancy


    @rampancy.setter
    def rampancy(self, value):
        self.__rampancy = value


    @property
    def defence(self):
        return self.__defence


    @defence.setter
    def defence(self, value):
        self.__defence = value


    @property
    def length(self):
        return self.__length


    @length.setter
    def length(self, value):
        self.__length = value


    @property
    def weaponWeight(self):
        return self.__weaponWeight


    @weaponWeight.setter
    def weaponWeight(self, value):
        self.__weaponWeight = value


    @property
    def handling(self):
        return self.__handling


    @handling.setter
    def handling(self, value):
        self.__handling = value


    @property
    def type(self):
        return self.__type
