from AbilityDAO import AbilityDAO
from ItemDAO import ItemDAO
from SpellDAO import SpellDAO
from database.ObjectDatabase import ObjectDatabase
from Database import Database
from enums.ObjectType import ObjectType
from structure.enums.NodeType import NodeType
from structure.tree.Folder import Folder
from structure.tree.Object import Object


class PlayerTreeDAO:
    TABLE_NAME = 'player_tree_structure'


    def __init__(self):
        self.database = Database('test.db')


    def get_root_nodes(self, target_type: int) -> list:
        data = self.database.select(self.TABLE_NAME,
                                    {'parent_id': None, 'target_type': target_type})

        return map_objects(data)

    def get_node(self, id):
        data = self.database.select(self.TABLE_NAME, {'ID':id})
        return map_objects(data)[0]


    def get_children_nodes(self, target_type: int, parent_id: int):
        data = self.database.select(self.TABLE_NAME,
                                    {'parent_id': parent_id, 'target_type': target_type})
        return map_objects(data)


    def update_node(self, node):
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


    def insert_node(self, node):
        if isinstance(node, Folder):
            values = {
                'target_type': ObjectType.SPELL.value,  # TODO
                'parent_id'  : node.parent_id,
                'type'       : NodeType.FOLDER.value,
                'name'       : node.name
            }
        else:
            values = {
                'target_type': ObjectType.SPELL.value,  # TODO
                'target_id'  : node.object.id,
                'parent_id'  : node.parent_id,
                'type'       : NodeType.OBJECT.value,
                'name'       : node.name

            }
        self.database.insert(self.TABLE_NAME, values)


    def delete_node(self, id):

        self.database.delete(self.TABLE_NAME, id)


def map_objects(data):
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
