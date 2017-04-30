from datetime import datetime, date
import os
import shutil
from lxml import etree

from structure.map.Map import Map


class XElement:
    """
    Element for store and import single attribute in XML
    """


    def __init__(self, name: str, enum=None, valueType=None):
        self.__value = None
        self.__name = name
        self.__xmlElement = None
        self.__enum = enum
        self.__valueType = valueType


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


    @property
    def enum(self):
        return self.__enum


    def set_attributes(self, objects: dict, name: str, attr):
        """
        Set attribute in object
        """
        for obj in objects.values():
            if self.__enum:
                setattr(obj, name, self.__enum.by_name(self.__enum, attr.text))
            else:
                try:
                    value = int(attr.text)
                except:
                    value = attr.text

                setattr(obj, name, value)
        return objects


    def __create_xml_element(self):
        """
        Create xml element        
        """
        self.__xmlElement = etree.Element(self.__name)
        if self.__valueType == 'DATETIME':
            self.__xmlElement.text = str(self.__value.strftime('%d/%m/%Y %H:%M:%S'))
        elif isinstance(self.__value, date):
            self.__xmlElement.text = str(self.__value.strftime('%d/%m/%Y'))
        elif type(self.__value) == bool:
            self.__xmlElement.text = str(self.__value).lower()
        else:
            if self.__value is None:
                self.__value = 0
            self.__xmlElement.text = str(self.__value)


class XAttribElement:
    """
    Element for store value with attribute, usually lang
    """


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
    """
    Element for include another XML object in XML object
    """


    def __init__(self, name: str, instance: object, single: bool = False, rename: str = None):
        self.__name = name
        self.__instance = instance
        self.__single = single
        self.__rename = rename


    @property
    def name(self):
        return self.__name


    @property
    def instance(self):
        return self.__instance


    @property
    def single(self):
        return self.__single


    @property
    def rename(self):
        return self.__rename


    @property
    def name(self):
        return self.__name


    def set_attributes(self, objects: dict, name: str, attr):
        attrList = []
        if self.single:
            o = self.__instance().import_xml(attr)
            for obj in objects.values():
                setattr(obj, name, o.popitem()[1])
        else:
            for a in attr:
                o = self.__instance().import_xml(a)
                attrList.append(o['cs'])  # TODO: default lang
            for obj in objects.values():
                setattr(obj, name, attrList)
        return objects


class XMLTemplate:
    ROOT_NAME = None
    OBJECT_TYPE = None


    def create_xml(self, objects, rename=None, path: str = None):
        """
        Create xml tree for current objects
        :param objects: list of objects, or single object
        :param rename: name if you want rename tag
        :param path: path for map tag
        :return: lxml root with objects
        """
        if not self.ROOT_NAME:
            raise NotImplementedError('ROOT_NAME not defined')

        if type(objects) not in (list, tuple):
            objects = [objects]

        if rename:
            root = etree.Element(rename)
        else:
            root = etree.Element(self.ROOT_NAME)

        if self.ROOT_NAME is 'map':
            self.create_image(objects[0], path)

        remapObjects = []
        for obj in objects:
            remapObjects.append(self.__attribute_name_remap(obj))
        for key, instance in self.__dict__.items():
            if isinstance(instance, XElement):
                if key in remapObjects[0].keys():  # and remapObjects[0][key] is not None:
                    if not remapObjects[0][key] and instance.enum is not None:
                        continue
                    else:
                        instance.value = remapObjects[0][key]
                        root.append(instance.xmlElement)
            elif isinstance(instance, XAttribElement):
                for lang in remapObjects:
                    if key in lang:  # and lang[key] is not None
                        if lang[key] is None:
                            text = ''
                        else:
                            text = lang[key]
                        instance.value = (text, lang[instance.attributeName])
                        root.append(instance.xmlElement)
            elif isinstance(instance, XInstance):
                if remapObjects[0][key] is None:
                    continue
                instanceRoot = None
                # Control duplicity of tags in root, if exist use old root
                for tag in root.getchildren():
                    if instance.name == tag.tag:
                        instanceRoot = tag

                # if not exist, create new one
                if instanceRoot is None:
                    instanceRoot = etree.Element(instance.name)

                add = False
                if type(remapObjects[0][key]) is list:
                    for one in remapObjects[0][key]:
                        child = instance.instance().create_xml(one, instance.rename, path)
                        instanceRoot.append(child)
                        add = True
                    if add:
                        root.append(instanceRoot)
                else:
                    child = instance.instance().create_xml(remapObjects[0][key], instance.rename, path)
                    root.append(child)

        return root


    def import_xml(self, root) -> list:
        """
        Import xml and create objects from given root
        :param root: root of lxml tree
        :return: list of objects
        """
        if not self.OBJECT_TYPE:
            raise NotImplementedError('OBJECT_TYPE not defined')
        if not self.ROOT_NAME:
            raise NotImplementedError('ROOT_NAME not defined')

        # if root.tag != self.ROOT_NAME:
        #     raise ValueError('Root tag name is not ' + self.ROOT_NAME)

        langs = self.__get_langs(root)

        objects = {}
        for lang in langs:
            obj = self.OBJECT_TYPE.instance()(None, lang)
            objects[lang] = obj

        if len(objects) == 0:
            objects['cs'] = self.OBJECT_TYPE.instance()(None, 'cs')  # TODO: default lang

        # Remap instances for easy finding
        xInstances = {}
        for key, instance in self.__dict__.items():
            if instance.name in xInstances:
                if type(xInstances[instance.name]) is not dict:
                    old = xInstances[instance.name]
                    xInstances[instance.name] = {}
                    xInstances[instance.name][old[0]] = old[1]
                xInstances[instance.name][key] = instance

            else:
                xInstances[instance.name] = (key, instance)

        for attr in root:
            if attr.tag in xInstances:
                if attr.tag == 'id':  # TODO: remap id
                    continue

                if type(xInstances[attr.tag]) is dict:
                    groups = self.__remap_xml_group(attr, xInstances[attr.tag])
                    for name, root in groups.items():
                        objects = xInstances[attr.tag][name].set_attributes(objects, name, root)
                else:
                    objects = xInstances[attr.tag][1].set_attributes(objects,
                                                                     xInstances[attr.tag][0],
                                                                     attr)

        return objects


    def create_image(self, map: Map, path: str):
        """
        Create image, if exporting map
        :param map: Map object 
        :param path: path to source map        
        """
        directory = os.path.dirname(path)

        resourcesDir = os.path.join(directory, 'resources')
        if not os.path.exists(resourcesDir):
            os.mkdir(resourcesDir)

        source = os.path.join('resources', 'maps', 'exportedMap-{}.png'.format(map.id))
        destination = os.path.join(resourcesDir, map.XMLMap)
        shutil.copy2(source, destination)


    def __remap_xml_group(self, rootTag, instances):
        groups = {}
        for name, instance in instances.items():
            groups[instance.instance.ROOT_NAME] = (name, [])

        for tag in list(rootTag):
            groups[tag.tag][1].append(tag)

        newTrees = {}
        for group in groups.values():
            root = etree.Element(group[0])
            for child in group[1]:
                root.append(child)
            newTrees[group[0]] = root

        return newTrees


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
