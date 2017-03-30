from structure.general.Singleton import Singleton


class Translate(metaclass=Singleton):
    """
    Function that handle all translates of UI, using files from structure
    """


    def __init__(self, lang_code=None):
        if lang_code is None:
            lang_code = 'cs'
        variables = {}

        exec(open('resources/translate/translate_' + lang_code + '.py', encoding='utf-8').read(),
             variables)

        self.translate_dict = variables['translate']


    def translate(self, value: str) -> str:
        """
        Get translate of value
        :param value:
        :return: Translated string or `Missing trans`
        """
        if str(value) in self.translate_dict:
            return self.translate_dict[str(value)]
        else:
            return 'Missing trans <' + str(value) + '>'


    def tr(self, value : str):
        """
        Get translate of value
        :param value:
        :return: Translated string or `Missing trans`
        """
        return self.translate(value)
