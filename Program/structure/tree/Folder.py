from structure.enums.NodeType import NodeType
from structure.tree.Node import Node


class Folder(Node):
    def __init__(self, id: int = None, name: str = None, parent_id: int = None):
        super().__init__(id, name, parent_id)

        self.__children = []


    @property
    def nodeType(self):
        return NodeType.FOLDER

    @property
    def children(self):
        return self.__children


    @children.setter
    def children(self, value):
        self.__children = value


    def add_child(self, child):
        self.__children.append(child)
