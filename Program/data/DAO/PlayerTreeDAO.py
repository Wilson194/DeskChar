from data.database.Database import Database
from structure.enums.ObjectType import ObjectType
from structure.enums.NodeType import NodeType
from structure.tree.Folder import Folder
from structure.tree.Object import Object
from structure.tree.Node import Node


class PlayerTreeDAO:
    """
    DAO for tree widget
    """
    TABLE_NAME = 'player_tree_structure'


    def __init__(self):
        self.database = Database('test.db')


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


    def get_children_objects(self, targetType: ObjectType, object: object, ) -> list:
        """
        Recursively find all child object of give type
        :param targetType:
        :param nodeId:
        :param parentType:
        :param objects:
        :return:
        """

        node = self.database.select(self.TABLE_NAME,
                                    {'target_id'  : object.id, 'target_type': object.object_type.value,
                                     'parent_type': object.object_type.value})[0]

        return self.__get_children_objects(targetType, node['ID'], object.object_type)


    def __get_children_objects(self, targetType, nodeId, parentType, objects: list = None):
        if objects is None:
            objects = []

        children = self.get_children_nodes(parentType, nodeId)

        for child in children:
            objects = self.__get_children_objects(targetType, child.id, parentType, objects)
            if isinstance(child, Object) and child.object.object_type is targetType:
                objects.append(child.object)

        return objects


    def get_children_nodes(self, target_type: ObjectType, parent_id: int) -> list:
        """
        Get all child of parent id
        :param target_type: target type
        :param parent_id: parent id
        :return: list of nodes with parent id, or empty list
        """
        data = self.database.select(self.TABLE_NAME,
                                    {'parent_id': parent_id, 'parent_type': target_type.value})
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
            obj = Object(row['ID'], row['name'], row['parent_id'], target_object)
        else:
            obj = None
        nodes.append(obj)

    return nodes
