from structure.general.Object import Object


class Modifier(Object):
    def __init__(self, id: int = None, lang: str = None, name: str = None,
                 description: str = None, id_parent_effect: int = None,
                 id_target: int = None, value_type: int = None,
                 value_target: int = None,
                 value: int = None):
        super().__init__(id, lang, name, description)

        self.__id_parent_effect = id_parent_effect
        self.__id_target = id_target
        self.__value_type = value_type
        self.__value_target = value_target
        self.__value = value


    def __name__(self):
        names = super().__name__()
        names.append('Modifier')
        return names


    @property
    def id_target(self):
        return self.__id_target


    @id_target.setter
    def id_target(self, value):
        self.__id_target = value


    @property
    def value_type(self):
        return self.__value_type


    @value_type.setter
    def value_type(self, value):
        self.__value_type = value


    @property
    def value_target(self):
        return self.__value_target


    @value_target.setter
    def value_target(self, value):
        self.__value_target = value


    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, value):
        self.__value = value


    @property
    def id_parent_effect(self):
        return self.__id_parent_effect


    @id_parent_effect.setter
    def id_parent_effect(self, value):
        self.__id_parent_effect = value
