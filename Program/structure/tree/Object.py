from tree.Node import Node


class Object(Node):
    def __init__(self, id: int = None, name: str = None, parent_id: int = None, object=None):
        super().__init__(id, name, parent_id)
        self.__object = object


    @property
    def object(self):
        return self.__object


    @object.setter
    def object(self, value):
        self.__object = value
