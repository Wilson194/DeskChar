from structure.general.Singleton import Singleton


class Synchronizer(metaclass=Singleton):
    """
    This class is used to share data between all widgets in application
    """


    def __init__(self):
        self.__data = {}


    def save_data(self, name: str, data):
        """
        Save data to singleton
        :param name: name of data
        :param data: data, could be everything
        """
        self.__data[name] = data


    def get_data(self, name: str):
        """
        Get data from singleton
        :param name: name of data
        :return: data
        """
        return self.__data.get(name, None)


    def delete_data(self, name):
        """
        Delete data from singleton
        :param name: name of data you want to delete
        """
        self.__data[name] = None
