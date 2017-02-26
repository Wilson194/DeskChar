from lxml import etree

from structure.enums.ObjectType import ObjectType
from data.xml.templates.XMLSpell import XMLSpell


class ParserHandler:
    def create_xml(self, data: list, path=None):
        root = etree.Element('templates')

        for type, id in data:
            if type is ObjectType.SPELL:
                child = XMLSpell().create_xml(id)
                root.append(child)

        with open(path, 'w', encoding='UTF-8') as out:
            out.write(etree.tostring(root, pretty_print=True, encoding='UTF-8').decode('UTF-8'))
