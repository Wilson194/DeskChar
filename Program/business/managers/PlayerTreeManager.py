from structure.tree.Object import Object
from structure.tree.Folder import Folder
from enums.NodeType import NodeType
from structure.tree.Node import Node
from PlayerTreeDAO import PlayerTreeDAO
from enums.ObjectType import ObjectType


class PlayerTreeManager:
    def __init__(self):
        self.treeDAO = PlayerTreeDAO()


    def get_spell_tree(self) -> list:
        roots = self.treeDAO.get_root_nodes(ObjectType.SPELL.value)

        for root in roots:
            self.__create_tree(root, ObjectType.SPELL.value)

        return roots


    def __create_tree(self, node: Node, type):
        children = self.treeDAO.get_children_nodes(type, node.id)
        for child in children:
            self.__create_tree(child, type)
        node.children = children


    def create_node(self, node_type, name, parent_id=None, object=None):
        print(node_type.value)
        if node_type.value is NodeType.FOLDER.value:
            node = Folder(None, name, parent_id)
        else:
            node = Object(None, name, parent_id, object)
        self.treeDAO.insert_node(node)


    def delete_node(self, id):
        self.treeDAO.delete_node(id)
