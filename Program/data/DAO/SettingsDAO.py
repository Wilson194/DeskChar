from data.DAO.interface.ISettingsDAO import ISettingsDAO
from data.database.Database import Database
from structure.general.Lang import Lang


class SettingsDAO(ISettingsDAO):
    """
    DAO for settings
    """
    TABLE_NAME = 'Settings'
    DATABASE_DRIVER = "file::memory:?cache=shared" # TODO: Database


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def get_value(self, name: str, type=None):
        """
        Get value of setting from database, str and int values could be returned
            Type could be str or int
        If not specified, int is first
        :param name: name of setting attribute
        :param type: type of value that will be returned
        :return: value of setting
        """
        data = self.database.select(self.TABLE_NAME, {'name': name})
        if len(data) == 0:
            return None
        intValue = data[0]['int_value']
        strValue = data[0]['str_value']

        if type is str:
            return strValue
        if type is int:
            return intValue
        if intValue:
            return intValue

        return strValue


    def set_value(self, name: str, value) -> None:
        """
        Set value for setting, save to database
        :param name: name of setting value
        :param value: value of setting 
        """
        data = self.database.select(self.TABLE_NAME, {'name': name})
        if len(data) == 0:
            if type(value) is int:
                self.database.insert(self.TABLE_NAME, {'name': name, 'int_value': value})
            else:
                self.database.insert(self.TABLE_NAME, {'name': name, 'str_value': value})
        else:
            id = data[0]['ID']
            if type(value) is int:
                self.database.update(self.TABLE_NAME, id, {'int_value': value})
            else:
                self.database.update(self.TABLE_NAME, id, {'str_value': value})
