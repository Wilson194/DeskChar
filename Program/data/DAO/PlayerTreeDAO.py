from data.DAO.AbilityDAO import AbilityDAO
from data.DAO.ItemDAO import ItemDAO
from data.DAO.SpellDAO import SpellDAO
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
                                    {'parent_id': None, 'target_type': target_type.value})

        return map_objects(data)


    def get_node(self, id: int) -> Node:
        """
        Get node by id
        :param id: id of node
        :return: node object if exist, None otherwise
        """
        data = self.database.select(self.TABLE_NAME, {'ID': id})
        return map_objects(data)[0] if len(data) > 0 else None


    def get_children_nodes(self, target_type: ObjectType, parent_id: int) -> list:
        """
        Get all child of parent id
        :param target_type: target type
        :param parent_id: parent id
        :return: list of nodes with parent id, or empty list
        """
        data = self.database.select(self.TABLE_NAME,
                                    {'parent_id': parent_id, 'target_type': target_type.value})
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
                'target_type': object_type.value,
                'parent_id'  : node.parent_id,
                'type'       : NodeType.FOLDER.value,
                'name'       : node.name
            }
        else:
            values = {
                'target_type': object_type.value,
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
            if row['target_type'] is ObjectType.ITEM.value:
                target_object = ItemDAO().get_item(row['target_id'])
            elif row['target_type'] is ObjectType.SPELL.value:
                target_object = SpellDAO().get_spell(row['target_id'])
            elif row['target_type'] is ObjectType.ABILITY.value:
                target_object = AbilityDAO().get_ability(row['target_id'])
            else:
                target_object = None

            obj = Object(row['ID'], row['name'], row['parent_id'], target_object)
        else:
            obj = None

        nodes.append(obj)

    return nodes