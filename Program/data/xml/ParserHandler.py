from lxml import etree

from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType


class ParserHandler:
    def create_xml(self, data: list, path=None):
        root = etree.Element('templates')

        for type, id in data:
            child = type.instance().XmlClass()().create_xml(id)
            root.append(child)

        with open(path, 'w', encoding='UTF-8') as out:
            out.write(etree.tostring(root, pretty_print=True, encoding='UTF-8').decode('UTF-8'))


    def import_xml(self, file_path):
        utf8_parser = etree.XMLParser(encoding='utf-8')
        root = etree.parse(file_path, utf8_parser).getroot()
        objects = []

        for child in root:
            obj_type = ObjectType.by_name(ObjectType, str(child.tag))
            if obj_type:
                obj = ObjectType.by_name(ObjectType,
                                         str(child.tag)).instance().XmlClass()().get_object(child)
            else:
                obj = Items.by_name(Items, str(child.tag)).instance().XmlClass()().get_object(child)
            objects.append(obj)

        return objects
