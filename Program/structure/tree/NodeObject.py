from structure.enums.NodeType import NodeType
from structure.enums.ObjectType import ObjectType
from structure.tree.Node import Node


class NodeObject(Node):
    def __init__(self, id: int = None, name: str = None, parent_id: int = None, object=None, context: ObjectType = None):
        super().__init__(id, name, parent_id)
        self.__object = object
        self.__context = context


    @property
    def nodeType(self):
        return NodeType.OBJECT


    @property
    def object(self):
        return self.__object


    @object.setter
    def object(self, value):
        self.__object = value


    @property
    def context(self):
        return self.__context


    @context.setter
    def context(self, value):
        self.__context = value


    def __repr__(self):
        return '<structure.tree.NodeObject -> {}(id: {}, parentId: {}, name: {}, context: {})'.format(
            self.object.object_type, self.object.id, self.parent_id, self.name, self.context)
