from structure.enums.NodeType import NodeType
from structure.tree.Node import Node


class NodeObject(Node):
    def __init__(self, id: int = None, name: str = None, parent_id: int = None, object=None):
        super().__init__(id, name, parent_id)
        self.__object = object

    @property
    def nodeType(self):
        return NodeType.OBJECT

    @property
    def object(self):
        return self.__object


    @object.setter
    def object(self, value):
        self.__object = value
