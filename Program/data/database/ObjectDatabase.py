from datetime import date

from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.database.Database import *
from structure.enums.AutoNumber import AutoNumber
from structure.enums.ObjectType import ObjectType

from structure.general.Object import Object
from structure.tree.NodeObject import NodeObject


class ObjectDatabase(Database):
    def insert_translate(self, strValues: dict, lang: str, objectId: int, objectType: ObjectType) -> None:
        """
        Insert translate for object to database
        :param strValues: dictionary of names and values  
        :param lang: lang of translate
        :param objectId: id ob object
        :param objectType: objectType of object
        """
        if not lang:  # TODO: default lang
            lang = 'cs'

        self.set_many(True)
        for name, value in strValues.items():
            data = {
                'lang'     : lang,
                'target_id': objectId,
                'type'     : objectType.value,
                'name'     : name,
                'value'    : value
            }

            self.insert('translates', data)
        self.insert_many_execute()
        self.set_many(False)


    def update_translate(self, strValues: dict, lang: str, objectId: int, objectType: ObjectType) -> None:
        """
        Update translates in database
        :param strValues: dictionary of names and values
        :param lang: lang of translates
        :param objectId: id of object
        :param objectType: Object type of object        
        """
        translates = self.select('translates',
                                 {'target_id': objectId,
                                  'type'     : objectType.value,
                                  'lang'     : lang})
        self.set_many(True)
        for name, value in strValues.items():
            db_line = get_line(name, translates)

            if db_line is None:
                data_dict = {
                    'name'     : name,
                    'value'    : value,
                    'lang'     : lang,
                    'target_id': objectId,
                    'type'     : objectType.value
                }

                self.insert('translates', data_dict)
            else:
                if db_line['value'] != value:
                    data_dict = {
                        'value': value
                    }
                    self.update('translates', db_line['ID'], data_dict)

        self.insert_many_execute()
        self.set_many(False)


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
