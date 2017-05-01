from abc import ABC, abstractmethod
from structure.enums.NodeType import NodeType
from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object
from structure.tree.Node import Node
from structure.tree.NodeObject import NodeObject


class IPlayerTreeManager(ABC):
    """
    Tree manager for tree widget
    """


    @abstractmethod
    def get_tree(self, object_type: ObjectType) -> list:
        """
        Return list of root in tree, root has children ( recursive)
        :return: list of root
        """
        pass


    @abstractmethod
    def search_tree_nodes(self, object_type: ObjectType, text: str) -> list:
        """
        Search tree nodes by object type and text, its for finding
        :param object_type: object type (context)
        :param text: text that should be included
        :return: list of root
        """
        pass


    @abstractmethod
    def create_folder(self, name: str, contextType: ObjectType, parentId: int = None) -> Node:
        """
        Create new node        
        :param name:  name of node
        :param contextType: Context type
        :param parentId: Id of parent node        
        :return: New node folder object
        """
        pass


    @abstractmethod
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
        pass


    @abstractmethod
    def delete_node(self, node: Node, targetObject: Object):
        """
        Delete node
        :param node: Node that you want to delete
        :param targetObject: Target object, that will be deleted too
        """
        pass


    @abstractmethod
    def get_node(self, id: int):
        """
        Get node by ID
        :param id: id of node
        :return: Node
        """
        pass


    @abstractmethod
    def update_node(self, node: Node):
        """
        Update node in database
        :param node: Updated node
        """
        pass


    @abstractmethod
    def update_node_parent(self, node: Node, parentId: int, context: ObjectType) -> bool:
        """
        Update parent of node, check if parent is Folder
        :param node: Node object
        :param parentId: parent id
        :param context: Context type
        :return:
        """
        pass


    @abstractmethod
    def available_parent(self, node: Node, parent_node: Node, context: ObjectType) -> bool:
        """
        Validate if can change parent_id for node
        Go recursive to root, if find object, just chceck if can be
        If there is no object, just add it
        :param node: Node
        :param parent_node: Parent node
        :param context Context type
        :return: True if can be there, False otherwise
        """
        pass


    @abstractmethod
    def have_tree_children(self, node: Node) -> bool:
        """
        Find out if node have children
        :param node: tree node
        :return: True if have children, False otherwise
        """
        pass


    @abstractmethod
    def create_empty_object(self, object_type: ObjectType) -> NodeObject:
        """
        Create empty object
        :param object_type: obkect type
        :return: NodeObject if created, None otherwise
        """
        pass


    @abstractmethod
    def get_object(self, node_id: int):
        """
        Get object from node
        :param node_id: id of node
        :return: Node if exist, None otherwise
        """
        pass


    @abstractmethod
    def export_to_html(self, selected: list, path: str) -> None:
        """
        Export data to HTML
        :param selected:  list of selected items
        :param path: path to file, where it will be created
        :return: 
        """
        pass


    @abstractmethod
    def export_to_xml(self, selected: list, path: str):
        """
        Export selected templates to xml
        :param selected: list of selected node in tree
        :param path: path to file, where will be final file
        """
        pass


    @abstractmethod
    def import_from_xml(self, file_path, parentType: ObjectType, parent: int = None, strict: bool = False):
        """
        Import templates from XML file
        :param file_path: path to XML file
        :param parentType: type of parent
        :param strict: if strict is TRUE, only corrent xml templates will be imported 
        :param parent: parent node id
        """
        pass


    @abstractmethod
    def tree_folder(self, node: Node) -> bool:
        """
        Function found if node is folder in root of tree
        :param node: target node
        :return: True if is folder, False otherwise
        """
        pass
