from data.DAO.ItemDAO import ItemDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.enums.Handling import Handling
from structure.enums.WeaponWeight import WeaponWeight
from structure.items.Container import Container
from structure.items.MeleeWeapon import MeleeWeapon


class XMLMeleeWeapon(XMLTemplate):
    ROOT_NAME = 'meleeWeapon'


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
            stre = self.get_value(root, 'strength', None, True)
            ramp = self.get_value(root, 'rampancy', None, True)
            defe = self.get_value(root, 'defence', None, True)
            leng = self.get_value(root, 'length', None, True)

            wepW_name = self.get_value(root, 'weaponWeight', None, False)
            hand_name = self.get_value(root, 'handling', None, False)

            wepW = WeaponWeight.by_name(WeaponWeight, wepW_name)
            hand = Handling.by_name(Handling, hand_name)

            obj = MeleeWeapon(None, lang, name, desc, None, weig, pric, stre, ramp, defe, leng,
                              wepW, hand)
            data[lang] = obj

        return data


    def remap_names(self, name: str) -> str:
        return name
