from data.DAO.SettingsDAO import SettingsDAO
from data.database.Database import Database
from structure.enums.ObjectType import ObjectType


class DAO:
    DATABASE_DRIVER = "file::memory:?cache=shared"
    DATABASE_TABLE = None
    TYPE = None


    def get_all_data(self, id: int) -> dict:
        """
        Get all data dictionary of one spell, all langs
        :param id: id of object
        :return: dictionary of all data
        """
        data = {}
        int_data = dict(Database(self.DATABASE_DRIVER).select(self.DATABASE_TABLE, {'ID': id})[0])
        tr_data = Database(self.DATABASE_DRIVER).select('translates',
                                                        {'target_id': id, 'type': self.TYPE.value})
        for key, value in int_data.items():
            data[key] = value

        for line in tr_data:
            name = line['name']
            lang = line['lang']
            value = line['value']

            if name in data:
                data[name][lang] = value
            else:
                data[name] = {}
                data[name][lang] = value

        return data


    def get_languages(self, id: int) -> list:
        """
        Get list of all languages codes for this object
        :param id: id of spell
        :return: list of langs codes
        """
        if self.TYPE is None:
            raise ValueError('Constant TYPE is not defined in class {}'.format(self))
        data = Database(self.DATABASE_DRIVER).select('translates',
                                                     {'target_id': id, 'type': self.TYPE.value})

        languages = []
        for line in data:
            if line['lang'] not in languages:
                languages.append(line['lang'])
        if len(languages) == 0:
            languages.append(SettingsDAO().get_value('language', str))
        return languages


    def get_list(self, id: int, nodeId: int = None, contextType: ObjectType = None):
        """
        Return list of object for one ID but all languages
        :param id: id of object
        :return: list of objects
        """
        languages = self.get_languages(id)
        objects = []
        for lang in languages:
            objects.append(self.get(id, lang, nodeId, contextType))
        return objects
