from data.DAO.interface.ISettingsDAO import ISettingsDAO

import os


class SettingsDAO(ISettingsDAO):
    """
    DAO for settings
    """
    SETTINGS_FILE = 'resources/settings.py'

    DEFAULT_SETTINGS = {
        'language': 'cs'
    }


    def __init__(self):

        if os.path.isfile(self.SETTINGS_FILE):
            variables = {}
            exec(open(self.SETTINGS_FILE, encoding='utf-8').read(),
                 variables)

            self.settings = variables['settings']
        else:
            with open(self.SETTINGS_FILE, 'w')as f:
                f.write(self.__dict_to_text(self.DEFAULT_SETTINGS))

            self.settings = self.DEFAULT_SETTINGS


    def get_value(self, name: str, type=None):
        """
        Get value of setting from database, str and int values could be returned
            Type could be str or int
        If not specified, int is first
        :param name: name of setting attribute
        :param type: type of value that will be returned
        :return: value of setting
        """

        if name not in self.settings:
            return None

        if type is str:
            return str(self.settings[name])

        if type is int:
            return int(self.settings[name])

        return str(self.settings[name])


    def set_value(self, name: str, value) -> None:
        """
        Set value for setting, save to database
        :param name: name of setting value
        :param value: value of setting 
        """

        self.settings[name] = value

        with open(self.SETTINGS_FILE, 'w') as f:
            f.write(self.__dict_to_text(self.settings))


    def __dict_to_text(self, dictionary: dict) -> str:
        text = 'settings = {\n'

        for key, value in dictionary.items():
            text += "'{}' : '{}',\n".format(key, value)

        text += '}'

        return text
