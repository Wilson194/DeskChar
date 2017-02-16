from Database import *
from structure.general.Object import Object


class ObjectDatabase(Database):
    def insert_object(self, obj: Object):
        str_values = {}
        int_values = {}
        for key, value in obj.__dict__.items():
            if not compare(key, obj.__name__()):
                continue
            if type(value) is int:
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
            db_id = self.insert_null(obj.__name__()[-1])
        else:
            db_id = self.insert(obj.__name__()[-1], int_values)

        for key, value in str_values.items():
            data_dict = {
                'lang': obj.lang,
                'target_id': db_id,
                'type': obj.__name__()[-1],
                'name': key,
                'value': value
            }
            self.insert('translates', data_dict)

        return db_id


    def update_object(self, obj: Object):
        if obj.id is None:
            raise ValueError('Cant update object without ID')
        data = self.select(obj.__name__()[-1], {'ID': obj.id})

        if not data:
            raise ValueError('Cant update none existing object')

        int_values = {}
        str_values = {}
        for key, value in obj.__dict__.items():
            if not compare(key, obj.__name__()):
                continue
            if type(value) is int:
                int_values[substr(key, obj.__name__())] = value
            elif 'type' in key:
                int_values[substr(key, obj.__name__())] = value
            elif 'lang' in key:
                continue
            elif 'id' in key:
                continue
            elif type(value) is str:
                str_values[substr(key, obj.__name__())] = value
            else:
                continue
        self.update(obj.__name__()[-1], obj.id, int_values)

        translates = self.select('translates',
                                 {'target_id': obj.id,
                                  'type': obj.__name__()[-1],
                                  'lang': obj.lang})

        for key, value in str_values.items():
            db_id = get_id(key, translates)
            if db_id is None:
                pass
            else:
                data_dict = {
                    'name': key,
                    'value': value
                }
                self.update('translates', db_id, data_dict)


def compare(name: str, objects: list) -> bool:
    for one in objects:
        if one in name:
            return True
    return False


def substr(string: str, objects: list):
    for one in objects:
        if one in string:
            return string.split(one)[1][2:]


def get_id(key: str, data):
    for line in data:
        if line['name'] == key:
            return line['ID']
    return None
