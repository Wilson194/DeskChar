from data.database.Database import Database
from structure.general.Lang import Lang


class LangDAO:
    TABLE_NAME = 'languages'


    def __init__(self):
        self.database = Database('test.db')


    def get_all_langs(self):
        data = self.database.select_all(self.TABLE_NAME)
        return self.map_objects(data)


    def get_lang_by_code(self, code):
        data = self.database.select(self.TABLE_NAME, {'code': code})
        return self.map_objects(data)[0] if len(data) > 0 else None


    def get_lang(self, id):
        data = self.database.select(self.TABLE_NAME, {'ID': id})
        return self.map_objects(data)[0] if len(data) > 0 else None


    def map_objects(self, data):
        langs = []
        for line in data:
            lang = Lang(line['ID'], line['name'], line['code'])
            langs.append(lang)
        return langs


    def create_lang(self, lang: Lang):
        values = {
            'name': lang.name,
            'code': lang.code
        }
        return self.database.insert(self.TABLE_NAME, values)
