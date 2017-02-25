from structure.general.Singleton import Singleton
import os, sys


class Translate(metaclass=Singleton):
    """
    Function that handle all translates of UI, using files from structure
    """


    def __init__(self, lang=None):
        variables = {}

        print(os.getcwd())
        exec(open('resources/translate/translate_cs.py', encoding='utf-8').read(),
             variables)  # TODO

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
            return 'Missing trans'


    def tr(self, value):
        """
        Get translate of value
        :param value:
        :return: Translated string or `Missing trans`
        """
        return self.translate(value)
