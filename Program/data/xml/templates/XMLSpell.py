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
            name_x = root.xpath(expr.format('name', lang))
            name = name_x[0].text if len(name_x) > 0 else ""
            desc_x = root.xpath(expr.format('description', lang))
            desc = desc_x[0].text if len(desc_x) > 0 else ""
            mani_x = root.xpath(expr.format('manaInitial', lang))
            mani = mani_x[0].text if len(mani_x) > 0 else ""
            manc_x = root.xpath(expr.format('manaContinual', lang))
            manc = manc_x[0].text if len(manc_x) > 0 else ""
            rang_x = root.xpath(expr.format('range', lang))
            rang = rang_x[0].text if len(rang_x) > 0 else ""
            scop_x = root.xpath(expr.format('scope', lang))
            scop = scop_x[0].text if len(scop_x) > 0 else ""
            cati_x = root.xpath(expr.format('castTime', lang))
            cati = cati_x[0].text if len(cati_x) > 0 else ""
            dura_x = root.xpath(expr.format('duration', lang))
            dura = dura_x[0].text if len(dura_x) > 0 else ""
            clas_x = root.xpath(expr.format('class', lang))
            clas = clas_x[0].text if len(clas_x) > 0 else ""

            obj = Spell(None, lang, name, desc, mani, manc,
                        rang, scop, cati, dura, clas)
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
