class Lang:
    def __init__(self, id: int = None, name: str = None, code: str = None):
        self.__id = id
        self.__name = name
        self.__code = code


    @property
    def id(self):
        return self.__id


    @id.setter
    def id(self, value):
        self.__id = value


    @property
    def name(self):
        return self.__name


    @name.setter
    def name(self, value):
        self.__name = value


    @property
    def code(self):
        return self.__code


    @code.setter
    def code(self, value):
        self.__code = value
