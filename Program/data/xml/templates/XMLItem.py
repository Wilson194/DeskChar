from data.DAO.ItemDAO import ItemDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.items.Container import Container
from structure.items.Item import Item


class XMLItem(XMLTemplate):
    ROOT_NAME = 'item'


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

            obj = Item(None, lang, name, desc, None, weig, pric)
            data[lang] = obj

        return data


    def remap_names(self, name: str) -> str:
        return name
