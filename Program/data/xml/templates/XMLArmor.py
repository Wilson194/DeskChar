from data.DAO.ItemDAO import ItemDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.items.Armor import Armor


class XMLArmor(XMLTemplate):
    ROOT_NAME = 'armor'


    def __init__(self):
        self.DAO = ItemDAO()


    def get_object(self, root) -> object:
        data = {}
        langs = self.get_langs(root)
        for lang in langs:
            name = self.get_value(root, 'name', lang)
            desc = self.get_value(root, 'description', lang)
            pric = self.get_value(root, 'price', None, True)
            qual = self.get_value(root, 'quality', None, True)
            weiA = self.get_value(root, 'weightA', None, True)
            weiB = self.get_value(root, 'weightB', None, True)
            weiC = self.get_value(root, 'weightC', None, True)
            size = self.get_value(root, 'size', None, True)

            obj = Armor(None, lang, name, desc, None, pric, qual, weiA, weiB, weiC, size)
            data[lang] = obj

        return data


    def remap_names(self, name: str) -> str:
        return name
