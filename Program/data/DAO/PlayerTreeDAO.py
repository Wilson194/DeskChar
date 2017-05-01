from data.DAO.interface.IPlayerTreeDAO import IPlayerTreeDAO
from data.database.Database import Database
from structure.enums.ObjectType import ObjectType
from structure.enums.NodeType import NodeType
from structure.tree.Folder import Folder
from structure.tree.NodeObject import NodeObject
from structure.tree.Node import Node


class PlayerTreeDAO(IPlayerTreeDAO):
    """
    DAO for tree widget
    """
    TABLE_NAME = 'player_tree_structure'
    DATABASE_DRIVER = "file::memory:?cache=shared"


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def get_root_nodes(self, target_type: ObjectType) -> list:
        """
        Get all nodes with parent null
        :param target_type: Type of object
        :return: list of root nodes
        """
        data = self.database.select(self.TABLE_NAME,
                                    {'parent_id': None, 'parent_type': target_type.value})

        return map_objects(data)


    def get_nodes_search(self, targetType: ObjectType, text: str):
        """
        Get nodes witch name contain searched text
        :param targetType: Type of object in node
        :param text: searching text
        :return: list of nodes with text included
        """
        data = self.database.select(self.TABLE_NAME, {'parent_type': targetType.value,
                                                      'name'       : ('like', '%' + text + '%')})
        return map_objects(data)


    def get_node(self, id: int) -> Node:
        """
        Get node by id
        :param id: id of node
        :return: node object if exist, None otherwise
        """
        data = self.database.select(self.TABLE_NAME, {'ID': id})
        return map_objects(data)[0] if len(data) > 0 else None


    def get_children_objects(self, parentNodeId: int, contextType: ObjectType) -> list:
        """
        Recursively find all child object of give type, only first level object (folders will be skipped and searching deep
        :param parentNodeId parent node, where you finding
        :param contextType object type of tree
        :return: list of objects in tree
        """

        nodes = self.get_children_nodes(contextType, parentNodeId)

        objects = []
        for node in nodes:
            if isinstance(node, Folder):
                objects += self.get_children_nodes(contextType, node.id)
            else:
                objects.append(node)

        return objects


    def __get_children_objects(self, targetType, nodeId: int, parentType: ObjectType, objects: list = None, direct: bool = False):
        """
        Private function, return all children object of target node
        :param targetType: Object type
        :param nodeId: id of target node
        :param parentType: Context type
        :param objects: list of object for recursion
        :param direct: if true, only first level child will be add to object list 
        :return: list of children
        """
        if objects is None:
            objects = []

        children = self.get_children_nodes(parentType, nodeId)

        for child in children:
            if direct and isinstance(child, NodeObject) and child.object.object_type is not targetType:
                continue

            objects = self.__get_children_objects(targetType, child.id, parentType, objects, direct=direct)
            if isinstance(child, NodeObject) and child.object.object_type is targetType:
                objects.append(child.object)

        return objects


    def get_children_nodes(self, contextType: ObjectType, parent_id: int) -> list:
        """
        Get all child of parent id
        :param target_type: target type
        :param parent_id: parent id
        :return: list of nodes with parent id, or empty list
        """
        data = self.database.select(self.TABLE_NAME,
                                    {'parent_id': parent_id, 'parent_type': contextType.value})

        return map_objects(data)


    def update_node(self, node: Node):
        """
        Update node data
        :param node: node
        """
        if isinstance(node, Folder):
            values = {
                'parent_id': node.parent_id,
                'name'     : node.name
            }
        else:
            values = {
                'target_id': node.object.id,
                'parent_id': node.parent_id,
                'name'     : node.name
            }
        self.database.update(self.TABLE_NAME, node.id, values)


    def insert_node(self, node: Node, object_type: ObjectType) -> int:
        """
        Create new node in database
        :param node: node object
        :return: id of created node
        """

        if isinstance(node, Folder):
            values = {
                'parent_type': object_type.value,
                'parent_id'  : node.parent_id,
                'type'       : NodeType.FOLDER.value,
                'name'       : node.name
            }
        else:
            values = {
                'target_type': node.object.object_type.value,
                'parent_type': object_type.value,
                'target_id'  : node.object.id,
                'parent_id'  : node.parent_id,
                'type'       : NodeType.OBJECT.value,
                'name'       : node.name

            }
        return self.database.insert(self.TABLE_NAME, values)


    def delete_node(self, id: int):
        """
        Delete node from database
        :param id: id of node
        """
        self.database.delete(self.TABLE_NAME, id)


    def get_node_by_object(self, object: object):
        """
        Return node based on object
        :param object: object that you finding
        :return: ObjectNode with object 
        """
        data = self.database.select(self.TABLE_NAME,
                                    {'target_id'  : object.id,
                                     'parent_type': object.object_type.value})

        return self.get_node(data[0]['id'])


def map_objects(data: dict) -> list:
    """
    Map data from database to Node object
    :param data: data from database
    :return: list of Node objects
    """
    nodes = []
    for row in data:
        if row['type'] is NodeType.FOLDER.value:
            obj = Folder(row['ID'], row['name'], row['parent_id'])
        elif row['type'] is NodeType.OBJECT.value:
            target_object = ObjectType(row['target_type']).instance().DAO()().get(row['target_id'])
            obj = NodeObject(row['ID'], row['name'], row['parent_id'], target_object, ObjectType(row['parent_type']))
        else:
            obj = None
        nodes.append(obj)

    return nodes
