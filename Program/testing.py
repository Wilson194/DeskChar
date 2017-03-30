from lxml import etree

from structure.effects.Effect import Effect
from structure.effects.Modifier import Modifier
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.ObjectType import ObjectType


class XElement:
    def __init__(self, name: str, enum=None):
        self.__value = None
        self.__name = name
        self.__xmlElement = None
        self.__enum = enum


    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, value):
        self.__value = value
        self.__create_xml_element()


    @property
    def xmlElement(self):
        return self.__xmlElement


    @property
    def name(self):
        return self.__name


    def set_attributes(self, objects: dict, name: str, attr):
        for obj in objects.values():
            if self.__enum:
                setattr(obj, name, self.__enum.by_name(self.__enum,attr.text))
            else:
                setattr(obj, name, attr.text)
        return objects


    def __create_xml_element(self):
        self.__xmlElement = etree.Element(self.__name)
        self.__xmlElement.text = str(self.__value)


class XAttribElement:
    def __init__(self, name: str, attribute: str):
        self.__name = name
        self.__attributeName = attribute
        self.__value = (None, None)
        self.__xmlElement = None


    @property
    def attributeName(self):
        return self.__attributeName


    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, value):
        self.__value = value
        self.__create_xml_element()


    @property
    def name(self):
        return self.__name


    def __create_xml_element(self):
        attributes = {self.__attributeName: self.__value[1]}
        self.__xmlElement = etree.Element(self.__name, **attributes)
        self.__xmlElement.text = str(self.__value[0])


    @property
    def xmlElement(self):
        return self.__xmlElement


    def set_attributes(self, objects: dict, name: str, attr):
        obj = objects[attr.attrib[self.__attributeName]]
        setattr(obj, name, attr.text)
        return objects


class XInstance:
    def __init__(self, name: str, instance: object):
        self.__name = name
        self.__instance = instance


    @property
    def name(self):
        return self.__name


    @property
    def instance(self):
        return self.__instance


    @property
    def name(self):
        return self.__name


    def set_attributes(self, objects: dict, name: str, attr):
        attrList = []
        for a in attr:
            o = self.__instance().import_xml(a)
            attrList.append(o['cs'])  # TODO: default lang
        for obj in objects.values():
            setattr(obj, name, attrList)
        return objects


class XMLTemplate:
    ROOT_NAME = None
    OBJECT_TYPE = None


    def create_xml(self, objects):

        if not self.ROOT_NAME:
            raise NotImplementedError('ROOT_NAME not defined')

        if type(objects) not in (list, tuple):
            objects = [objects]

        root = etree.Element(self.ROOT_NAME)

        remapObjects = []
        for obj in objects:
            remapObjects.append(self.__attribute_name_remap(obj))

        for key, instance in self.__dict__.items():
            if isinstance(instance, XElement):
                if key in remapObjects[0].keys() and remapObjects[0][key] is not None:
                    instance.value = remapObjects[0][key]
                    root.append(instance.xmlElement)
            elif isinstance(instance, XAttribElement):
                for lang in remapObjects:
                    if key in lang and lang[key] is not None:
                        instance.value = (lang[key], lang[instance.attributeName])
                        root.append(instance.xmlElement)
            elif isinstance(instance, XInstance):
                instanceRoot = etree.Element(instance.name)
                for one in remapObjects[0][key]:
                    child = instance.instance().create_xml(one)
                    instanceRoot.append(child)
                root.append(instanceRoot)

        return root


    def import_xml(self, root):
        if not self.OBJECT_TYPE:
            raise NotImplementedError('OBJECT_TYPE not defined')
        if not self.ROOT_NAME:
            raise NotImplementedError('ROOT_NAME not defined')

        if root.tag != self.ROOT_NAME:
            raise ValueError('Root tag name is not ' + self.ROOT_NAME)

        langs = self.__get_langs(root)

        objects = {}
        for lang in langs:
            obj = self.OBJECT_TYPE.instance()(None, lang)
            objects[lang] = obj

        if len(objects) == 0:
            objects['cs'] = self.OBJECT_TYPE.instance()(None, 'cs')  # TODO: default lang

        xInstances = {}
        for key, instance in self.__dict__.items():
            xInstances[instance.name] = (key, instance)

        for attr in root:
            objects = xInstances[attr.tag][1].set_attributes(objects, xInstances[attr.tag][0], attr)

        return objects


    def __attribute_name_remap(self, obj):
        newAttrs = {}
        for key, value in obj.__dict__.items():
            for c in obj.__name__():
                key = key.replace('_' + c + '__', '')
            newAttrs[key] = value
        return newAttrs


    def __get_langs(self, root) -> set:
        langs = set()
        for node in root:
            if 'lang' in node.attrib.keys():
                langs.add(node.attrib['lang'])
        return langs


class XMLModifier(XMLTemplate):
    ROOT_NAME = 'modifier'
    OBJECT_TYPE = ObjectType.MODIFIER


    def __init__(self):
        self.id = XElement('id')
        self.valueType = XElement('valueType', ModifierValueTypes)
        self.value = XElement('value')
        self.targetType = XElement('targetType')
        self.valueTargetAttribute = XElement('valueTargetAttribute')


class XMLEffect(XMLTemplate):
    ROOT_NAME = 'effect'
    OBJECT_TYPE = ObjectType.EFFECT


    def __init__(self):
        self.id = XElement('id')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')
        self.targetType = XElement('targetType')
        self.modifiers = XInstance('modifiers', XMLModifier)


a = XMLModifier()
b = [Modifier(2, None, None, None, ModifierValueTypes.TO_TOTAL, 25, CharacterAttributes.STRENGTH,
              ModifierTargetTypes.CHARACTER),
     Modifier(2, None, None, None, ModifierValueTypes.TO_TOTAL, 25, CharacterAttributes.STRENGTH,
              ModifierTargetTypes.CHARACTER)]

c = XMLEffect()
e = Effect(3, 'cs', 'Lektvar sily', 'Mocny lektvar', None, ModifierTargetTypes.CHARACTER)
f = Effect(3, 'en', 'lectvaren', 'Powerfull', None, ModifierTargetTypes.CHARACTER)
e.modifiers = b
d = [e, f]

path = 'text.xml'

with open(path, 'w', encoding='UTF-8') as out:
    out.write(etree.tostring(c.create_xml(d), pretty_print=True, encoding='UTF-8').decode('UTF-8'))

utf8_parser = etree.XMLParser(encoding='utf-8')
root = etree.parse(path, utf8_parser).getroot()

objs = c.import_xml(root)
print(type(objs['en'].modifiers[0].valueType))
