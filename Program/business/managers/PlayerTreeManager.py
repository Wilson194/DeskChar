from structure.tree.Object import Object
from structure.tree.Folder import Folder
from enums.NodeType import NodeType
from structure.tree.Node import Node
from PlayerTreeDAO import PlayerTreeDAO
from enums.ObjectType import ObjectType
from data.DAO.SpellDAO import SpellDAO
from structure.spells.Spell import Spell


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


    def create_node(self, node_type, name, parent_id=None, object_type=None):
        if node_type.value is NodeType.FOLDER.value:
            node = Folder(None, name, parent_id)
        else:
            obj = self.create_empty_object(object_type)
            node = Object(None, name, parent_id, obj)
        self.treeDAO.insert_node(node)


    def delete_node(self, id):
        self.treeDAO.delete_node(id)


    def update_node_parent(self, node_id, parent_id):
        node = self.treeDAO.get_node(node_id)
        if not parent_id:
            if node.parent_id != parent_id:
                node.parent_id = parent_id
                self.treeDAO.update_node(node)
        else:
            parent_node = self.treeDAO.get_node(parent_id)
            if node.parent_id != parent_id and isinstance(parent_node, Folder):
                node.parent_id = parent_id
                self.treeDAO.update_node(node)


    def create_empty_object(self, object_type: ObjectType) -> Object:
        if object_type.value is ObjectType.SPELL.value:
            obj = Spell()
            spell_id = SpellDAO().create_spell(obj)
            obj.id = spell_id
        else:
            obj = None
        return obj
