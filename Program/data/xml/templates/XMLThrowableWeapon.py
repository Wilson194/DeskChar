from data.DAO.ItemDAO import ItemDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.enums.Handling import Handling
from structure.enums.WeaponWeight import WeaponWeight
from structure.items.Container import Container
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon


class XMLThrowableWeapon(XMLTemplate):
    ROOT_NAME = 'throwableWeapon'


    def __init__(self):
        self.DAO = ItemDAO()


    def get_object(self, root) -> object:
        data = {}
        langs = self.get_langs(root)
        for lang in langs:
            name = self.get_value(root, 'name', lang)
            desc = self.get_value(root, 'description', lang)
            pric = self.get_value(root, 'price', None, True)
            weig = self.get_value(root, 'weight', None, True)
            init = self.get_value(root, 'initiative', None, True)
            stre = self.get_value(root, 'strength', None, True)
            ramp = self.get_value(root, 'rampancy', None, True)
            ranL = self.get_value(root, 'rangeLow', None, True)
            ranM = self.get_value(root, 'rangeMedium', None, True)
            ranH = self.get_value(root, 'rangeHigh', None, True)
            defe = self.get_value(root, 'defence', None, True)
            wepW_name = self.get_value(root, 'weaponWeight', None, False)

            wepW = WeaponWeight.by_name(WeaponWeight, wepW_name)

            obj = ThrowableWeapon(None, lang, name, desc, None, weig, pric, init, stre, ramp, ranL,
                                  ranM, ranH, defe, wepW)
            data[lang] = obj

        return data


    def remap_names(self, name: str) -> str:
        return name
