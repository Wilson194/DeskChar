from business.managers.LangManager import LangManager
from data.DAO.EffectDAO import EffectDAO
from data.DAO.ItemDAO import ItemDAO
from data.DAO.ModifierDAO import ModifierDAO
from data.database.ObjectDatabase import ObjectDatabase
from data.html.HtmlHandler import HtmlHandler
from data.xml.ParserHandler import ParserHandler
from structure.tree.NodeObject import NodeObject
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

        for i in range(len(roots)):
            root = roots[i]
            new = self.__create_tree(root, object_type)
            roots[i] = new

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

        if node.id == None:
            node.id = -1
        children = self.treeDAO.get_children_nodes(type, node.id)

        if isinstance(node, NodeObject):
            if node.object.object_type is ObjectType.EFFECT:
                modifiers = ModifierDAO().get_link(node.object.id)
                for modifier in modifiers:
                    modifierNode = NodeObject(None, modifier.name, node.id, modifier)
                    children.append(modifierNode)

            if node.object.object_type is ObjectType.ITEM:
                effects = EffectDAO().get_link(node.object.id, node.object.object_type)
                for effect in effects:
                    effectNode = NodeObject(None, effect.name, node.id, effect)
                    children.append(effectNode)

        for i in range(len(children)):
            child = children[i]
            parentType = type if isinstance(child, Folder) else child.object.object_type
            new = self.__create_tree(child, parentType)
            children[i] = new

        node.children = children
        return node


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
            id = self.treeDAO.insert_node(node, object_type)  # TODO : remove object_type
            node.id = id
        else:
            id = target_object.DAO()().create(target_object())

            obj = target_object(id)
            node = self.treeDAO.get_node_by_object(obj)
            node.name = name
            self.treeDAO.update_node(node)  # TODO : remove object_type

        return node


    def create_node_link(self, nodeType: NodeType, name: str, parentId: int,
                         parentType: ObjectType = None, targetObject: object = None):
        """
        Create node in tree, that link to some object, that already exist        
        :param nodeType: Type of node (Folder, NodeObject)
        :param name: name of node
        :param parentId: id of parent object
        :param parentType: 
        :param targetObject: target object
        :return: node
        """
        if nodeType is NodeType.FOLDER:
            node = Folder(None, name, parentId)
            self.treeDAO.insert_node(node, parentType)
        else:
            if targetObject.object_type is ObjectType.MODIFIER:

                parentObjectId = self.treeDAO.get_node(parentId).object.id
                parentObject = parentType.instance().DAO()().get(parentObjectId)

                EffectDAO().create_link(parentObject, targetObject)

            elif targetObject.object_type is ObjectType.EFFECT and parentType is ObjectType.ITEM:
                parentObjectId = self.treeDAO.get_node(parentId).object.id
                parentObject = parentType.instance().DAO()().get(parentObjectId)

                ItemDAO().create_effect_link(parentObject, targetObject)
            else:
                node = NodeObject(None, name, parentId, targetObject)
                self.treeDAO.insert_node(node, parentType)


    def delete_node(self, node, targetObject):
        """
        Delete node
        :param id: id of node
        """
        if targetObject and targetObject.object_type is ObjectType.MODIFIER:
            parentObject = node.object
            EffectDAO().delete_link(parentObject, targetObject)
        else:
            self.treeDAO.delete_node(node.id)


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


    def update_node_parent(self, node: int, parentId: int, context: ObjectType):
        """
        Update parent of node, check if parent is Folder
        :param nodeId: id of node
        :param parentId: parent id
        :return:
        """
        parentNode = self.treeDAO.get_node(parentId)
        oldParentNode = self.treeDAO.get_node(node.parent_id)
        if node.parent_id != parentId and self.available_parent(node, parentNode, context):
            node.parent_id = parentId
            if isinstance(node, Folder):
                self.treeDAO.update_node(node)
            else:
                if node.object.object_type is ObjectType.MODIFIER:
                    EffectDAO().delete_link(oldParentNode.object, node.object)
                    EffectDAO().create_link(parentNode.object, node.object)
                else:
                    self.treeDAO.update_node(node)


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


    def create_empty_object(self, object_type: ObjectType) -> NodeObject:
        """
        Create empty object
        :param object_type: obkect type
        :return: NodeObject if created, None otherwise
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


    def export_to_html(self, selected: list, path: str):
        exporting = []
        for id in selected:
            node = self.treeDAO.get_node(id)
            exporting.append(node.object)

        HtmlHandler().create_html(exporting, path)


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


    def import_from_xml(self, file_path, parentType, parent=None, strict: bool = False):
        """
        Import templates from XML file
        :param file_path: path to XML file
        :param type:
        :param strict:
        :param parent: parent node id
        """
        objects = ParserHandler().import_xml(file_path)

        ObjectDatabase('test.db').set_many(True)

        for languages in objects:
            leader = languages.popitem()

            leaderCode = leader[0]
            leaderObejct = leader[1]

            if strict and leaderObejct.object_type != parentType:
                continue

            if not LangManager().lang_exists(leaderCode):
                LangManager().create_lang(leaderCode, leaderCode)

            leaderId = ObjectDatabase('test.db').insert_object(leaderObejct,
                                                               parentType.name.title(), parentType,
                                                               parent)
            leaderObejct.id = leaderId

            for lang in languages.values():
                if not LangManager().lang_exists(lang.lang):
                    LangManager().create_lang(lang.lang, lang.lang)

                lang.id = leaderId
                ObjectDatabase('test.db').update_object(lang, parentType.name.title())

        ObjectDatabase('test.db').insert_many_execute()
        ObjectDatabase('test.db').set_many(False)


    def create_tree_dependences(self, objects: list, parentId: int, parentType: object):
        for item in objects:
            node = NodeObject(None, item.name, parentId, item)
            nodeId = self.treeDAO.insert_node(node, parentType)

            for value in item.__dict__.values():
                if type(value) is list:
                    self.create_tree_dependences(value, nodeId, parentType)


    def tree_folder(self, node: Node) -> bool:
        while node.parent_id:
            parentNode = self.get_node(node.parent_id)
            if isinstance(parentNode, Folder):
                node = parentNode
            else:
                return False

        return True
