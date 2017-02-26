from abc import ABC, abstractmethod


class XMLTemplate(ABC):
    @abstractmethod
    def get_object(self, root) -> object:
        pass

    @abstractmethod
    def create_xml(self, object_id : int):
        pass
