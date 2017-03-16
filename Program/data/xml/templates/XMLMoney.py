from data.DAO.ItemDAO import ItemDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.items.Container import Container
from structure.items.Item import Item
from structure.items.Money import Money


class XMLMoney(XMLTemplate):
    ROOT_NAME = 'money'


    def __init__(self):
        self.DAO = ItemDAO()


    def get_object(self, root) -> object:
        data = {}
        langs = self.get_langs(root)
        for lang in langs:
            name = self.get_value(root, 'name', lang)
            desc = self.get_value(root, 'description', lang)
            copp = self.get_value(root, 'copper', None, True)
            silv = self.get_value(root, 'silver', None, True)
            gold = self.get_value(root, 'gold', None, True)

            obj = Money(None, lang, name, desc, None, copp, silv, gold)
            data[lang] = obj

        return data


    def remap_names(self, name: str) -> str:
        return name
