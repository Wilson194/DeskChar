from data.DAO.SpellDAO import SpellDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.enums.Classes import Classes
from lxml import etree


class XMLSpell(XMLTemplate):
    ROOT_NAME = 'spell'


    def __init__(self):
        self.DAO = SpellDAO()


    def get_object(self, root) -> object:
        data = {}
        for element in self.root_element:
            if 'lang' in element.attrib.keys():
                if element.tag in data:
                    data[element.tag][element.attrib['lang']] = element.text
                else:
                    data[element.tag] = {}
                    data[element.tag][element.attrib['lang']] = element.text
            else:
                data[element.tag] = element.text
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
