from abc import ABC, abstractmethod
from lxml import etree

from structure.enums.Classes import Classes
from structure.enums.Handling import Handling
from structure.enums.Races import Races
from structure.enums.WeaponWeight import WeaponWeight


class XMLTemplate(ABC):
    @abstractmethod
    def get_object(self, root) -> object:
        pass


    def create_xml(self, object_id: int):
        root = etree.Element(self.ROOT_NAME)

        data = self.DAO.get_all_data(object_id)

        for key, value in data.items():
            if value is None:
                continue

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

            elif key == 'handling':
                ele = etree.SubElement(root, self.remap_names(key))
                ele.text = Handling(value).xml_name()

            elif key == 'weaponWeight':
                ele = etree.SubElement(root, self.remap_names(key))
                ele.text = WeaponWeight(value).xml_name()
            else:
                ele = etree.SubElement(root, self.remap_names(key))
                ele.text = str(value)

        return root


    def get_langs(self, root) -> set:
        langs = set()
        for node in root:
            if 'lang' in node.attrib.keys():
                langs.add(node.attrib['lang'])
        return langs


    def get_value(self, root, name, lang=None, numeric=True):
        expr = "./{}[@lang='{}']"

        if lang is None:
            if numeric:
                value_x = root.xpath("./{}".format(name))
                return int(value_x[0].text) if len(value_x) > 0 else 0
            else:
                value_x = root.xpath("./{}".format(name))
                return value_x[0].text if len(value_x) > 0 else ""
        else:
            value_x = root.xpath(expr.format(name, lang))
            return value_x[0].text if len(value_x) > 0 else ""


    def remap_names(self, key):
        return key
