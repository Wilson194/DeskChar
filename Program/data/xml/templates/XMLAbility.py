from data.DAO.AbilityDAO import AbilityDAO
from data.DAO.SpellDAO import SpellDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.abilities.Ability import Ability
from structure.enums.Classes import Classes
from lxml import etree

from structure.enums.Races import Races


class XMLAbility(XMLTemplate):
    ROOT_NAME = 'ability'


    def __init__(self):
        self.DAO = AbilityDAO()


    def get_object(self, root) -> object:
        data = {}
        langs = self.get_langs(root)
        expr = "./{}[@lang='{}']"
        for lang in langs:
            name = self.get_value(root, 'name', lang)
            desc = self.get_value(root, 'description', lang)
            chan = self.get_value(root, 'chance', lang)
            clas = self.get_value(root, 'class', None, False)
            race = self.get_value(root, 'race', None, False)

            clas_num = Classes.by_name(Classes, clas)
            race_num = Races.by_name(Races, race)

            obj = Ability(None, lang, name, desc, chan, race_num, clas_num)
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
            elif key == 'drd_race':
                ele = etree.SubElement(root, self.remap_names(key))
                ele.text = Races(value).xml_name()
            else:
                ele = etree.SubElement(root, self.remap_names(key))
                ele.text = str(value)

        return root


    def remap_names(self, name: str) -> str:
        return name
