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
            elif type(value) is str:
                str_values[substr(key, obj.__name__())] = value
            else:
                continue
        self.insert(obj.__name__()[-1], int_values)


def compare(name: str, objects: list) -> bool:
    for one in objects:
        if one in name:
            return True
    return False


def substr(string: str, objects: list):
    for one in objects:
        if one in string:
            return string.split(one)[1][2:]
