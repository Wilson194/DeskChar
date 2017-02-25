from data.database.Database import Database
from structure.general.Lang import Lang


class LangDAO:
    """
    DAO for lang
    """
    TABLE_NAME = 'languages'


    def __init__(self):
        self.database = Database('test.db')


    def get_all_langs(self) -> list:
        """
        Return list of all langs
        :return: List of lang objects
        """
        data = self.database.select_all(self.TABLE_NAME)
        return self.__map_objects(data)


    def get_lang_by_code(self, code: str) -> Lang:
        """
        Get lang from database by code
        :param code: Code of lang (2 char)
        :return: Lang object if exist, None otherwise
        """
        data = self.database.select(self.TABLE_NAME, {'code': code})
        return self.__map_objects(data)[0] if len(data) > 0 else None


    def get_lang(self, id: int) -> Lang:
        """
        Get lang by id
        :param id: id of lang
        :return: Lang object if exist, None otherwise
        """
        data = self.database.select(self.TABLE_NAME, {'ID': id})
        return self.__map_objects(data)[0] if len(data) > 0 else None


    def create_lang(self, lang: Lang):
        """
        Create new lang
        :param lang: lang object
        :return: id of created lang
        """
        values = {
            'name': lang.name,
            'code': lang.code
        }
        return self.database.insert(self.TABLE_NAME, values)


    def __map_objects(self, data: dict) -> list:
        """
        Map data from database to Lang objects
        :param data:
        :return:
        """
        langs = []
        for line in data:
            lang = Lang(line['ID'], line['name'], line['code'])
            langs.append(lang)
        return langs
