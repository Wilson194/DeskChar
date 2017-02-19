from structure.general.Singleton import Singleton
import os, sys


class Translate(metaclass=Singleton):
    def __init__(self, lang=None):
        variables = {}

        print(os.getcwd())
        exec(open('resources/translate/translate_cs.py', encoding='utf-8').read(), variables)

        self.translate_dict = variables['translate']


    def translate(self, value):
        if str(value) in self.translate_dict:
            return self.translate_dict[str(value)]
        else:
            return 'Missing trans'


    def tr(self, value):
        return self.translate(value)
