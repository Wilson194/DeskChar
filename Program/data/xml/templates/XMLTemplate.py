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
