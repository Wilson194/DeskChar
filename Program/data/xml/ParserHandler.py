from lxml import etree

from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType
import os


class ParserHandler:
    def create_xml(self, data: list, path: str = None):
        root = etree.Element('templates')

        characters = []
        for node in data:
            if node.object.object_type == ObjectType.CHARACTER:
                scenario = node.object.DAO()().get(node.object.id, None, node.id, node.object.object_type)
                root = scenario.XmlClass()().create_xml(scenario)

            elif node.object.object_type == ObjectType.SCENARIO:
                scenario = node.object.DAO()().get(node.object.id, None, node.id, node.object.object_type)
                root = scenario.XmlClass()().create_xml(scenario)
            else:
                objs = node.object.DAO()().get_list(node.object.id, node.id, node.object.object_type)
                child = objs[0].XmlClass()().create_xml(objs)
                root.append(child)

        pathParts = path.split(os.sep)
        fileName = pathParts[-1]

        fileExtension = fileName.split('.')[-1]

        if fileExtension != 'xml':
            fileName += '.xml'

        path = ''.join(pathParts[:-2]) + fileName

        with open(path, 'w', encoding='UTF-8') as out:
            out.write(etree.tostring(root, pretty_print=True, encoding='UTF-8').decode('UTF-8'))

        for num, char in enumerate(characters):
            # path = ''.join(pathParts[:-2]) + ''.join(fileName.split('.')[:-1]) + str(num) + '.' + \
            #        fileName.split('.')[-1]
            with open(path, 'w', encoding='UTF-8') as out:
                out.write(etree.tostring(char, pretty_print=True, encoding='UTF-8').decode('UTF-8'))


    def import_xml(self, file_path):
        utf8_parser = etree.XMLParser(encoding='utf-8')
        root = etree.parse(file_path, utf8_parser).getroot()
        objects = []

        if root.tag == 'character':
            obj = ObjectType.CHARACTER.instance().XmlClass()().import_xml(root)
            objects.append(obj)
        elif root.tag == 'scenario':
            obj = ObjectType.SCENARIO.instance().XmlClass()().import_xml(root)
            objects.append(obj)
        else:
            for child in root:
                obj_type = ObjectType.by_name(ObjectType, str(child.tag))
                if obj_type:
                    obj = ObjectType.by_name(ObjectType,
                                             str(child.tag)).instance().XmlClass()().import_xml(
                        child)
                else:
                    obj = Items.by_name(Items, str(child.tag)).instance().XmlClass()().import_xml(
                        child)
                objects.append(obj)

        return objects
