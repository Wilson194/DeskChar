from structure.enums.NodeType import NodeType
from structure.tree.Node import Node


class Folder(Node):
    def __init__(self, id: int = None, name: str = None, parent_id: int = None):
        super().__init__(id, name, parent_id)


    @property
    def nodeType(self):
        return NodeType.FOLDER


    def add_child(self, child):
        self.__children.append(child)

    def __repr__(self):
        return '<structure.tree.Folder -> name: {}, parentId: {}'.format(self.name, self.parent_id)
