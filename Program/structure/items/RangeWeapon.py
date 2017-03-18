from structure.enums.Items import Items
from structure.items.Item import Item


class RangeWeapon(Item):
    TABLE_SCHEMA = ['id', 'name', 'description', 'weight', 'price', 'initiative', 'strength',
                    'rampancy', 'rangeLow', 'rangeMedium', 'rangeHigh', 'type']


    def __init__(self, id: int = None, lang=None, name: str = None,
                 description: str = None, parent_id: int = None, weight: int = None,
                 price: int = None,
                 initiative: int = None, strength: int = None, rampancy: int = None,
                 rangeLow: int = None, rangeMedium: int = None, rangeHigh: int = None):
        super().__init__(id, lang, name, description, parent_id, weight, price)

        self.__initiative = initiative
        self.__strength = strength
        self.__rampancy = rampancy
        self.__rangeLow = rangeLow
        self.__rangeMedium = rangeMedium
        self.__rangeHigh = rangeHigh

        self.__type = Items.RANGED_WEAPON


    def __name__(self):
        names = super().__name__()
        names.append('RangeWeapon')
        return names


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLRangeWeapon import XMLRangeWeapon
        return XMLRangeWeapon


    @staticmethod
    def layout():
        from presentation.layouts.RangeWeaponLayout import RangeWeaponLayout
        return RangeWeaponLayout


    @property
    def icon(self):
        return 'resources/icons/bow.png'


    @property
    def initiative(self):
        return self.__initiative


    @initiative.setter
    def initiative(self, value):
        self.__initiative = value


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
    def rangeLow(self):
        return self.__rangeLow


    @rangeLow.setter
    def rangeLow(self, value):
        self.__rangeLow = value


    @property
    def rangeMedium(self):
        return self.__rangeMedium


    @rangeMedium.setter
    def rangeMedium(self, value):
        self.__rangeMedium = value


    @property
    def rangeHigh(self):
        return self.__rangeHigh


    @rangeHigh.setter
    def rangeHigh(self, value):
        self.__rangeHigh = value
