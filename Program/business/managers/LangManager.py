from data.DAO.LangDAO import LangDAO
from structure.general.Lang import Lang


class LangManager:
    def __init__(self):
        self.DAO = LangDAO()


    def get_all_langs(self):
        return self.DAO.get_all_langs()


    def lang_exists(self, code):
        lang = self.DAO.get_lang_by_code(code)

        if lang:
            return True

        return False


    def get_lang(self, id):
        return self.DAO.get_lang(id)


    def create_lang(self, name, code):
        lang = Lang(None, name, code)
        id = self.DAO.create_lang(lang)
        lang.id = id
        return lang

