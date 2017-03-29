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


    def search_tree_nodes(self, object_type: ObjectType, text: str) -> list:
        roots = self.treeDAO.get_nodes_search(object_type, text)

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


    def create_node_link(self, nodeType: NodeType, name: str, parentId: int,
                         parentType: ObjectType = None, targetObject: object = None) -> Node:
        """
        Create node in tree, that link to some object, that already exist        
        :param nodeType: Type of node (Folder, Object)
        :param name: name of node
        :param parentId: id of parent object
        :param parentType: 
        :param targetObject: target object
        :return: node
        """
        if nodeType is NodeType.FOLDER:
            node = Folder(None, name, parentId)
        else:
            node = Object(None, name, parentId, targetObject)

        id = self.treeDAO.insert_node(node, parentType)
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


    def update_node_parent(self, nodeId: int, parentId: int, context: ObjectType):
        """
        Update parent of node, check if parent is Folder
        :param nodeId: id of node
        :param parentId: parent id
        :return:
        """
        node = self.treeDAO.get_node(nodeId)
        parentNode = self.treeDAO.get_node(parentId)
        if node.parent_id:
            oldParentNode = self.treeDAO.get_node(parentId)
        else:
            oldParentNode = None

        if node.parent_id != parentId and self.available_parent(node, parentNode, context):
            self.update_links(node, parentNode, oldParentNode)
            node.parent_id = parentId
            self.treeDAO.update_node(node)


    def update_links(self, node, newParentNode, oldParentNode):
        while oldParentNode:
            if isinstance(oldParentNode, Folder):
                if oldParentNode.parent_id is None:
                    oldParentNode = None
                else:
                    oldParentNode = self.treeDAO.get_node(oldParentNode.parent_id)
            else:
                break

        while newParentNode:
            if isinstance(newParentNode, Folder):
                if newParentNode.parent_id is None:
                    newParentNode = None
                else:
                    newParentNode = self.treeDAO.get_node(newParentNode.parent_id)
            else:
                break

        children = self.get_all_children(node)

        for child in children:
            if oldParentNode:
                oldParentNode.object.DAO()().delete_link(oldParentNode.object, child.object)
            if newParentNode:
                newParentNode.object.DAO()().create_link(newParentNode.object, child.object)


    def get_all_children(self, node, children=None):
        if children is None:
            children = []

        if isinstance(node, Folder):
            for child in node.children:
                if isinstance(child, Folder):
                    children = self.get_all_children(child, children)
                else:
                    children.append(child)
        else:
            children.append(node)

        return children


    def available_parent(self, node, parent_node, context: ObjectType) -> bool:
        """
        Validate if can change parent_id for node
        Go recursive to root, if find object, just chceck if can be
        If there is no object, just add it
        :param node: Node
        :param parent_node: Parent node
        :return: True if can be there, False otherwise
        """
        while parent_node is not None:
            if isinstance(parent_node, Folder):
                if parent_node.parent_id is None:
                    parent_node = None
                else:
                    parent_node = self.treeDAO.get_node(parent_node.parent_id)
            else:
                if isinstance(node, Folder):
                    if NodeType.FOLDER in parent_node.object.treeChildren:
                        return True
                    else:
                        return False
                else:
                    if node.object.object_type in parent_node.object.treeChildren:
                        return True
                    else:
                        return False

        if isinstance(node, Folder):  # TODO
            return True
        else:
            if node.object.object_type is context:
                return True
            else:
                return False


    def have_tree_children(self, node) -> bool:
        while node is not None:
            if isinstance(node, Folder):
                if node.parent_id is None:
                    node = None
                else:
                    node = self.treeDAO.get_node(node.parent_id)
            else:
                return len(node.object.treeChildren) > 0

        return False


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
        Get object from node
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
