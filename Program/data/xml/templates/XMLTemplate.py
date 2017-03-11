from abc import ABC, abstractmethod


class XMLTemplate(ABC):
    @abstractmethod
    def get_object(self, root) -> object:
        pass


    @abstractmethod
    def create_xml(self, object_id: int):
        pass


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
