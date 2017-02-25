from data.DAO.LangDAO import LangDAO
from structure.general.Lang import Lang


class LangManager:
    """
    Manager for langs operations
    """


    def __init__(self):
        self.DAO = LangDAO()


    def get_all_langs(self) -> list:
        """
        Return all langs in database
        :return: list of object Langs
        """
        return self.DAO.get_all_langs()


    def lang_exists(self, code: str) -> bool:
        """
        Check if lang code exist in database
        :param code: lang code ( 2 char)
        :return: True if exist, False otherwise
        """
        lang = self.DAO.get_lang_by_code(code)

        if lang:
            return True
        return False


    def get_lang(self, id: int) -> Lang:
        """
        Get lang by id
        :param id: id of lang
        :return: object Lang if exist, None otherwise
        """
        return self.DAO.get_lang(id)


    def get_lang_by_code(self, code):
        """
        Get lang by code
        :param code: lang code (2 char)
        :return: object Lang if exist, None otherwise
        """
        return self.DAO.get_lang_by_code(code)


    def create_lang(self, name, code):
        """
        Create new lang
        :param name: Name of lang
        :param code: Code of lang
        :return: object Lang if created, None otherwise
        """
        if self.lang_exists(code):
            return None
        lang = Lang(None, name, code)
        id = self.DAO.create_lang(lang)
        lang.id = id
        return lang
