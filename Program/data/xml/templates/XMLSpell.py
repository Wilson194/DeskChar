from data.DAO.SpellDAO import SpellDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.enums.Classes import Classes
from lxml import etree

from structure.spells.Spell import Spell


class XMLSpell(XMLTemplate):
    ROOT_NAME = 'spell'


    def __init__(self):
        self.DAO = SpellDAO()


    def get_object(self, root) -> object:
        data = {}
        langs = self.get_langs(root)
        expr = "./{}[@lang='{}']"
        for lang in langs:
            name = self.get_value(root, 'name', lang)
            desc = self.get_value(root, 'description', lang)
            mani = self.get_value(root, 'manaInitial', lang)
            manc = self.get_value(root, 'manaContinual', lang)
            rang = self.get_value(root, 'range', lang)
            scop = self.get_value(root, 'scope', lang)
            cati = self.get_value(root, 'castTime')
            dura = self.get_value(root, 'duration', lang)
            clas = self.get_value(root, 'class', None, False)

            clas_num = Classes.by_name(Classes, clas)

            obj = Spell(None, lang, name, desc, mani, manc,
                        rang, scop, cati, dura, clas_num.value)
            data[lang] = obj

        return data


    def create_xml(self, object_id: int):
        root = etree.Element(self.ROOT_NAME)

        data = self.DAO.get_all_data(object_id)

        for key, value in data.items():
            if type(value) is dict:
                for lang, lang_value in value.items():
                    ele = etree.SubElement(root, self.remap_names(key), lang=lang)
                    ele.text = lang_value
            elif key == 'drd_class':
                ele = etree.SubElement(root, self.remap_names(key))
                ele.text = Classes(value).xml_name()
            else:
                ele = etree.SubElement(root, self.remap_names(key))
                ele.text = str(value)

        return root


    def remap_names(self, name: str) -> str:
        if name == 'mana_cost_initial':
            return 'manaInitial'
        if name == 'mana_cost_continual':
            return 'manaContinual'
        if name == 'drd_class':
            return 'class'
        if name == 'ID':
            return 'id'
        if name == 'cast_time':
            return 'castTime'
        return name
