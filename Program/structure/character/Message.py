from datetime import date


class Message:
    def __init__(self, id: int = None, text: str = None, date: date = None, isMine: bool = None):
        self.__id = id
        self.__text = text
        self.__date = date
        self.__isMine = isMine


    @property
    def id(self):
        return self.__id


    @id.setter
    def id(self, value):
        self.__id = value


    @property
    def text(self):
        return self.__text


    @text.setter
    def text(self, value):
        self.__text = value


    @property
    def date(self):
        return self.__date


    @date.setter
    def date(self, value):
        self.__date = value


    @property
    def isMine(self):
        return self.__isMine


    @isMine.setter
    def isMine(self, value):
        self.__isMine = value
