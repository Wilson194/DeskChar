from lxml import etree


class Parser:
    def __init__(self, root_element):
        self.root_element = root_element


    def parse(self) -> dict:
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


    def create(self, data: dict):
        for key, value in data.items():
            if type(value) == dict:
                for lang, text in value.items():
                    element = etree.Element(key, {'lang': lang})
                    element.text = text
                    self.root_element.append(element)
            else:
                element = etree.Element(key)
                element.text = value
                self.root_element.append(element)
        return self.root_element
