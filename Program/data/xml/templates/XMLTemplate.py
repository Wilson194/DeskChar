from lxml import etree


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
                setattr(obj, name, self.__enum.by_name(self.__enum, attr.text))
            else:
                # lang = attr.get('lang')
                # if lang:
                #     value = attr.text
                # else:
                #     value = int(attr.text)
                try:
                    value = int(attr.text)
                except:
                    value = attr.text

                setattr(obj, name, value)
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
    def __init__(self, name: str, instance: object, single: bool = False, link: bool = False):
        self.__name = name
        self.__instance = instance
        self.__single = single


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
    def name(self):
        return self.__name


    def set_attributes(self, objects: dict, name: str, attr):
        attrList = []
        if self.single:
            o = self.__instance().import_xml(attr)
            for obj in objects.values():
                setattr(obj, name, o)
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
                instanceRoot = None
                # Control duplicity of tags in root, if exist use old root
                for tag in root.iter():
                    if instance.name == tag.tag:
                        instanceRoot = tag

                # if not exist, create new one
                if not instanceRoot:
                    instanceRoot = etree.Element(instance.name)

                add = False
                if type(remapObjects[0][key]) is list:
                    for one in remapObjects[0][key]:
                        child = instance.instance().create_xml(one)
                        instanceRoot.append(child)
                        add = True
                    if add:
                        root.append(instanceRoot)
                else:
                    child = instance.instance().create_xml(remapObjects[0][key])
                    root.append(child)

        return root


    def import_xml(self, root):
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
                # if type(xInstances[instance.name]) is not list:
                #     xInstances[instance.name] = [xInstances[instance.name]]
                # xInstances[instance.name].append((key, instance))
            else:
                xInstances[instance.name] = (key, instance)

        for attr in root:
            if attr.tag in xInstances:
                if attr.tag == 'id':  # TODO: remap id
                    continue
                # if not attr:
                #     continue

                if type(xInstances[attr.tag]) is dict:
                    groups = self.__remap_xml_group(attr, xInstances[attr.tag])
                    for name, root in groups.items():
                        objects = xInstances[attr.tag][name].set_attributes(objects, name, root)
                else:
                    objects = xInstances[attr.tag][1].set_attributes(objects,
                                                                     xInstances[attr.tag][0],
                                                                     attr)

        return objects


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
