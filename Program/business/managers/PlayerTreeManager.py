from data.database.ObjectDatabase import ObjectDatabase
from data.xml.ParserHandler import ParserHandler
from structure.tree.Object import Object
from structure.tree.Folder import Folder
from structure.enums.NodeType import NodeType
from structure.tree.Node import Node
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from structure.enums.ObjectType import ObjectType
from data.DAO.SpellDAO import SpellDAO
from structure.spells.Spell import Spell


class PlayerTreeManager:
    """
    Tree manager for tree widget
    """


    def __init__(self):
        self.treeDAO = PlayerTreeDAO()


    def get_tree(self, object_type: ObjectType) -> list:
        """
        Return list of root in tree, root has children ( recursive)
        :return: list of root
        """
        roots = self.treeDAO.get_root_nodes(object_type)

        for root in roots:
            self.__create_tree(root, object_type)

        return roots


    def __create_tree(self, node: Node, type: ObjectType):
        """
        Recursive function for create tree with children
        :param node: Current node
        :param type: parent of node
        """
        children = self.treeDAO.get_children_nodes(type, node.id)
        for child in children:
            self.__create_tree(child, type)
        node.children = children


    def create_node(self, node_type: NodeType, name: str, parent_id: int = None,
                    object_type: ObjectType = None):
        """
        Create new node
        :param node_type: Node type
        :param name:  name of node
        :param parent_id: parent id
        :param object_type: Type of object
        :return: New node object
        """
        if node_type.value is NodeType.FOLDER.value:
            node = Folder(None, name, parent_id)
        else:
            obj = self.create_empty_object(object_type)
            node = Object(None, name, parent_id, obj)
        id = self.treeDAO.insert_node(node, object_type)
        node.id = id
        return node


    def delete_node(self, id):
        """
        Delete node
        :param id: id of node
        """
        self.treeDAO.delete_node(id)


    def update_node_parent(self, node_id, parent_id):
        """
        Update parent of node, check if parent is Folder
        :param node_id: id of node
        :param parent_id: parent id
        :return:
        """
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
        """
        Create empty object
        :param object_type: obkect type
        :return: Object if created, None otherwise
        """
        if object_type.value is ObjectType.SPELL.value:
            obj = Spell()
            spell_id = SpellDAO().create_spell(obj)
            obj.id = spell_id
        else:
            obj = None
        return obj


    def get_object(self, node_id):
        """
        Get node by id
        :param node_id: id of node
        :return: Node if exist, None otherwise
        """
        node = self.treeDAO.get_node(node_id)
        return node.object


    def export_to_xml(self, selected, path):
        exporting = []
        for id in selected:
            node = self.treeDAO.get_node(id)
            exporting.append((ObjectType.SPELL, node.object.id))  # TODO

        ParserHandler().create_xml(exporting, path)


    def import_from_xml(self, file_path, type):
        objects = ParserHandler().import_xml(file_path)
        for object in objects:
            default = object.pop('cs')  # TODO: default lang
            default_id = ObjectDatabase('test.db').insert_object(default)
            default.id = default_id
            for lang in object.values():
                lang.id = default_id
                ObjectDatabase('test.db').update_object(lang)

            node = Object(None, default.name, None, default)
            self.treeDAO.insert_node(node, ObjectType.SPELL)
