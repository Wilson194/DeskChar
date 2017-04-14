from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.database.Database import *
from structure.enums.AutoNumber import AutoNumber
from structure.enums.ObjectType import ObjectType

from structure.general.Object import Object
from structure.tree.NodeObject import NodeObject


class ObjectDatabase(Database):
    """
    Class that extend class Database, can handlig mapping object to database
    NodeObject need function __name__ that return list of table names (hierarchy)
    """


    def insert_object(self, obj: Object, database_table: str = None, rootParentType: object = None,
                      parentId: int = None, parentObject: object = None,
                      recursionLevel: int = 1) -> int:
        """
        Insert object to database, map translates to translate table
        :param obj: given object
        :param database_table: database table name
        :return: id of autoincrement
        """
        database_name = database_table if database_table else obj.__name__()[-1]
        str_values = {}
        int_values = {}
        list_values = []

        for key, value in obj.__dict__.items():
            if not compare(key, obj.__name__()):
                continue
            else:
                key = substr(key, obj.__name__())
            if key not in obj.TABLE_SCHEMA:
                if type(value) is list:
                    for item in value:
                        list_values.append(item)
            elif isinstance(value, AutoNumber):
                int_values[key] = value.value
            elif type(value) is int:
                int_values[key] = value
            elif type(value) is str:
                str_values[key] = value
            else:
                continue

        if not int_values:
            db_id = self.insert_null(database_name)
        else:
            db_id = self.insert(database_name, int_values, True)

        for key, value in str_values.items():
            data_dict = {
                'lang'     : obj.lang,
                'target_id': db_id,
                'type'     : obj.object_type.value if obj.object_type else None,
                'name'     : key,
                'value'    : value
            }
            self.insert('translates', data_dict)

        # Insert into tree with same object
        obj.id = db_id

        nodeParent = parentId if not parentObject else None

        node = NodeObject(None, obj.name, nodeParent, obj)
        nodeId = PlayerTreeDAO().insert_node(node, obj.object_type)

        # Add to importing tree
        if parentObject:
            if obj.object_type is ObjectType.MODIFIER:
                from data.DAO.EffectDAO import EffectDAO
                EffectDAO().create_link(parentObject, obj)
            elif obj.object_type is ObjectType.EFFECT and parentObject.object_type == ObjectType.ITEM:
                from data.DAO.ItemDAO import ItemDAO
                ItemDAO().create_effect_link(parentObject, obj)
            else:
                node = NodeObject(None, obj.name, parentId, obj)
                PlayerTreeDAO().insert_node(node, rootParentType)

        for item in list_values:
            self.insert_object(item, item.object_type.name.title(), rootParentType, nodeId, obj,
                               recursionLevel + 1)

        return db_id


    def update_object(self, obj: Object, database_table: str = None):
        """
        Update object in database, update all translate columns
        :param obj: given object
        """
        database_name = database_table if database_table else obj.__name__()[-1]
        if obj.id is None:
            raise ValueError('Cant update object without ID')
        data = self.select(database_name, {'ID': obj.id})

        if not data:
            raise ValueError('Cant update none existing object')

        int_values = {}
        str_values = {}
        for key, value in obj.__dict__.items():
            if not compare(key, obj.__name__()):
                continue
            else:
                key = substr(key, obj.__name__())

            if key not in obj.TABLE_SCHEMA:
                continue
            elif isinstance(value, AutoNumber):
                int_values[key] = value.value
            elif type(value) is int:
                int_values[key] = value
            elif type(value) is str or type(value) is bytes:
                str_values[key] = value
            else:
                continue

        self.update(database_name, obj.id, int_values)

        translates = self.select('translates',
                                 {'target_id': obj.id,
                                  'type'     : obj.object_type.value,
                                  'lang'     : obj.lang})
        for key, value in str_values.items():
            db_line = get_line(key, translates)

            if db_line is None:
                data_dict = {
                    'name'     : key,
                    'value'    : value,
                    'lang'     : obj.lang,
                    'target_id': obj.id,
                    'type'     : obj.object_type.value
                }

                self.insert('translates', data_dict)
            else:
                if db_line['value'] != value:
                    data_dict = {
                        'name' : key,
                        'value': value
                    }
                    self.update('translates', db_line['ID'], data_dict)


def compare(name: str, objects: list) -> bool:
    for one in objects:
        if one in name:
            return True
    return False


def substr(string: str, objects: list):
    for one in objects:
        if one in string:
            return string.split(one)[1][2:]


def get_line(key: str, data):
    for line in data:
        if line['name'] == key:
            return line
    return None
