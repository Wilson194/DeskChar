from data.database.Database import *
from structure.enums.Classes import Classes
from structure.enums.Handling import Handling
from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType
from structure.enums.Races import Races
from structure.enums.WeaponWeight import WeaponWeight
from structure.general.Object import Object


class ObjectDatabase(Database):
    """
    Class that extend class Database, can handlig mapping object to database
    Object need function __name__ that return list of table names (hierarchy)
    """


    def insert_object(self, obj: Object, database_table: str = None) -> int:
        """
        Insert object to database, map translates to translate table
        :param obj: given object
        :param database_table: database table name
        :return: id of autoincrement
        """
        database_name = database_table if database_table else obj.__name__()[-1]

        str_values = {}
        int_values = {}
        for key, value in obj.__dict__.items():
            if not compare(key, obj.__name__()):
                continue
            elif type(value) in (Classes, Races, Handling, WeaponWeight, Items):
                int_values[substr(key, obj.__name__())] = value.value
            elif type(value) is int:
                int_values[substr(key, obj.__name__())] = value
            elif 'type' in key:
                int_values[substr(key, obj.__name__())] = value
            elif 'lang' in key:
                continue
            elif type(value) is str:
                str_values[substr(key, obj.__name__())] = value
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
            if type(value) is int:
                int_values[substr(key, obj.__name__())] = value
            elif type(value) in [WeaponWeight, Handling]:
                int_values[substr(key, obj.__name__())] = value.value
            elif 'type' in key:
                int_values[substr(key, obj.__name__())] = value.value
            elif 'lang' in key:
                continue
            elif 'id' in key:
                continue
            elif type(value) is str or type(value) is bytes:
                str_values[substr(key, obj.__name__())] = value
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
