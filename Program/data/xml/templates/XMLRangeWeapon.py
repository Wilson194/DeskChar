from data.DAO.ItemDAO import ItemDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.items.RangeWeapon import RangeWeapon


class XMLRangeWeapon(XMLTemplate):
    ROOT_NAME = 'rangedWeapon'


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

            obj = RangeWeapon(None, lang, name, desc, None, weig, pric, init, stre, ramp, ranL,
                              ranM, ranH)
            data[lang] = obj

        return data


    def remap_names(self, name: str) -> str:
        return name
