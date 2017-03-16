from business.managers.LangManager import LangManager
from data.database.ObjectDatabase import ObjectDatabase
from data.xml.ParserHandler import ParserHandler
from structure.tree.Object import Object
from structure.tree.Folder import Folder
from structure.enums.NodeType import NodeType
from structure.tree.Node import Node
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from structure.enums.ObjectType import ObjectType


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
                    object_type: ObjectType = None, target_object: object = None):
        """
        Create new node
        :param node_type: Node type
        :param name:  name of node
        :param parent_id: parent id
        :param object_type: Type of object
        :param target_object: instance of target object
        :return: New node object
        """
        if node_type.value is NodeType.FOLDER.value:
            node = Folder(None, name, parent_id)
        else:
            id = target_object.DAO()().create(target_object())
            obj = target_object(id)
            node = Object(None, name, parent_id, obj)
        id = self.treeDAO.insert_node(node, object_type)  # TODO : remove object_type
        node.id = id
        return node


    def delete_node(self, id):
        """
        Delete node
        :param id: id of node
        """
        self.treeDAO.delete_node(id)


    def get_node(self, id: int):
        """
        Get node by ID
        :param id: id of node
        :return: Node
        """
        return self.treeDAO.get_node(id)


    def update_node(self, node):
        """
        Update node in database
        :param node: Updated node
        """
        self.treeDAO.update_node(node)


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
        obj = object_type.instance()()
        obj.id = object_type.instance().DAO()().create(obj)

        return obj


    def get_object(self, node_id: int):
        """
        Get node by id
        :param node_id: id of node
        :return: Node if exist, None otherwise
        """
        node = self.treeDAO.get_node(node_id)
        return node.object


    def export_to_xml(self, selected: list, path: str):
        """
        Export selected templates to xml
        :param selected: list of selected node in tree
        :param path: path to file, where will be final file
        """
        exporting = []
        for id in selected:
            node = self.treeDAO.get_node(id)
            print(node.object.object_type)
            exporting.append(
                (node.object.object_type, node.object.id))

        ParserHandler().create_xml(exporting, path)


    def import_from_xml(self, file_path, type, parent=None, strict: bool = False):
        """
        Import templates from XML file
        :param file_path: path to XML file
        :param type:
        :param strict:
        :param parent: parent node id
        """
        objects = ParserHandler().import_xml(file_path)
        ObjectDatabase('test.db').set_many(True)

        if not LangManager().lang_exists('cs'):  # TODO : default lang
            LangManager().create_lang('Čeština', 'cs')

        for object in objects:
            if strict and object[list(object.keys())[0]].object_type != type:
                continue

            default = object.pop('cs')  # TODO: default lang
            default_id = ObjectDatabase('test.db').insert_object(default, type.name.title())
            default.id = default_id
            for lang in object.values():
                if not LangManager().lang_exists(lang.lang):  # TODO : default lang
                    LangManager().create_lang(lang.lang, lang.lang)
                lang.id = default_id
                ObjectDatabase('test.db').update_object(lang, type.name.title())

            node = Object(None, default.name, parent, default)
            self.treeDAO.insert_node(node, default.object_type)

        ObjectDatabase('test.db').insert_many_execute()
        ObjectDatabase('test.db').set_many(False)
