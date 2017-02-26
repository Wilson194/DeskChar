class Lang:
    """
    Class for handling langs
    """


    def __init__(self, id: int = None, name: str = None, code: str = None):
        """
        Basic constructor
        :param id: id of lang
        :param name: long name of lang
        :param code: 2 char long code of lang (unique)
        """
        self.__id = id
        self.__name = name
        self.__code = code


    @property
    def id(self) -> int:
        """
        Id of lang
        """
        return self.__id


    @id.setter
    def id(self, value: int):
        self.__id = value


    @property
    def name(self) -> str:
        """
        Long name of lang
        """
        return self.__name


    @name.setter
    def name(self, value: str):
        self.__name = value


    @property
    def code(self) -> str:
        """
        2 char long
        """
        return self.__code


    @code.setter
    def code(self, value: str):
        self.__code = value
